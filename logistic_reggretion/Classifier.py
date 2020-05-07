__author__ = 'haim.levy@post.idc.ac.il'

from sklearn.metrics import confusion_matrix  #, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.svm import SVC

from FolderLoader import *
from Base import *


class Classifier(object):
    def __init__(self, fold_path, PREPATH):
        fold_reader = FolderLoader(fold_path)
        self.fold = fold_reader.load_fold()

        self.train_X = None
        self.test_X = None
        self.train_y = None
        self.test_y = None
        self.scalar = None

    def classify(self, sw, features):
        self._trim_features(sw, features)
        scores = [
                    self._do_classify(LogisticRegression(), sw, features),
                    #self._do_classify(DecisionTreeClassifier()),
                    #self._do_classify(RandomForestRegressor()),
                    #self._do_classify(SVC(kernel='rbf', probability=True)),
                    #self._do_classify(SVC(kernel='linear', probability=True)),
                    #self._do_classify(SVC(kernel='poly', probability=True)),
                    #self._do_classify(SVC(kernel='sigmoid', probability=True)),
        ]
        return scores

    def _do_classify(self, classifier, sw, fea):
        classifier.fit(self.train_X, self.train_y)
        score = classifier.score(self.test_X, self.test_y)
        y_pred = classifier.predict(self.test_X)

        tn, fp, fn, tp = confusion_matrix(self.test_y, y_pred).ravel()

        if True:
            print "sw", sw
            print "classifier.coef_", classifier.coef_
            print "classifier.intercept_", classifier.intercept_

        if False and sw == 600:
            print "printing debug data:"
            print "self.train_X", "self.train_y"
            for i in xrange(len(self.train_y)):
                print self.train_X[i], self.train_y[i]
            print "self.test_X", "self.test_y", "y_pred"
            for i in xrange(len(self.test_y)):
                print self.test_X[i], self.test_y[i], y_pred[i]
            print "classifier.coef_", classifier.coef_
            print "classifier.intercept_", classifier.intercept_
            print "self.scalar.mean_", self.scalar.mean_
            print "self.scalar.scale_", self.scalar.scale_

        # print '-', 1, 0
        # print 1, tp, fp
        # print 0, fn, tn
        # print ''
        # print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
        # print 'sens', float(tp) / (tp + fn) * 100
        # print 'spec', float(tn) / (tn + fp) * 100
        # print 'precision', float(tp) / (tp + fp) * 100
        # print ''
        # print ''
        # print_map(classifier, self.scalar, self.test_X, self.test_y, sw, fea)

        if False and type(classifier) is LogisticRegression:
            y_pred = classifier.predict(self.test_X)
            proba = classifier.predict_proba(self.test_X)[:, 1]
            print 'classifier debug;'
            for i in xrange(len(y_pred)):
                print self.test_y[i], y_pred[i], proba[i]

        return score

    def _trim_features(self, sw, features):
        iotf, notf = self.fold.train.trim_features(sw, features)
        train_X = notf + iotf
        self.train_y = [0] * len(notf) + [1] * len(iotf)

        t_iotf, t_notf = self.fold.test.trim_features(sw, features)
        test_X = t_notf + t_iotf
        self.test_y = [0] * len(t_notf) + [1] * len(t_iotf)

        self.train_X, self.test_X, _ = handle_nan(train_X, self.train_y, test_X)

        self.scalar = StandardScaler()
        self.scalar.fit(self.train_X)
        self.train_X = self.scalar.transform(self.train_X)
        self.test_X = self.scalar.transform(self.test_X)
        return
