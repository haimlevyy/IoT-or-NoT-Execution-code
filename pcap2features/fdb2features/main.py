__author__ = 'haim.levy@post.idc.ac.il'
from DBReader import DBReader
from DBRecord import DBRecord
from DeviceTagsLoader import *
from Saver import Saver

# load file
# then; filter by slot_width/devices/features/...


def fdb2features(oracle_fn, features_file, pre_path):
    dtl = DeviceTagsLoader(oracle_fn)
    oracle = dtl.devs
    reader = DBReader(features_file)
    records = reader.read()

    # print len(records)
    saver = Saver(pre_path, records, oracle)
    saver.print_touples(pre_path, samples=False)
