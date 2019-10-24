__author__ = 'haim.levy@post.idc.ac.il'

import pickle
from sklearn.metrics import confusion_matrix
from base_libs.DeviceTagsLoader import DeviceTagsLoader
from base_libs.DHCPRecord import DHCPRecord
from base_libs.DBReader import DBReader


class OnDemandDHCPClassifier:
    def __init__(self, oracle, dhcp_fdb):
        self.enc = pickle.load(open("../dumps/dhcp_enc.bin", "rb"))
        self.classifier = pickle.load(open("../dumps/dhcp_classifier.bin", "rb"))
        self.dict = {}
        dtl = DeviceTagsLoader(oracle)
        self.oracle = dtl.devs
        dhcp_reader = DBReader(dhcp_fdb, DHCPRecord())
        self.dhcp_records = dhcp_reader.read()

    def classify(self, dev, slot_id, slot_width=1200):
        tn, fp, fn, tp = 0, 0, 0, 0

        k = None
        for dd in self.oracle.values():
            if dd.mac in dev.replace("-", ":"):
                k = dd.mac
                break
        if k is None:
            # print "ERROR: key=", dev, "not found!"
            return

        labels = []
        X, y = [], []
        dps = get_dev_sw_slots(self.dhcp_records, k, 0)
        for dp in dps:
            if not is_record_in_width(dp, slot_id, slot_width):
                continue
            labels += self.prepare_vector(dp.hostname, dp.vendor_class, dp.req_lst, dp.mds, dp.msg_t)
        if len(labels) == 0:
            return None
        labels = list(set(labels))
        X.append(labels)
        y.append(int(dev.isiot))

        return self.test_device(X, y, dev)

    def test_device(self, X, y, dev):
        y_pred = self.classifier.predict(X)
        if y_pred == y[0]:
            return 1
        else:
            return 0

    def prepare_vector(self, hn, vci, req_lst, mds, msg_t):
        if vci is None:
            vci = ''
        if hn is None:
            hn = ''
        labels = []
        labels += add_catagory(filter_labels(sanitize_string(hn)), 'hostname')
        labels += add_catagory(filter_labels(sanitize_string(vci)), 'vci')
        labels += add_catagory(sanitize_string(req_lst), 'prl')
        labels += add_catagory(sanitize_string(mds), 'mds')
        labels += add_catagory(sanitize_string(msg_t), 'msg_t')
        labels = self.encode(labels)
        return labels

    def encode(self, labels):
        labels = list(set(labels))
        lbls = [[label] for label in labels]
        res = self.enc.transform(lbls).toarray()
        rr = res[0]
        for r in res[1:]:
            rr += r
        return rr


def get_dev_sw_slots(records, dev, sw):
    rr = [f for f in records if f.mac == dev.mac and f.slot_width == sw]
    return rr

def is_record_in_width(record, slot_id, slot_width):
    if slot_id <= record.slot_id <= slot_id + slot_width:
        return True
    return False

def sanitize_string(string):
    string = string.lower()
    string = string.replace(";", '')
    chars = '.,|{}[]()-+=:/\\'
    string = string.replace("'", '')
    for c in chars:
        string = string.replace(c, ' ')
    res = string.split(' ')
    return res


def filter_labels(labels):
    res = []
    for l in labels:
        try:
            int(l)
            float(l)
        except:
            res.append(l)
    return res


def add_catagory(lst, category):
    res = [category + ':' + str(x) for x in lst]
    return res


def dhcp_classifier(dhcp_fdb, oracle):
    dhclassi = DHCPClassifier()
    dict = dhclassi.classify(oracle, dhcp_fdb)
    return dict

