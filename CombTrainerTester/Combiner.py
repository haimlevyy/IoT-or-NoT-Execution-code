from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from base_libs.DeviceTagsLoader import DeviceTagsLoader
from CombTrainerTester.base_libs.FolderLoader import *
from Base import *


class Combiner(object):
    def __init__(self):
        self.classifier = LogisticRegression()
        self.train_X = None
        self.train_y = None
        self.scaler = None
        self.fixes = None

    def fit(self, train_qt, train_qd, train_y):
        self._trim_features(train_qt, train_qd, train_y)
        self.classifier.fit(self.train_X, self.train_y)

    def classify(self, test_qt, test_qd, test_y, label):
        test_x = np.array([test_qt, test_qd]).T
        test_x = handle_test_nans(test_x, self.fixes)
        test_x = self.scaler.transform(test_x)

        tp, tn, fp, fn = 0, 0, 0, 0
        if len(test_x) == 0:
            print "no test features;"
            return

        _, probas, tp, tn, fp, fn = self._do_classify_dev("", test_x, test_y)
        f1score = float(2 * tp) / (2 * tp + fn + fp) * 100
        print "------------------------------------------------"
        print "Combiner for:", label
        print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        print 'recall', float(tp) / (tp + fn) * 100
        print 'precision', float(tp) / (tp + fp) * 100
        return f1score

    def _do_classify_dev(self, ky, x, y):
        y_pred = self.classifier.predict(x)
        y_proba = self.classifier.predict_proba(x)
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
        tp, tn, fp, fn = tp/all, tn/all, fp/all, fn/all

        return ky, y_proba, tp, tn, fp, fn

    def _trim_features(self, train_qt, train_qd, train_y):
        train_x = np.vstack([train_qt, train_qd]).T
        self.train_y = train_y

        self.train_X, _, self.fixes = handle_nan(train_x, self.train_y, [], True)
        self.scaler = StandardScaler()
        self.scaler.fit(self.train_X)
        self.train_X = self.scaler.transform(self.train_X)
        return


