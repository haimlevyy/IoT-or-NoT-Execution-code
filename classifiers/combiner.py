import math


class PredictionSets:
    def __init__(self, name, isiot):
        self.name = name
        self.isiot = isiot
        self.set1 = []
        self.set2 = []
        self.set3 = []
        self.set4 = []
        self.set5 = []
        self.set10 = []
        self.set20 = []


def make_dicts(data):
    devs = {}
    for line in data.split('\n'):
        splt = line.split(',')
        if len(splt) < 3:
            continue
        name = splt[0]
        isiot = int(splt[1])
        sw = splt[2]
        set = splt[3:]
        set = [int(x) for x in set]
        if name not in devs.keys():
            devs[name] = PredictionSets(name, isiot)
        if sw == '60':
            devs[name].set1 = set
        if sw == '120':
            devs[name].set2 = set
        if sw == '180':
            devs[name].set3 = set
        if sw == '240':
            devs[name].set4 = set
        if sw == '300':
            devs[name].set5 = set
        if sw == '600':
            devs[name].set10 = set
        if sw == '1200':
            devs[name].set20 = set

    return devs


def process(devs, dhcp_dict):
    tn, fp, fn, tp = 0, 0, 0, 0
    rp20 = []
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print "Final Classification: (device classification by majority for all slots)"

    for k, dev in devs.items():
        res, tn, fp, fn, tp = ratio_process_20(dev, dhcp_dict, tn, fp, fn, tp)
        rp20.append(res)

    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print 'Total results for combined classification'
    print 'f1-score', float(2 * tp) / (2 * tp + fn + fp) * 100
    print 'recall', float(tp) / (tp + fn) * 100
    print 'precision', float(tp) / (tp + fp) * 100
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"


def avg(lst):
    return float(sum(lst))/len(lst)


def isiot_helper(num_isiot):
    if num_isiot == 0:
        return "NoT"
    else:
        return "IoT"


def ratio_process_20(dev, dhcp_dict, tn, fp, fn, tp):
    # for 20 i have 7, so, at least 4
    res = []
    for i20 in xrange(len(dev.set20)):
        i10 = i20 * 2
        i5 = i20 * 4
        elem = 1

        classi = dev.set20[i20]
        for i in xrange(2):
            if i10 + i < len(dev.set10):
                classi += (dev.set10[i10 + i])
                elem += 1
        for i in xrange(4):
            if i5 + i < len(dev.set5):
                classi += (dev.set5[i5 + i])
                elem += 1

        ## enrich with dhcp;
        dhcp = []
        for k, v in dhcp_dict.items():
            if k.replace(':', '-') in dev.name:
                dhcp = [v]*2
                break
        res.append(float(classi + sum(dhcp)) / (elem + len(dhcp)))

    ratio = []
    for r in res:
        if r >= 0.5:
            ratio.append(1)
        else:
            ratio.append(0)

    avg_res = avg(ratio)
    #print dev.name, avg_res
    if avg_res >= 0.5:
        print dev.name, "classified as:", isiot_helper(dev.isiot)
        if dev.isiot == 1:
            tp += 1
        else:
            tn += 1
    else:
        print dev.name, "classified as:", isiot_helper(1 - dev.isiot)
        if dev.isiot == 1:
            fn += 1
        else:
            fp += 1
    return avg_res, tn, fp, fn, tp


def combiner(dhcp_dict):
    fn = "_sets_tmp.csv"
    fl = open(fn, 'r')
    data = fl.read()
    fl.close()
    devs = make_dicts(data)
    process(devs, dhcp_dict)

