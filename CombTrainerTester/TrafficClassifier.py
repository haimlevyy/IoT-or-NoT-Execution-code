from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from base_libs.DeviceTagsLoader import DeviceTagsLoader

from CombTrainerTester.base_libs.FolderLoader import *
from Base import *
import matplotlib
matplotlib.rcParams.update({'font.size': 22})


class TrafficClassifier(object):
    def __init__(self, train_path, test_path):
        fold_reader = FolderLoader(train_path, test_path)
        self.fold = fold_reader.load_fold(is_lst=False)
        self.classifier = LogisticRegression()
        self.train_X = None
        self.test_X = None
        self.train_y = None
        self.test_y = None
        self.scaler = None
        self.fixes = None

    def get_dev_sids(self, mac, sw):
        features = self.fold.get_dev_features(mac)
        sids = []
        for f in features:
            if f.sw == sw:
                sids.append(f.slot_id)
        return sids

    def fit(self, sw, features):
        self._trim_features(sw, features)
        self.classifier.fit(self.train_X, self.train_y)

    def classify_test_folder(self, label):
        tp, tn, fp, fn = 0, 0, 0, 0
        probas = {}
        for k in self.test_X.keys():
            if len(self.test_X[k]) == 0:
                probas[k] = np.array([np.nan])
                continue
            _, probas[k], d_tp, d_tn, d_fp, d_fn = self._do_classify_dev(k, self.test_X[k], self.test_y[k])
            tp, tn, fp, fn = tp + d_tp, tn + d_tn, fp + d_fp, fn + d_fn
        f1score = float(2 * tp) / (2 * tp + fn + fp) * 100
        print "------------------------------------------------"
        print 'Traffic for label:', label
        print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        print 'recall', float(tp) / (tp + fn) * 100
        print 'precision', float(tp) / (tp + fp) * 100
        return probas

    def _do_classify_dev(self, ky, x, y):
        y_pred = self.classifier.predict(x)
        y_proba = self.classifier.predict_proba(x)[:, 1]
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

        self.train_X, self.test_X, self.fixes = handle_nan(train_X, self.train_y, test_X, False)
        self.scaler = StandardScaler()
        self.scaler.fit(self.train_X)
        self.train_X = self.scaler.transform(self.train_X)
        for k in self.test_X.keys():
            if len(self.test_X[k]) == 0:
                continue
            self.test_X[k] = self.scaler.transform(self.test_X[k])
        return
