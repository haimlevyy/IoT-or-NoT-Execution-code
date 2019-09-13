from os import listdir
from os.path import isfile, join
import numpy as np
import math


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


class DevData(object):
    def __init__(self, mac, desc, isiot):
        self.mac = mac
        self.desc = desc
        self.isiot = int(isiot)


class Feature(object):
    def __init__(self, ln):
        splt = ln.split(',')
        self.sw = int(splt[0])
        self.slot_id = float(splt[1])
        self.ethlen = float(splt[2])
        self.ethsum = float(splt[3])
        self.ethstd = float(splt[4])
        self.remote_ip = float(splt[5])
        self.avg_ttl = float(splt[6])
        self.tcp_udp_ratio = float(splt[7])
        self.ports = float(splt[8])
        self.tcpts = float(splt[9])
        self.max_winds = float(splt[10])
        self.udns = float(splt[11])
        self.dns = float(splt[12])
        self.avg_ua = float(splt[13])

    def trim_features(self, features):
        res = []
        prt = ''
        if 'max_winds' in features:
            res.append(self.max_winds)
            prt += "max_winds "
        if 'ethlen' in features:
            prt += "ethlen "
            res.append(self.ethlen)
        if 'ethsum' in features:
            prt += "ethsum "
            res.append(self.ethsum)
        if 'ethstd' in features:
            prt += "ethstd "
            res.append(self.ethstd)
        if 'remote_ip' in features:
            prt += "remote_ip "
            res.append(self.remote_ip)
        if 'avg_ttl' in features:
            prt += "avg_ttl "
            res.append(self.avg_ttl)
        if 'tcp_udp_ratio' in features:
            prt += "tcp_udp_ratio "
            res.append(self.tcp_udp_ratio)
        if 'ports' in features:
            prt += "ports "
            res.append(self.ports)
        if 'tcpts' in features:
            prt += "tcpts "
            res.append(self.tcpts)
        if 'udns' in features:
            prt += "udns "
            res.append(self.udns)
        if 'dns' in features:
            prt += "dns "
            res.append(self.dns)
        if 'avg_ua' in features:
            prt += "avg_ua "
            res.append(self.avg_ua)
        return res

    def to_string(self):
        return str(self.sw) + ', ' + str(self.ethlen) + ', ' + str(self.ethsum) + ', ' + str(self.ethstd) + ', ' + str(self.remote_ip) + ', ' + str(self.avg_ttl) + ', ' + str(self.tcp_udp_ratio) + ', ' + str(self.ports) + ', ' + str(self.tcpts) + ', ' + str(self.max_winds) + ', ' + str(self.udns) + ', ' + str(self.dns) + ', ' + str(self.avg_ua)


class DeviceBase(object):
    def __init__(self, path):
        self.notf = None
        self.iotf = None
        self.load_base(path)

    def load_base(self, path):

        iot_dir = path + 'IOT/'
        not_dir = path + 'NOT/'

        iotfiles = [iot_dir + f for f in listdir(iot_dir) if isfile(join(iot_dir, f))]
        notfiles = [not_dir + f for f in listdir(not_dir) if isfile(join(not_dir, f))]

        self.iotf = self._load_features_dict(iotfiles)
        self.notf = self._load_features_dict(notfiles)

    @staticmethod
    def _load_features_dict(files):
        dct = {}
        for fn in files:
            fl = open(fn, 'r')
            data = fl.read()
            fl.close()
            lines = data.split('\n')
            if len(lines) <= 1:
                print "filtered:", fn
                continue
            dct[fn] = []
            for ln in lines:
                if len(ln.split(',')) < 11:
                    continue
                dct[fn].append(Feature(ln))
        return dct

    def trim_features(self, sw, features):
        return self.trim_features_dict(sw, features)

    def trim_features_dict(self, sw, features):
        iotf = {}
        for k, v in self.iotf.items():
            iotf[k] = []
            for f in v:
                if f.sw != sw:
                    continue
                iotf[k].append(f.trim_features(features))
        notf = {}
        for k, v in self.notf.items():
            notf[k] = []
            for f in v:
                if f.sw != sw:
                    continue
                notf[k].append(f.trim_features(features))
        return iotf, notf
