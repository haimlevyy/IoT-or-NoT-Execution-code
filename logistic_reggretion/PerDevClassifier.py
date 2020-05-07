__author__ = 'haim.levy@post.idc.ac.il'

from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import pickle
from FolderLoader import *
from Base import *


class PerDevClassifier(object):
    def __init__(self, fold_path, PRE_NAME):
        fold_reader = FolderLoader(fold_path)
        self.fold = fold_reader.load_fold(is_lst=False)

        self.train_X = None
        self.test_X = None
        self.train_y = None
        self.test_y = None
        self.scaler = None

        self.PRE_NAME = PRE_NAME

    def classify(self, sw, features):
        self._trim_features(sw, features)
        scores = [
            self._do_classify(LogisticRegression(), sw, features, self.PRE_NAME),
            # self._do_classify(DecisionTreeClassifier()),
            # self._do_classify(RandomForestRegressor()),
            # self._do_classify(SVC(kernel='rbf', probability=True)),
            # self._do_classify(SVC(kernel='linear', probability=True)),
            # self._do_classify(SVC(kernel='poly', probability=True)),
            # self._do_classify(SVC(kernel='sigmoid', probability=True)),
        ]
        return scores

    def _do_classify(self, classifier, sw, fea, PRE_NAME):
        tp, tn, fp, fn = 0, 0, 0, 0
        classifier.fit(self.train_X, self.train_y)
        pickle.dump(classifier, open(str(sw) + "_classifier.bin", "wb"))
        for k in self.test_X.keys():
            if len(self.test_X[k]) == 0:
                continue
            _, d_tp, d_tn, d_fp, d_fn = self._do_classify_dev(classifier, k, sw, fea, PRE_NAME)
            tp, tn, fp, fn = tp + d_tp, tn + d_tn, fp + d_fp, fn + d_fn
        f1score = float(2 * tp) / (2 * tp + fn + fp) * 100
        #print 'sw:', sw
        #print '-', 1, 0
        #print 1, tp, fp
        #print 0, fn, tn
        #print ''
        #print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        #print 'sens', float(tp) / (tp + fn) * 100
        #print 'spec', float(tn) / (tn + fp) * 100
        #print 'precision', float(tp) / (tp + fp) * 100
        #print ''
        #print ''

        return f1score

    def _do_classify_dev(self, classifier, ky, sw, fea, PRE_NAME):
        y_pred = classifier.predict(self.test_X[ky])
        y_proba = classifier.predict_proba(self.test_X[ky])

        tn, fp, fn, tp = 0, 0, 0, 0
        resu = confusion_matrix(self.test_y[ky], y_pred).ravel()

        if len(resu) == 1:
            if self.test_y[ky][0] == 0:
                tn = resu[0]
            else:
                tp = resu[0]
        else:
            tn, fp, fn, tp = resu

        all = float(tp + fp + tn + fn)
        tp, tn, fp, fn = tp/all, tn/all, fp/all, fn/all

        #print ''
        #print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        #print 'sens', float(tp) / (tp + fn) * 100
        #print 'spec', float(tn) / (tn + fp) * 100
        #print 'precision', float(tp) / (tp + fp) * 100
        #print ''
        #print ''
        return '', tp, tn, fp, fn

    def _trim_features(self, sw, features):
        iotf, notf = self.fold.train.trim_features(sw, features)
        train_X = notf + iotf
        self.train_y = [0] * len(notf) + [1] * len(iotf)

        t_iotf, t_notf = self.fold.test.trim_features(sw, features)
        test_X = t_notf.copy()
        test_X.update(t_iotf)

        self.test_y = {}
        for k, v in t_notf.items():
            self.test_y[k] = [0] * len(v)
        for k, v in t_iotf.items():
            self.test_y[k] = [1] * len(v)

        self.train_X, self.test_X, fixes = handle_nan(train_X, self.train_y, test_X, False)
        pickle.dump(fixes, open(str(sw) + "_fixes.bin", "wb"))
        self.scaler = StandardScaler()
        self.scaler.fit(self.train_X)
        pickle.dump(self.scaler, open(str(sw) + "_scaler.bin", "wb"))
        self.train_X = self.scaler.transform(self.train_X)
        for k in self.test_X.keys():
            if len(self.test_X[k]) == 0:
                continue
            self.test_X[k] = self.scaler.transform(self.test_X[k])
        return
