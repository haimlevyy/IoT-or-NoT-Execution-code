import pcapy
from scapy.layers.l2 import Ether

from Base import *
from FeatureExtractor import FeatureExtractor


class PcapReader(object):
    def __init__(self, pcapfile, bpf=None):
        self._cachers = []
        self._pcapfile_name = pcapfile
        self._pc = pcapy.open_offline(pcapfile)
        self._bpf = bpf
        if bpf is not None:
            self._pc.setfilter(bpf)

    def read(self):
        packet_index = 0
        while True:
            try:
                (header, pack) = self._pc.next()
                if header is None or pack is None:
                    break
                ts = (header.getts()[0] * 10 ** 6 + header.getts()[1]) / 10. ** 6
                packet_index += 1

                pack = Ether(pack)
                for sc in self._cachers:
                    sc.add(ts, pack)

                if packet_index % 10000 == 0:
                    print packet_index

            except pcapy.PcapError:
                break
        return

    def load_pcap(self, pcap, bpf=None):
        self._pc = pcapy.open_offline(pcap)
        self._bpf = bpf
        if bpf is not None:
            self._pc.setfilter(bpf)
        elif self._bpf is not None:
            self._pc.setfilter(self._bpf)
        return

    def add_cacher(self, slot_cache):
        if type(slot_cache) is not SlotCache:
            raise RuntimeError('Argument is not a SlotCahce type')
        self._cachers.append(slot_cache)
        return


class SlotCache(object):
    def __init__(self, slot_width, oracle, writer):
        self.sd = slot_width
        self.slot_id = 0
        self._oracle = oracle
        self._dev_fea = DevFeatures.copy_from_devdata(oracle)

        if type(writer) is LogWriter:
            self._writer = writer
        else:
            raise AssertionError('Wrong Writer Type')

    def __del__(self):
        self._writer.log_record(self.slot_id, self.sd, self._dev_fea)

    def add(self, ts, pack):
        if self.slot_id == 0:
            self.slot_id = ts
        if ts > self.slot_id + self.sd or ts < self.slot_id:
            self._writer.log_record(self.slot_id, self.sd, self._dev_fea)  # # call writer
            self.slot_id = ts
            del self._dev_fea
            self._dev_fea = DevFeatures.copy_from_devdata(self._oracle)
            self._dev_fea = FeatureExtractor().extract_feas(self._dev_fea, ts, pack)
            return
        self._dev_fea = FeatureExtractor().extract_feas(self._dev_fea, ts, pack)
        pass


class LogWriter(object):
    def __init__(self, out_file_name, oracle):
        self._oracle = oracle
        self._ofn = out_file_name
        self._fl = open(self._ofn, 'w')
        self._write_header()

    def __del__(self):
        self._fl.close()

    def _write_header(self):
        head = add('slot_id', '')
        head += add('slot_width')
        head += add('mac')
        head += add('desc')
        head += add('isiot')
        head += add('ethlen')
        head += add('ethsum')
        head += add('ethstd')
        head += add('remote_ip')
        head += add('avg_ttl')
        head += add('tcp_udp_ratio')
        head += add('ports')
        head += add('tcpts_skew')
        head += add('max_winds')
        head += add('udns')
        head += add('dns')
        head += add('avg_ua') + '\n'
        self._fl.write(head)

    def log_record(self, slot_id, slot_width, packs):
        print 'making logs for:', slot_id, 'width:', slot_width
        record = self._make_records(slot_id, slot_width, packs)
        self._fl.write(record)

    def _make_records(self, slot_id, slot_width, devs_fea):
        res = ''
        res += self._compile_records(slot_id, slot_width, devs_fea)
        return res

    @staticmethod
    def _compile_records(slot_id, slot_width, devs_fea):
        res = ''
        for dev in devs_fea.values():
            if dev.eth == 0:
                continue
            res += str(slot_id)
            res += add(slot_width)
            res += add(dev.mac)
            res += add(dev.desc)
            res += add(dev.isiot)
            res += add(dev.eth)
            res += add(sum(dev.ethlen))
            # eth std
            diffs = [dev.eth_ts[i] - dev.eth_ts[i-1] for i in xrange(1, len(dev.eth_ts))]
            res += add(np.nanstd(diffs))

            res += add(len(set(dev.remote_ip)))
            ttlavg = ''
            if len(dev.ttl) > 0:
                ttlavg = float(sum(dev.ttl)) / len(dev.ttl)
            res += add(ttlavg)
            # tcp_udp_ratio
            tcp_num = len(set([p for p in dev.ports if 'T' in p]))
            udp_num = len(set([p for p in dev.ports if 'U' in p]))
            ratio = 0
            if tcp_num + udp_num > 0:
                ratio = float(tcp_num)/(tcp_num + udp_num)
            res += add(ratio)

            res += add(len(set(dev.ports)))
            lls = dev.do_lls()
            if lls is None:
                lls = ''
            res += add(lls)
            winds = ''
            if len(dev.winds) > 0:
                winds = max(dev.winds)
            res += add(winds)
            res += add(len(set(dev.dns)))
            res += add(len(dev.dns))
            ua = ''
            if len(dev.ua) > 0:
                ua = float(sum(dev.ua))/len(dev.ua)
            res += add(ua)
            res += '\n'
        return res





