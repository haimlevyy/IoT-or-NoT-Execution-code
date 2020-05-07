import numpy as np


class DHCPRecord(object):
    def __init__(self, slot_id=None, slot_width=None, mac=None, desc=None, isiot=None, ethlen=None, hostname=None, vendor_class=None, req_lst=None, mds=None, msg_t = None, client_id = None):
        if slot_id is None:
            return
        self.slot_id = slot_id
        self.slot_width = slot_width
        self.mac = mac
        self.desc = desc
        self.isiot = isiot
        self.ethlen = ethlen
        self.hostname = hostname
        self.vendor_class = vendor_class
        self.req_lst = req_lst
        self.mds = mds
        self.msg_t = msg_t
        self.client_id = client_id
        return

    @staticmethod
    def is_valid(ln):
        splt = ln.split(',')
        if len(splt) != 12:
            return False
        try:
            float(splt[0])
            int(splt[1])
            int(splt[4])
            int(splt[5])
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

        hostname = None
        vendor_class = None
        req_lst = None
        mds = None
        msg_t = None
        client_id = None

        if len(splt[6]) > 0:
            hostname = splt[6]
        if len(splt[7]) > 0:
            vendor_class = splt[7]
        if len(splt[8]) > 0:
            req_lst = splt[8]
        if len(splt[9]) > 0:
            mds = splt[9]
        if len(splt[10]) > 0:
            msg_t = splt[10]
        if len(splt[11]) > 0:
            client_id = splt[11]

        return DHCPRecord(slot_id, slot_width, mac, desc, isiot, ethlen, hostname, vendor_class, req_lst, mds, msg_t, client_id)
