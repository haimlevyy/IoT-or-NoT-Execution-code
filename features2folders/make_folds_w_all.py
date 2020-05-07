__author__ = 'haim.levy@post.idc.ac.il'

from os import listdir
from os.path import isfile, join
import random

from Base import *
from DeviceTagsLoader import *

oracle_fn = 'seen_oracle.csv'
SAMPLES_IN_DIR = '../2_fdb2features/seen_samples/'
ALL_IN_DIR = '../2_fdb2features/seen_all/'
OUT_MAIN = './seen_w_all_folds/'
OUT_TRAIN = 'train/'
OUT_TEST = 'test/'


def get_len(oracle, isiot):
    ln = 0
    for dev in oracle.values():
        if int(dev.isiot) == int(isiot):
            ln += 1
    return ln


def get_lengthes(oracle, train_ratio):
    iot_len, not_len = get_len(oracle, 1), get_len(oracle, 0)
    train_iot_len = int(round(iot_len * train_ratio))
    test_iot_len = int(round(iot_len * (1 - train_ratio)))
    if train_iot_len + test_iot_len > iot_len:
        test_iot_len -= 1
    train_not_len = int(round(not_len * train_ratio))
    test_not_len = int(round(not_len * (1 - train_ratio)))
    if train_not_len + test_not_len > not_len:
        test_not_len -= 1

    return train_iot_len, test_iot_len, train_not_len, test_not_len


def get_keys(oracle):
    iot_keys = []
    not_keys = []
    for dev in oracle.values():
        if dev.isiot == 0:
            not_keys.append(dev.mac)
        else:
            iot_keys.append(dev.mac)
    random.shuffle(iot_keys)
    random.shuffle(iot_keys)
    random.shuffle(iot_keys)
    random.shuffle(not_keys)
    random.shuffle(not_keys)
    random.shuffle(not_keys)
    return iot_keys, not_keys


def split_devs(oracle, train_ratio=0.8):
    train_oracle = {}
    test_oracle = {}
    train_iot_len, test_iot_len, train_not_len, test_not_len = get_lengthes(oracle, train_ratio)
    iot_keys, not_keys = get_keys(oracle)

    train_iot_keys = iot_keys[:train_iot_len]
    train_not_keys = not_keys[:train_not_len]

    test_iot_keys = iot_keys[train_iot_len:]
    test_not_keys = not_keys[train_not_len:]

    for k, v in oracle.items():
        if k in train_iot_keys or k in train_not_keys:
            train_oracle[k] = v
        if k in test_iot_keys or k in test_not_keys:
            test_oracle[k] = v

    return train_oracle, test_oracle


def make_folds(oracle):
    folds = []
    iot_k, not_k = get_keys(oracle)
    ilen, nlen = len(iot_k), len(not_k)

    for i in xrange(5):
        end_iot_curr = (i+1) * int(round(ilen * 0.2))
        end_not_curr = (i+1) * int(round(nlen * 0.2))
        if i == 4:
            end_iot_curr = ilen
            end_not_curr = nlen
        test_iot = iot_k[int(round(ilen * 0.2)) * i: end_iot_curr]
        test_not = not_k[int(round(nlen * 0.2)) * i: end_not_curr]
        train_iot = []
        for k in iot_k:
            if k not in test_iot:
                train_iot.append(k)
        train_not = []
        for k in not_k:
            if k not in test_not:
                train_not.append(k)

        folds.append(((train_iot + train_not), (test_iot + test_not)))
    return folds


def make_oracles(oracle, train, test):
    train_oracle, test_oracle = {}, {}
    for k, v in oracle.items():
        if k in train:
            train_oracle[k] = v
        if k in test:
            test_oracle[k] = v
    return train_oracle, test_oracle


def get_files_names():
    iot_dir = SAMPLES_IN_DIR + 'IOT/'
    not_dir = SAMPLES_IN_DIR + 'NOT/'
    iotfiles = [iot_dir + f for f in listdir(iot_dir) if isfile(join(iot_dir, f))]
    notfiles = [not_dir + f for f in listdir(not_dir) if isfile(join(not_dir, f))]
    return iotfiles + notfiles


def copy_files_per_oracle(oracle, infiles, pre_path):
    for k, v in oracle.items():
        name = get_dev_file_name(v)
        related_files = []
        for nm in infiles:
            if name[2:].lower() in nm.lower():
                related_files.append(nm)
        oracle[k].files = related_files
        for fl in related_files:
            out_fn = pre_path + '/' + name
            ifl = open(fl, 'r')
            ofl = open(out_fn, 'a')
            ofl.write(ifl.read())
            ifl.close()
            ofl.close()


def prepare_folders():
    tr_name = OUT_TRAIN
    ts_name = OUT_TEST
    for i in xrange(5):
        create_folder(OUT_MAIN)
        fold = OUT_MAIN + str(i) + '_fold/'
        create_folder(fold)
        create_folder(fold + tr_name)
        create_folder(fold + ts_name)
        create_folder(fold + tr_name + '/NOT')
        create_folder(fold + tr_name + '/IOT')
        create_folder(fold + ts_name + '/NOT')
        create_folder(fold + ts_name + '/IOT')
    return tr_name, ts_name


def map_samples_to_all(files):
    res = []
    for fl in files:
        #print fl
        fl = fl.replace("seen_samples", "seen_all")
        res.append(fl)
        #print fl
    return res


def main():
    train_fol, test_fol = prepare_folders()
    dtl = DeviceTagsLoader(oracle_fn)
    oracle = dtl.devs

    folds = make_folds(oracle)
    #for e in folds:
    #    print e

    file_names = get_files_names()

    for i in xrange(5):
        train, test = make_oracles(oracle, folds[i][0], folds[i][1])
        copy_files_per_oracle(train, file_names, OUT_MAIN + str(i) + '_fold/' + train_fol)
        file_names = map_samples_to_all(file_names)
        copy_files_per_oracle(test, file_names, OUT_MAIN + str(i) + '_fold/' + test_fol)


if '__main__' == __name__:
    main()
