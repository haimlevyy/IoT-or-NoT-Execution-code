from os import listdir
from os.path import isfile, join

# fold.train.iotf[].max_winds


class FolderLoader(object):
    def __init__(self, folder_path):
        self.path = folder_path

    def load_fold(self, is_lst=True):
        fold = Fold()
        fold.load_fold(self.path, is_lst)
        return fold


class Fold(object):
    def __init__(self):
        self.train = Portion()
        self.test = Portion()

    def load_fold(self, path, is_lst):
        train_dir = path + 'train/'
        test_dir = path + 'test/'

        self.train.load_portion(train_dir, True)
        self.test.load_portion(test_dir, is_lst)


class Portion(object):
    def __init__(self):
        self.notf = None
        self.iotf = None
        self.is_lst = True

    def load_portion(self, path, is_lst):
        self.is_lst = is_lst

        iot_dir = path + 'IOT/'
        not_dir = path + 'NOT/'

        iotfiles = [iot_dir + f for f in listdir(iot_dir) if isfile(join(iot_dir, f))]
        notfiles = [not_dir + f for f in listdir(not_dir) if isfile(join(not_dir, f))]

        if is_lst:
            self.iotf = self._load_features_lst(iotfiles)
            self.notf = self._load_features_lst(notfiles)
        else:
            self.iotf = self._load_features_dict(iotfiles)
            self.notf = self._load_features_dict(notfiles)

    @staticmethod
    def _load_features_lst(files):
        lst = []
        for fn in files:
            fl = open(fn, 'r')
            data = fl.read()
            fl.close()
            lines = data.split('\n')
            for ln in lines:
                if len(ln.split(',')) < 11:
                    continue
                lst.append(Feature(ln))
        return lst

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
                if len(ln.split(',')) != 14:
                    continue
                dct[fn].append(Feature(ln))
        return dct

    def trim_features(self, sw, features):
        if self.is_lst:
            return self.trim_features_lst(sw, features)
        else:
            return self.trim_features_dict(sw, features)

    def trim_features_lst(self, sw, features):
        iotf = []
        for f in self.iotf:
            if f.sw != sw:
                continue
            iotf.append(f.trim_features(features))
        notf = []
        for f in self.notf:
            if f.sw != sw:
                continue
            notf.append(f.trim_features(features))
        return iotf, notf

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

    def to_string(self):
        return str(self.sw) + ', ' + str(self.ethlen) + ', ' + str(self.ethsum) + ', ' + str(self.ethstd) + ', ' + str(self.remote_ip) + ', ' + str(self.avg_ttl) + ', ' + str(self.tcp_udp_ratio) + ', ' + str(self.ports) + ', ' + str(self.tcpts) + ', ' + str(self.max_winds) + ', ' + str(self.udns) + ', ' + str(self.dns) + ', ' + str(self.avg_ua)

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
        #print 'features vector:' + prt
        return res
