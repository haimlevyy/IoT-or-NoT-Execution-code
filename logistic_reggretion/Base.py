import numpy as np
import math


def handle_nan(train_features, y_train, test_features, is_lst=True):
    iot_train = []
    not_train = []
    for i in xrange(len(train_features)):
        if y_train[i] == 1:  # iot
            iot_train.append(train_features[i])
        else:
            not_train.append(train_features[i])

    #_, fixes = handle_train_nans(iot_train + not_train)

    iot_train, i_fixes = handle_train_nans(iot_train)
    not_train, n_fixes = handle_train_nans(not_train)
    fixes = []
    for i in xrange(len(i_fixes)):
        fixes.append(np.mean([i_fixes[i], n_fixes[i]]))
    #print fixes

    if is_lst:
        test_features = handle_test_nans(test_features, fixes)
    else:
        for k in test_features.keys():
            test_features[k] = handle_test_nans(test_features[k], fixes)

    train_features = np.asarray(list(not_train) + list(iot_train))
    return train_features, test_features, fixes


def handle_test_nans(features, fixes):
    res = []
    features = np.asarray(features).T
    i = 0
    for fset in features:
        nfset = []
        for f in fset:
            if math.isnan(f) or np.isnan(f):
                f = fixes[i]
            nfset.append(f)
        i += 1
        res.append(nfset)
    res = np.asarray(res).T
    return res


def handle_train_nans(features):
    res = []
    fixes = []
    features = np.asarray(features).T
    for fset in features:
        curr_fix = np.median([t for t in fset if not (math.isnan(t) or np.isnan(t))])
        fixes.append(curr_fix)
        nfset = []
        for f in fset:
            if math.isnan(f) or np.isnan(f):
                f = curr_fix
            nfset.append(f)
        res.append(nfset)
    res = np.asarray(res).T
    return res, fixes


class DevData(object):
    def __init__(self, mac, desc, isiot):
        self.mac = mac
        self.desc = desc
        self.isiot = int(isiot)
