__author__ = 'haim.levy@post.idc.ac.il'

import pickle

from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from Common.DBReader import DBReader
from Common.DHCPRecord import DHCPRecord
from Common.DeviceTagsLoader import *
import graphviz
from sklearn import tree

ORACLE_PATH = "oracles\\"

SEEN_DHCPDB = r"full_dhcp_db.csv"
UNSEEN_DHCPDB = r"full_dhcp_db.csv"
SEEN_ORACLE = r"train_oracle.csv"
UNSEEN_ORACLE = r"test_oracle.csv"


def get_dev_sw_slots(records, dev, sw):
    rr = [f for f in records if f.mac == dev.mac and f.slot_width == sw]
    return rr


def sanitize_string(string):
    string = string.lower()
    string = string.replace("'", '')
    string = string.replace(";", ':')
    chars = ',|{}[]()+=/-\\'
    for c in chars:
        string = string.replace(c, ':')
    res = string.split(':')
    return res


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


def add_catagory(lst, category):
    res = [category + ':' + str(x) for x in lst]
    return res


def encode(labels, enc):
    labels = list(set(labels))
    lbls = [[label] for label in labels]
    res = enc.transform(lbls).toarray()
    rr = res[0]
    for r in res[1:]:
        rr += r
    return rr


def init_enc(labels):
    enc = OneHotEncoder(handle_unknown='ignore')
    X = [[i] for i in labels]
    enc.fit(X)
    return enc


def filter_labels(labels):
    res = []
    for l in labels:
        try:
            int(l)
            float(l)
        except:
            res.append(l)
    return res


def prepare_vector(hn, vci, req_lst, mds, msg_t, client_id, enc):
    if vci is None:
        vci = ''
    if hn is None:
        hn = ''
    labels = []
    labels += add_catagory(filter_labels(sanitize_string(hn)), 'hostname')
    labels += add_catagory(filter_labels(sanitize_string_vci(vci)), 'vci')
    labels += add_catagory(sanitize_string(req_lst), 'prl')
    labels += add_catagory(sanitize_string(mds), 'mds')
    labels += add_catagory(sanitize_string(msg_t), 'msg_t')
    labels = encode(labels, enc)
    # print labels
    return labels


def prepare_tagged(dhcp, oracle, enc):
    X = []
    y = []
    for dev in oracle.values():
        dps = get_dev_sw_slots(dhcp, dev, 1)
        for dp in dps:
            labels = prepare_vector(dp.hostname, dp.vendor_class, dp.req_lst, dp.mds, dp.msg_t, dp.client_id, enc)
            X.append(labels)
            y.append(int(dev.isiot))
    return X, y


def fit_classifier(X, y):
    classifier = DecisionTreeClassifier()
    classifier.fit(X, y)
    return classifier


def get_set_of_labels(dhcp_records):
    labels = []
    for rec in dhcp_records:
        labels += add_catagory(filter_labels(sanitize_string_vci(rec.hostname)), 'hostname')
        labels += add_catagory(filter_labels(sanitize_string_vci(rec.vendor_class)), 'vci')
        labels += add_catagory(sanitize_string(rec.req_lst), 'prl')
        labels += add_catagory(sanitize_string(rec.mds), 'mds')
        labels += add_catagory(sanitize_string(rec.msg_t), 'msg_t')

    labels = list(set(labels))
    labels.sort()
    print labels
    return labels


def train(oracle, dhcp_fdb):
    dtl = DeviceTagsLoader(oracle)
    oracle = dtl.devs
    dhcp_reader = DBReader(dhcp_fdb, DHCPRecord())
    dhcp_records = dhcp_reader.read()
    labels = get_set_of_labels(dhcp_records)
    enc = init_enc(labels)
    X, y = prepare_tagged(dhcp_records, oracle, enc)
    classi = fit_classifier(X, y)
    print "trained"
    return labels, enc, classi


def perform_testing(oracle, dhcp_fdb, enc, classifier):
    dtl = DeviceTagsLoader(oracle)
    oracle = dtl.devs
    dhcp_reader = DBReader(dhcp_fdb, DHCPRecord())
    dhcp_records = dhcp_reader.read()
    tn, fp, fn, tp = 0, 0, 0, 0

    for dev in oracle.values():
        #print dev.desc
        X, y = [], []
        dps = get_dev_sw_slots(dhcp_records, dev, 1)
        for dp in dps:
            labels = prepare_vector(dp.hostname, dp.vendor_class, dp.req_lst, dp.mds, dp.msg_t, dp.client_id, enc)
            X.append(labels)
            y.append(int(dev.isiot))
        if len(X) == 0:
            continue
        print dev.desc
        d_tp, d_tn, d_fp, d_fn = perform_testing_per_device(X, y, classifier)
        if not (d_tp == 1 or d_tn == 1):
            print dev.desc
            print d_tp, d_tn, d_fp, d_fn
        tp, tn, fp, fn = tp + d_tp, tn + d_tn, fp + d_fp, fn + d_fn

    print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
    print 'recall', float(tp) / (tp + fn) * 100
    print 'precision', float(tp) / (tp + fp) * 100


def perform_testing_per_device(X, y, classifier):
    y_pred = classifier.predict(X)
    print y[0]
    print classifier.predict_proba(X)
    exit()
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
    tp, tn, fp, fn = tp / all, tn / all, fp / all, fn / all
    return tp, tn, fp, fn


def paint(classifier, labels):
    dot_data = tree.export_graphviz(classifier, out_file=None,
                                    feature_names=labels,
                                    class_names=["NOT", "IOT"],
                                    label='all', rounded=True,
                                    special_characters=True)

    graph = graphviz.Source(dot_data)
    graph.render("find_fp_auto_tree")


def main():
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    labels, enc, classifier = train(SEEN_ORACLE, SEEN_DHCPDB)
    pickle.dump(enc, open("dhcp_enc.bin", "wb"))
    pickle.dump(classifier, open("dhcp_classifier.bin", "wb"))

    paint(classifier, labels)
    perform_testing(UNSEEN_ORACLE, UNSEEN_DHCPDB, enc, classifier)


main()
