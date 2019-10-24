__author__ = 'haim.levy@post.idc.ac.il'
# Purpose:
#
# Read two types of files:
# - a pcap contains communication of IOT/NOT (.pcap file)
# - a txt/csv file that contains tagging to the device's MAC (isiot & desc, for debugging, 'oracle')
#

from DeviceTagsLoader import DeviceTagsLoader
from PcapIO import *


class Activator(object):
    def __init__(self, pcaps, oracle_file, outfile):
        dtl = DeviceTagsLoader(oracle_file)
        oracle = dtl.devs
        writer = LogWriter(outfile, oracle)
        self.pcaps = pcaps

        slot = SlotCache(oracle, writer, False)
        slot_accu = SlotCache(oracle, writer, True)

        self.pcap_reader = PcapReader(self.pcaps[0], 'udp port 67')
        self.pcap_reader.add_cacher(slot)
        self.pcap_reader.add_cacher(slot_accu)

    def process(self):
        print 'reading:', self.pcaps[0]
        self.pcap_reader.read()
        for pc in self.pcaps[1:]:
            self.pcap_reader.load_pcap(pc)
            print 'reading:', pc
            self.pcap_reader.read()


def dhcp2fdb(pcaps, oracle, out_file):
    act = Activator(pcaps, oracle, out_file)
    act.process()


if '__main__' == __name__:
    pass #main()
