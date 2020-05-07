__author__ = 'haim.levy@post.idc.ac.il'

from CombTrainerTester.Combiner import Combiner
from CombTrainerTester.OnDemandDHCPClassifier import OnDemandDHCPClassifier
from CombTrainerTester.TrafficClassifier import TrafficClassifier
from CombTrainerTester.base_libs.DeviceTagsLoader import DeviceTagsLoader
import numpy as np

SEEN_ORACLE = r"train_oracle.csv"
ORACLE = r"full_oracle.csv"
FEATURES_PATH = r"features/"
DHCP_FDB_PATH = r"full_dhcp_db.csv"


features = {60: ['remote_ip', 'max_winds'],  # 60
            300: ['ethlen', 'max_winds', 'remote_ip', 'tcp_udp_ratio', 'udns'],  # 300
            600: ['remote_ip', 'max_winds', 'udns', 'avg_ua'],  # 600
            1200: ['tcp_udp_ratio', 'max_winds', 'udns', 'avg_ua'],  # 1200
            }

dtl = DeviceTagsLoader(ORACLE)
full_oracle = dtl.devs
dhcp_on_demand = OnDemandDHCPClassifier(ORACLE, DHCP_FDB_PATH)


def keys_mac2fol(mac, items):
    for k in items:
        if mac in k.replace("-", ":"):
            return k


def keys_fol2mac(key, oracle):
    for dev in oracle:
        if dev.mac in key.replace("-", ":"):
            return dev.mac


def get_fol2dev(key):
    for dev in full_oracle.values():
        if dev.mac in key.replace("-", ":"):
            return dev


def train(sw):
    comb = Combiner()
    tclassi = TrafficClassifier(FEATURES_PATH + "train/", FEATURES_PATH + "train/")
    tclassi.fit(sw, features[sw])
    qt = tclassi.classify_test_folder("train " + str(sw))
    qd = {}
    for ky in qt.keys():
        dev = get_fol2dev(ky)
        sids = tclassi.get_dev_sids(dev.mac, sw)
        qd[ky] = dhcp_on_demand.classify_device(dev, sids, slot_width=sw)

    qt_vec = []
    qd_vec = []
    y_vec = []
    for ky in qt.keys():
        dev = get_fol2dev(ky)
        qt_vec = np.hstack((qt_vec, qt[ky]))
        qd_vec = np.hstack((qd_vec, qd[ky]))
        y_vec = np.hstack((y_vec, [int(dev.isiot) for i in xrange(len(qt[ky]))]))
    comb.fit(qt_vec, qd_vec, y_vec)
    return comb


def classify(comb, sw):
    tclassi = TrafficClassifier(FEATURES_PATH + "train/", FEATURES_PATH + "test/")
    tclassi.fit(sw, features[sw])
    qt = tclassi.classify_test_folder("test " + str(sw))
    qd = {}
    for ky in tclassi.test_X.keys():
        dev = get_fol2dev(ky)
        sids = tclassi.get_dev_sids(dev.mac, sw)
        qd[ky] = dhcp_on_demand.classify_device(dev, sids, slot_width=sw)

    qt_vec = []
    qd_vec = []
    y_vec = []
    for ky in tclassi.test_X.keys():
        dev = get_fol2dev(ky)
        qt_vec = np.hstack((qt_vec, qt[ky]))
        qd_vec = np.hstack((qd_vec, qd[ky]))
        y_vec = np.hstack((y_vec, [int(dev.isiot) for i in xrange(len(qt[ky]))]))
    comb.classify(qt_vec, qd_vec, y_vec, sw)
    return comb


def process(sw):
    comb = train(sw)
    classify(comb, sw)


def main():
    process(60)
    process(300)
    process(600)
    process(1200)


main()
