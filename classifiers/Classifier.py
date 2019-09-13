__author__ = 'haim.levy@post.idc.ac.il'

from sklearn.metrics import confusion_matrix
import base_libs.Base
from base_libs.Base import *

import pickle

SET_TMP_FILE = "_sets_tmp.csv"
fl = open(SET_TMP_FILE, "w")
fl.close()


class LogRegClassifier(object):
    def __init__(self, test_path):
        self.database = DeviceBase(test_path)
        self.dict = {}
        self.test_X = None
        self.test_y = None
        self.scaler = None

    def classify(self, sw, features):
        tp, tn, fp, fn = 0, 0, 0, 0
        self._trim_features(sw, features)
        classifier = pickle.load(open("../dumps/" + str(sw) + "_classifier.bin", "rb"))
        for k in self.test_X.keys():
            d_tp, d_tn, d_fp, d_fn = self._do_classify_dev(classifier, k, sw, features)
            tp, tn, fp, fn = tp + d_tp, tn + d_tn, fp + d_fp, fn + d_fn
        f1score = float(2 * tp) / (2 * tp + fn + fp) * 100
        print '-----------------------------------------------------'
        print 'Total results for slot width of:', sw
        print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        print 'Recall', float(tp) / (tp + fn) * 100
        print 'precision', float(tp) / (tp + fp) * 100
        print '-----------------------------------------------------'

        return f1score, self.dict

    def _do_classify_dev(self, classifier, ky, sw, fea):
        tn, fp, fn, tp = 0, 0, 0, 0
        y_pred = classifier.predict(self.test_X[ky])
        y_proba = classifier.predict_proba(self.test_X[ky])
        resu = confusion_matrix(self.test_y[ky], y_pred).ravel()
        if len(resu) == 1:
            if self.test_y[ky][0] == 0:
                tn = resu[0]
            else:
                tp = resu[0]
        else:
            tn, fp, fn, tp = resu
        
        name = ky.split('/')[-1].split('.txt')[0]
        save_sets(name, sw, self.test_y[ky], y_pred)
        all = float(tp + fp + tn + fn)
        self.dict[ky] = (tp + tn) / all
        tp, tn, fp, fn = tp/all, tn/all, fp/all, fn/all

        nt, it = 0.0, 0.0
        for res in y_proba:
            if res[0] > res[1]:
                nt += 1
            else:
                it += 1
        
        print "Classifying results for device:", name, "sw= " + str(sw),
        print "(NoT, IoT) = " + str(nt/len(y_proba)) + ", " + str(it/len(y_proba))
        return tp, tn, fp, fn

    def _trim_features(self, sw, features):
        t_iotf, t_notf = self.database.trim_features(sw, features)
        test_X = t_notf.copy()
        test_X.update(t_iotf)

        self.test_y = {}
        for k, v in t_notf.items():
            self.test_y[k] = [0] * len(v)
        for k, v in t_iotf.items():
            self.test_y[k] = [1] * len(v)

        fixes = pickle.load(open("../dumps/" + str(sw) + "_fixes.bin", "rb"))
        self.test_X = {}
        for k in test_X.keys():
            self.test_X[k] = handle_test_nans(test_X[k], fixes)
        self.scaler = pickle.load(open("../dumps/" + str(sw) + "_scaler.bin", "rb"))
        for k in self.test_X.keys():
            self.test_X[k] = self.scaler.transform(self.test_X[k])
        return


def save_sets(k, sw, expected_y, predicted_y):

    res = str(k.split('/')[-1])
    res += ',' + str(expected_y[0])
    res += ',' + str(sw)

    for i in xrange(len(predicted_y)):
        if predicted_y[i] == expected_y[i]:
            res += ',1'
        else:
            res += ',0'
    res += '\n'

    fl = open(SET_TMP_FILE, "a")
    fl.write(res)
    fl.close()
    return


def logreg_classifier(folder_path):
    classi = LogRegClassifier(folder_path)
    features = [['max_winds', 'udns', 'tcp_udp_ratio', 'ethlen'],  # 60
                ['max_winds', 'udns'],  # 120
                ['udns', 'max_winds', 'ethstd', 'remote_ip', 'tcp_udp_ratio'],  # 180
                ['udns', 'max_winds', 'remote_ip'],  # 240 #
                ['udns', 'max_winds', 'remote_ip'],  # 300
                ['udns', 'max_winds', 'remote_ip', 'ethstd'],  # 600
                ['udns', 'max_winds', 'remote_ip'],  # 1200
                ]
    sws = [60, 120, 180, 240, 300, 600, 1200]

    dictionaries_lst = []

    for i in xrange(len(sws)):
        f1score, tmp = classi.classify(sws[i], features[i])
        dictionaries_lst.append(tmp)

    return dictionaries_lst