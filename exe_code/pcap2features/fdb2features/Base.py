import os


class DevData(object):
    def __init__(self, mac, desc, isiot):
        self.mac = mac
        self.desc = desc
        self.isiot = isiot


def add(st, delim=','):
    return delim + str(st)


def format_lst(lst):
    return str(lst).replace(',', ';').replace('[', '').replace(']', '')


def create_folder(name):
    prefix = add(name, '')
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    return


def is_mac_valid(mac):
    bytes = None
    if ':' in mac:
        bytes = mac.split(':')
    elif '-' in mac:
        bytes = mac.split('-')
    else:
        return False

    if len(bytes) != 6:
        return False

    for byte in bytes:
        try:
            int(byte, 16)
        except ValueError as ve:
            return False
    return True


def make_fn_vars(name, slot_width):
    res = add(name, '')
    res += add(slot_width, '_sd_')
    return res


def save_file(fn, data, mode='w'):
    fl = open(fn, mode)
    fl.write(data)
    fl.close()
    return


def get_dev_file_name(pre_path, dev):
    prefix = pre_path + 'NOT/'
    if str(dev.isiot) == str(1):
        prefix = pre_path + 'IOT/'
    name = (dev.desc + '_' + dev.mac).replace(":", '-').replace(" ", '_').replace("/", '_').replace(" ", '_')
    return prefix + name + '.txt'


