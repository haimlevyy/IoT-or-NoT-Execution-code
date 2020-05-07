from itertools import combinations
from main import Activator


FEATURES = ['ethlen',
            'ethsum',
            'ethstd',
            'remote_ip',
            'avg_ttl',
            'tcp_udp_ratio',
            'ports',
            'tcpts',
            'max_winds',
            'udns',
            'dns',
            'avg_ua']


def real_greedy_test(features, act, sw, last):
    combs = []
    for fea in features:
        if fea in last:
            continue
        combs.append(last + [fea])
    db = []
    for comb in combs:
        val = act.make_avg(sw, comb)
        print "GRGRGRG", sw, comb, val
        db.append((comb, val))
    comb, score = max(db, key=lambda t: t[1])
    scores = act.get_all_scores(sw, comb)
    return comb, score, scores


def exhaustive_test(features, num, act, sw):
    combs = combinations(features, num)
    db = []
    for comb in combs:
        val = act.make_avg(sw, comb)
        #print sw, comb, val
        db.append((comb, val))
    comb, score = max(db, key=lambda t: t[1])
    scores = act.get_all_scores(sw, comb)
    return comb, score, scores


def run_feature_test_sw(features, act, sw, thresh=6):
    print 'For:', sw
    scores = []
    last = 0
    for i in xrange(thresh):
        # comb, score, sc = real_greedy_test(features, act, sw, last)
        print 'For:', i+1, 'features'
        comb, score, sc = exhaustive_test(features, i + 1, act, sw)
        scores.append(sc)
        print "final", comb, '-', score
        if last >= score[0]:
            break
        last = score[0]


def features_test():
    print 'started'
    features = FEATURES
    sws = [60, 300, 600, 1200]
    act = Activator(r'C:\Users\Haim\Desktop\thesis\13022020 - new tasks after meeting\brand new world\features2folders\seen_folds\\', None, True)
    for sw in sws:
        run_feature_test_sw(features, act, sw, 5)


features_test()



