import numpy as np


class DBRecord(object):
    def __init__(self, slot_id, slot_width, mac, desc, isiot, ethlen, ethsum, ethstd, remote_ip, avg_ttl, tcp_udp_ratio, ports, tcpts, max_winds, udns, dns, avg_ua):
        self.slot_id = slot_id
        self.slot_width = slot_width
        self.mac = mac
        self.desc = desc
        self.isiot = isiot
        self.ethlen = ethlen
        self.ethsum = ethsum
        self.ethstd = ethstd
        self.remote_ip = remote_ip
        self.avg_ttl = avg_ttl
        self.tcp_udp_ratio = tcp_udp_ratio
        self.ports = ports
        self.tcpts = tcpts
        self.max_winds = max_winds
        self.udns = udns
        self.dns = dns
        self.avg_ua = avg_ua
        return

    @staticmethod
    def is_valid(ln):
        splt = ln.split(',')
        if len(splt) != 17:
            return False
        try:
            float(splt[0])
            int(splt[1])
            int(splt[4])
            int(splt[5])
            int(splt[6])
            if len(splt[7]) > 0:
                float(splt[7])
            if len(splt[8]) > 0:
                int(splt[8])
            if len(splt[9]) > 0:
                float(splt[9])
            if len(splt[10]) > 0:
                float(splt[10])
            if len(splt[11]) > 0:
                int(splt[11])
            if len(splt[12]) > 0:
                float(splt[12])
            if len(splt[13]) > 0:
                int(splt[13])
            if len(splt[14]) > 0:
                int(splt[14])
            if len(splt[15]) > 0:
                int(splt[15])
            if len(splt[16]) > 0:
                float(splt[16])
        except ValueError as we:
            print ln
            print we.message
            return False
        return True

    @staticmethod
    def parse(ln):
        splt = ln.split(',')

        slot_id = float(splt[0])
        slot_width = int(splt[1])
        mac = splt[2]
        desc = splt[3]
        isiot = int(splt[4])
        ethlen = int(splt[5])
        ethsum = int(splt[6])

        ethstd = np.nan # 7
        tcp_udp_ratio = np.nan # 10
        remote_ip = np.nan
        avg_ttl = np.nan
        ports = np.nan
        tcpts = np.nan
        max_winds = np.nan
        udns = np.nan
        dns = np.nan
        avg_ua = np.nan

        if len(splt[7]) > 0:
            ethstd = float(splt[7])
        if len(splt[8]) > 0:
            remote_ip = int(splt[8])
        if len(splt[9]) > 0:
            avg_ttl = float(splt[9])
        if len(splt[10]) > 0:
            tcp_udp_ratio = float(splt[10])
        if len(splt[11]) > 0:
            ports = int(splt[11])
        if len(splt[12]) > 0:
            tcpts = float(splt[12])
        if len(splt[13]) > 0:
            max_winds = int(splt[13])
        if len(splt[14]) > 0:
            udns = int(splt[14])
        if len(splt[15]) > 0:
            dns = int(splt[15])
        if len(splt[16]) > 0:
            avg_ua = float(splt[16])

        return DBRecord(slot_id, slot_width, mac, desc, isiot, ethlen, ethsum, ethstd, remote_ip, avg_ttl, tcp_udp_ratio, ports, tcpts, max_winds, udns, dns, avg_ua)
