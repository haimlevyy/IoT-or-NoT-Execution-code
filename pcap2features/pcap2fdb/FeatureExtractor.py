from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Ether
from scapy.all import *

from Base import *


class FeatureExtractor(object):
    def __init__(self):
        self.devs_fea = {}

    def process(self, devs, cache):
        self.devs_fea = DevFeatures.copy_from_devdata(devs)
        for ts, pack in cache:
            if Ether not in pack:
                continue
            mc = pack[Ether].src
            if mc not in devs.keys():
                continue
            self.devs_fea[mc].eth += 1
            self._collect_ip(mc, pack)
            self._collect_tcpts(mc, ts, pack)
            self._collect_winds(mc, pack)
            self._collect_dns(mc, pack)
            self._collect_ua(mc, pack)
        return self.devs_fea

    def extract_feas(self, devs_fea, ts, pack):
        self.devs_fea = devs_fea
        if Ether not in pack:
            return self.devs_fea
        mc = pack[Ether].src
        if mc not in self.devs_fea.keys():
            return self.devs_fea
        self.devs_fea[mc].eth += 1
        self._collect_ethlen(mc, pack)
        self._collect_eth_ts(mc, pack, ts)
        self._collect_ip(mc, pack)
        self._collect_ttl(mc, pack)
        self._collect_ports(mc, pack)
        self._collect_tcpts(mc, ts, pack)
        self._collect_winds(mc, pack)
        self._collect_dns(mc, pack)
        self._collect_ua(mc, pack)
        return self.devs_fea

    def _collect_eth_ts(self, mac, pack, ts):
        if Ether not in pack:
            return
        self.devs_fea[mac].eth_ts.append(ts)

    def _collect_ethlen(self, mac, pack):
        if Ether not in pack:
            return
        self.devs_fea[mac].ethlen.append(len(pack))

    def _collect_ip(self, mac, pack):
        if IP not in pack:
            return
        self.devs_fea[mac].remote_ip.append(pack[IP].dst)
        return

    def _collect_ttl(self, mac, pack):
        if IP not in pack:
            return
        self.devs_fea[mac].ttl.append(pack[IP].ttl)
        return

    def _collect_ports(self, mac, pack):
        if IP not in pack:
            return
        dport = None
        if TCP in pack:
            dport = 'T' + str(pack[TCP].dport)
        if UDP in pack:
            dport = 'U' + str(pack[UDP].dport)
        if dport is not None:
            self.devs_fea[mac].ports.append(dport)
        return

    def _collect_tcpts(self, mac, ts, pack):
        if TCP not in pack:
            return
        timestamp = None
        for opt in pack[TCP].options:
            if type(opt[0]) is not str:
                continue
            if opt[0].lower() == 'timestamp':
                timestamp = opt[1][0]
        if timestamp is None:
            return
        self.devs_fea[mac].tcpts.append((ts, timestamp))
        return

    def _collect_winds(self, mac, pack):
        if TCP not in pack:
            return
        wind = pack[TCP].window
        self.devs_fea[mac].winds.append(wind)
        return

    def _collect_dns(self, mac, pack):
        if UDP not in pack:
            return
        if pack[UDP].dport != 53:
            return
        if DNS not in pack:
            return
        dom = None
        try:
            dom = sanitize_domain(str(pack[DNS].qd.qname), 3)
        except:
            print 'dns no dom :('
        if dom is not None:
            self.devs_fea[mac].dns.append(dom)
        return

    def _collect_ua(self, mac, pack):
        if TCP not in pack:
            return
        payload = str(pack[TCP].payload)
        ua = get_ua(payload)
        if ua is None:
            return
        self.devs_fea[mac].ua.append(len(ua))
