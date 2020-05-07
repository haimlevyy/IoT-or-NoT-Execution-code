__author__ = 'haim.levy@post.idc.ac.il'

import pickle
from sklearn.metrics import confusion_matrix
from base_libs.DeviceTagsLoader import DeviceTagsLoader
from base_libs.DHCPRecord import DHCPRecord
from base_libs.DBReader import DBReader


class DHCPClassifier:
    def __init__(self):
        self.enc = pickle.load(open("../dumps/dhcp_enc.bin", "rb"))
        self.classifier = pickle.load(open("../dumps/dhcp_classifier.bin", "rb"))
        self.dict = {}

    def classify(self, oracle, dhcp_fdb):
        dtl = DeviceTagsLoader(oracle)
        oracle = dtl.devs
        dhcp_reader = DBReader(dhcp_fdb, DHCPRecord())
        dhcp_records = dhcp_reader.read()
        tn, fp, fn, tp = 0, 0, 0, 0

        for dev in oracle.values():
            X, y = [], []
            dps = get_dev_sw_slots(dhcp_records, dev, 1)
            for dp in dps:
                labels = self.prepare_vector(dp.hostname, dp.vendor_class, dp.req_lst, dp.mds, dp.msg_t)
                X.append(labels)
                y.append(int(dev.isiot))
            if len(X) == 0:
                continue
                

            d_tp, d_tn, d_fp, d_fn = self.test_per_device(X, y, dev)
            tp, tn, fp, fn = tp + d_tp, tn + d_tn, fp + d_fp, fn + d_fn
        print '-----------------------------------------------------'
        print 'Total results for DHCP based classification'
        print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        print 'recall', float(tp) / (tp + fn) * 100
        print 'precision', float(tp) / (tp + fp) * 100
        print '-----------------------------------------------------'
        return self.dict

    def test_per_device(self, X, y, dev):
        y_pred = self.classifier.predict(X)
        tn, fp, fn, tp = 0, 0, 0, 0
        resu = confusion_matrix(y, y_pred).ravel()
        if len(resu) == 1:
            if y[0] == 0:
                tn = resu[0]
            else:
                tp = resu[0]
        else:
            tn, fp, fn, tp = resu

        all = float(tp + fp + tn + fn)
        print "Classifying results for device:", dev.desc, dev.mac,
        print "(NoT, IoT) = " + str((fn + tn)/all) + ", " + str((tp + fp)/all)
        self.dict[dev.mac] = (tp + tn) / all
        tp, tn, fp, fn = tp / all, tn / all, fp / all, fn / all
        return tp, tn, fp, fn

    def prepare_vector(self, hn, vci, req_lst, mds, msg_t):
        if vci is None:
            vci = ''
        if hn is None:
            hn = ''
        labels = []
        labels += add_catagory(filter_labels(sanitize_string_vci(hn)), 'hostname')
        labels += add_catagory(filter_labels(sanitize_string_vci(vci)), 'vci')
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
    rr = [f for f in records if f.mac == dev.mac]
    return rr

def sanitize_string_vci(string):
    string = string.lower()
    string = string.replace("'", '')
    nono = "0123456789."
    for no in nono:
        string = string.replace(no, '')
    string = string.replace("'", '')
    string = string.replace(";", ':')
    chars = ',|{}[]()+=/\\'
    for c in chars:
        string = string.replace(c, ':')
    res = string.split(':')
    return res

def sanitize_string(string):
    string = string.lower()
    string = string.replace("'", '')
    string = string.replace(";", ':')
    chars = ',|{}[]()+=/\\'
    for c in chars:
        string = string.replace(c, ':')
    res = string.split(':')
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

