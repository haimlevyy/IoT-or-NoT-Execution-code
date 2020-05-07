import numpy as np


class DBRecord(object):
    def __init__(self, slot_id=None, slot_width=None, mac=None, desc=None, isiot=None, ethlen=None, ethsum=None, remote_ip=None, avg_ttl=None, ports=None, tcpts=None, max_winds=None, udns=None, dns=None, avg_ua=None):
        if slot_id is None:
            return
        self.slot_id = slot_id
        self.slot_width = slot_width
        self.mac = mac
        self.desc = desc
        self.isiot = isiot
        self.ethlen = ethlen
        self.ethsum = ethsum
        self.remote_ip = remote_ip
        self.avg_ttl = avg_ttl
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
        if len(splt) != 15:
            return False
        try:
            float(splt[0])
            int(splt[1])
            int(splt[4])
            int(splt[5])
            int(splt[6])
            if len(splt[7]) > 0:
                int(splt[7])
            if len(splt[8]) > 0:
                float(splt[8])
            if len(splt[9]) > 0:
                int(splt[9])
            if len(splt[10]) > 0:
                float(splt[10])
            if len(splt[11]) > 0:
                int(splt[11])
            if len(splt[12]) > 0:
                int(splt[12])
            if len(splt[13]) > 0:
                int(splt[13])
            if len(splt[14]) > 0:
                float(splt[14])
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

        remote_ip = np.nan
        avg_ttl = np.nan
        ports = np.nan
        tcpts = np.nan
        max_winds = np.nan
        udns = np.nan
        dns = np.nan
        avg_ua = np.nan
        if len(splt[7]) > 0:
            remote_ip = int(splt[7])
        if len(splt[8]) > 0:
            avg_ttl = float(splt[8])
        if len(splt[9]) > 0:
            ports = int(splt[9])
        if len(splt[10]) > 0:
            tcpts = float(splt[10])
        if len(splt[11]) > 0:
            max_winds = int(splt[11])
        if len(splt[12]) > 0:
            udns = int(splt[12])
        if len(splt[13]) > 0:
            dns = int(splt[13])
        if len(splt[14]) > 0:
            avg_ua = float(splt[14])

        return DBRecord(slot_id, slot_width, mac, desc, isiot, ethlen, ethsum, remote_ip, avg_ttl, ports, tcpts, max_winds, udns, dns, avg_ua)
