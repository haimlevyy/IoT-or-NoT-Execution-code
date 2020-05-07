from Base import *


class DeviceTagsLoader(object):
    def __init__(self, tagfile):
        self.devs = {}
        self.load(tagfile)

    def load(self, tagfile, is_fresh=True):
        if is_fresh:
            self.devs = {}
        fl = open(tagfile, 'r')
        data = fl.read()
        fl.close()
        lines = data.replace('\r', '').split('\n')
        for ln in lines:
            if not self.is_valid(ln):
                continue
            mac, desc, isiot, = self.parse_line(ln)
            dd = DevData(mac, desc, int(isiot))
            if mac in self.devs.keys():
                continue
            self.devs[mac] = dd
        return self.devs

    @staticmethod
    def is_valid(ln):
        splt = ln.split(',')
        if len(splt) != 3:
            return False
        if not is_mac_valid(splt[0]) or len(splt[1]) < 1 or len(splt[2]) != 1:
            return False
        try:
            int(splt[2])
        except ValueError:
            return False
        return True

    @staticmethod
    def parse_line(ln):
        splt = ln.split(',')
        mac, desc, isiot = splt[0], splt[1], splt[2]
        return mac, desc, isiot


def is_mac_valid(mac):
    bytes = None
    if ':' in mac:
        bytes = mac.split(':')
    elif '-' in mac:
        bytes = mac.split('-')
    else:
        return False
        #raise NotImplementedError('Unsupported MAC address type')

    if len(bytes) != 6:
        return False
        #raise ValueError('Bad MAC format')

    for byte in bytes:
        try:
            int(byte, 16)
        except ValueError as ve:
            return False
            #raise ve
    return True
