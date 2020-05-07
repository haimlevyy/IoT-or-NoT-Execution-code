from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether
from scapy.all import *

from Base import *


class FeatureExtractor(object):
    def __init__(self):
        self.devs_fea = {}

    def extract_feas(self, devs_fea, ts, pack):
        self.devs_fea = devs_fea
        if Ether not in pack:
            return self.devs_fea
        mc = pack[Ether].src
        if mc not in self.devs_fea.keys():
            return self.devs_fea
        self.devs_fea[mc].eth += 1
        self._collect_dhcp(mc, pack)
        return self.devs_fea

    def _collect_dhcp(self, mac, pack):
        if IP not in pack:
            return
        if DHCP not in pack:
            return
        opts = pack[DHCP].options
        vci = None
        hn = None
        req_lst = []
        mds = 'None'
        msg_t = 'None'
        client_id = 'None'
        for i in opts:
            if type(i) is not tuple:
                continue
            if len(i) <= 1:
                continue
            try:
                if i[0].lower() == 'vendor_class_id':
                    vci = i[1]
                if i[0].lower() == 'hostname':
                    hn = i[1]
                if i[0].lower() == 'param_req_list':
                    req_lst = i[1]
                if i[0].lower() == 'max_dhcp_size':
                    mds = str(i[1])
                if i[0].lower() == 'message-type':
                    msg_t = str(i[1])
                if i[0].lower() == 'client_id':
                    client_id = str(i[1])
            except:
                pass
                # print "Error; i=", i
        if hn is not None:
            self.devs_fea[mac].hostname.append(hn)
            if vci is None:
                self.devs_fea[mac].vendor_class.append('None')
            if not req_lst:
                self.devs_fea[mac].req_lst.append('None')

        if req_lst:
            self.devs_fea[mac].req_lst += req_lst
            if vci is None:
                self.devs_fea[mac].vendor_class.append('None')
            if hn is None:
                self.devs_fea[mac].hostname.append('None')

        if vci is not None:
            self.devs_fea[mac].vendor_class.append(vci)
            if hn is None:
                self.devs_fea[mac].hostname.append('None')
            if not req_lst:
                self.devs_fea[mac].req_lst.append('None')

        self.devs_fea[mac].mds.append(mds)
        self.devs_fea[mac].msg_t.append(msg_t)
        self.devs_fea[mac].client_id.append(client_id)

        return
