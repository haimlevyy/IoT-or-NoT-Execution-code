import pcapy
#from scapy.all import *
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
        if bpf is not None:
            self._pc.setfilter(bpf)
            self._bpf = bpf
        elif self._bpf is not None:
            self._pc.setfilter(self._bpf)
        return

    def add_cacher(self, slot_cache):
        if type(slot_cache) is not SlotCache:
            raise RuntimeError('Argument is not a SlotCahce type')
        self._cachers.append(slot_cache)
        return


class SlotCache(object):
    def __init__(self, oracle, writer):
        self.slot_id = 0
        self._oracle = oracle
        self._dev_fea = DevFeatures.copy_from_devdata(oracle)

        if type(writer) is LogWriter:
            self._writer = writer
        else:
            raise AssertionError('Wrong Writer Type')

    def __del__(self):
        self._writer.log_record(self.slot_id, self._dev_fea)
        return

    def add(self, ts, pack):
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
        head += add('dhcp_len')
        head += add('hostname')
        head += add('vendor_class_id')
        head += add('request_params')
        head += add('max_dhcp-size')
        head += add('msg_type')
        head += add('client_id') + '\n'
        self._fl.write(head)

    def log_record(self, slot_id, packs):
        record = self._make_records(slot_id, 0, packs)
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
            if len(dev.hostname) == 0 and len(dev.vendor_class) == 0:
                continue
            res += str(slot_id)
            res += add(slot_width)
            res += add(dev.mac)
            res += add(dev.desc)
            res += add(dev.isiot)
            res += add(dev.eth)
            res += add(format_lst(list(set(dev.hostname))))
            res += add(format_lst(list(set(dev.vendor_class))))
            res += add(format_lst(list(set(dev.req_lst))))
            res += add(format_lst(list(set(dev.mds))))
            res += add(format_lst(list(set(dev.msg_t))))
            res += add(format_lst(list(set(dev.client_id))))

            res += '\n'
        return res





