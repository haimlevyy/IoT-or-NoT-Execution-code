import math
import numpy as np
from Base import *


class Saver(object):
    def __init__(self, pre_path, records, oracle):
        self.records = records
        self.oracle = oracle
        create_folder(pre_path + './IOT/')
        create_folder(pre_path + './NOT/')

    def print_50perc_features(self):
        sws = list(set([t.slot_width for t in self.records]))
        for sw in sws:
            records = [t for t in self.records if t.slot_width == sw]
            print sw, len(records)
            self._print_50_by_sw(records, sw)

    def _print_50_by_sw(self, records, sw):
        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.ethlen for t in records if t.mac == dev.mac]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_ethlen', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.ethsum for t in records if t.mac == dev.mac]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_ethsum', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.remote_ip for t in records if t.mac == dev.mac and type(t.remote_ip) is int]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_remote_ip', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.avg_ttl for t in records if t.mac == dev.mac and type(t.avg_ttl) is float and not math.isnan(float(t.avg_ttl))]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_avg_ttl', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.ports for t in records if t.mac == dev.mac and type(t.ports) is int]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_ports', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.tcpts for t in records if t.mac == dev.mac and type(t.tcpts) is float and not math.isnan(float(t.tcpts))]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_tcpts', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.max_winds for t in records if t.mac == dev.mac and type(t.max_winds) is int]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_max_winds', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.udns for t in records if t.mac == dev.mac and type(t.udns) is int]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_udns', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.dns for t in records if t.mac == dev.mac and type(t.dns) is int]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_dns', self.oracle, pams50, sw)

        pams50 = {}
        for dev in self.oracle.values():
            tmp = [t.avg_ua for t in records if t.mac == dev.mac and type(t.avg_ua) is float and not math.isnan(float(t.avg_ua))]
            if len(tmp) == 0:
                continue
            pams50[dev.mac] = np.percentile(tmp, 50)
        generic_print('50_avg_ua', self.oracle, pams50, sw)

    def print_touples(self, pre_path, samples=True):
        sws = sorted(list(set([t.slot_width for t in self.records])))
        for dev in self.oracle.values():
            records = [t for t in self.records if t.mac == dev.mac]
            self._print_toup_by_dev(pre_path, records, dev, sws, samples)

    def _print_toup_by_dev(self, pre_path, records, dev, sws, samples):
        fn = get_dev_file_name(pre_path, dev)
        fl = open(fn, 'a')
        for sw in sws:
            recs = [t for t in records if t.slot_width == sw and t.ethlen >= 10]
            self._print_toup_by_dev_sw(recs, sw, fl, dev, samples)
        fl.close()

    def _print_toup_by_dev_sw(self, records, sw, fl, dev, samples):
        num = 3
        if sw <= 600:
            num = 4
        if samples:
            records = self._find_dev_instances(records, dev, num)
        for rec in records:
            record  = add(sw, '')
            record += add(rec.slot_id)
            record += add(rec.ethlen)
            record += add(rec.ethsum)
            record += add(rec.ethstd)
            record += add(rec.remote_ip)
            record += add(rec.avg_ttl)
            record += add(rec.tcp_udp_ratio)
            record += add(rec.ports)
            record += add(rec.tcpts)
            record += add(rec.max_winds)
            record += add(rec.udns)
            record += add(rec.dns)
            record += add(rec.avg_ua)
            fl.write(record + '\n')

    @staticmethod
    def _find_dev_instances(records, dev, num=5):
        res = []
        if len(records) < num:
            msg = 'Yo doug!'
            msg += add(dev.mac)
            msg += add(dev.desc)
            if len(records) > 0:
                msg += add(records[0].slot_width)
            msg += add(len(records))
            print (msg)
            return []

        records = sorted(records, key=lambda t: t.ethsum)
        ln = len(records)
        if ln == num:
            res = records
            return res

        divider = num
        offset = 0
        if ln >= num + 2:
            divider += 2
            offset = 1
        diff = float(ln - 1) / (divider - 1)
        i = 0.0
        for _ in xrange(num):
            res.append(records[int(round((offset * diff) + i))])
            i += diff
        return res


def generic_print(name, devs, pams, slot_width):
    fea_name = make_fn_vars(name, slot_width)
    for dev in devs.values():
        if dev.mac not in pams.keys():
            continue
        feature = pams[dev.mac]
        fn = get_dev_file_name(dev)
        data = fea_name + '\n' + str(feature) + '\n'
        save_file(fn, data, 'a')
