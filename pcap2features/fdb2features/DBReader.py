from DBRecord import *


class DBReader(object):
    def __init__(self, fn):
        self.fl = open(fn, 'r')
        self.records = []

    def read(self):
        while True:
            line = self.fl.readline()
            if line is None or line == '':
                break
            line = line.replace('\r', '').replace('\n', '')
            if not DBRecord.is_valid(line):
                continue
            self.records.append(DBRecord.parse(line))
        return self.records

