__author__ = 'haim.levy@post.idc.ac.il'
# Purpose:
#
# Read two types of files:
# - a pcap contains communication of IOT/NOT
# - a txt/csv file that contains tagging to the device's MAC (isiot & desc, for debugging)

from DeviceTagsLoader import DeviceTagsLoader
from PcapIO import *


class Activator(object):
    def __init__(self, pcaps, oracle_file, outfile):
        dtl = DeviceTagsLoader(oracle_file)
        oracle = dtl.devs
        writer = LogWriter(outfile, oracle)
        self.pcaps = pcaps

        slot_60 = SlotCache(60, oracle, writer)
        slot_120 = SlotCache(120, oracle, writer)
        slot_180 = SlotCache(180, oracle, writer)
        slot_240 = SlotCache(240, oracle, writer)
        slot_300 = SlotCache(300, oracle, writer)
        slot_600 = SlotCache(600, oracle, writer)
        slot_1200 = SlotCache(1200, oracle, writer)

        self.pcap_reader = PcapReader(self.pcaps[0])
        self.pcap_reader.add_cacher(slot_60)
        self.pcap_reader.add_cacher(slot_120)
        self.pcap_reader.add_cacher(slot_180)
        self.pcap_reader.add_cacher(slot_240)
        self.pcap_reader.add_cacher(slot_300)
        self.pcap_reader.add_cacher(slot_600)
        self.pcap_reader.add_cacher(slot_1200)

    def process(self):
        print 'reading:', self.pcaps[0]
        self.pcap_reader.read()
        for pc in self.pcaps[1:]:
            self.pcap_reader.load_pcap(pc)
            print 'reading:', pc
            self.pcap_reader.read()


def pcap2fdb(pcaps, oracle, outfile):
    act = Activator(pcaps, oracle, outfile)
    act.process()


if '__main__' == __name__:
    pass #logreg_classifier()
