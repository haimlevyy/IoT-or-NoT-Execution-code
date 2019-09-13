class DBReader(object):
    def __init__(self, fn, dbrecord):
        self.fl = open(fn, 'r')
        self.records = []
        self._dbrecord = dbrecord

    def read(self):
        while True:
            line = self.fl.readline()
            if line is None or line == '':
                break
            line = line.replace('\r', '').replace('\n', '')
            if not self._dbrecord.is_valid(line):
                continue
            self.records.append(self._dbrecord.parse(line))
        return self.records








