__author__ = 'haim.levy@post.idc.ac.il'

from PerDevClassifier import *
from Classifier import *

OUTPUT = 'outfile.txt'


class Activator(object):
    def __init__(self, pre_path, PRE_NAME=None, per_dev=False):
        classi = Classifier
        if per_dev:
            classi = PerDevClassifier
        self.fold_0 = classi(pre_path + '0_fold/', PRE_NAME)
        self.fold_1 = classi(pre_path + '1_fold/', PRE_NAME)
        self.fold_2 = classi(pre_path + '2_fold/', PRE_NAME)
        self.fold_3 = classi(pre_path + '3_fold/', PRE_NAME)
        self.fold_4 = classi(pre_path + '4_fold/', PRE_NAME)

    def make_avg(self, sw, features):
        res = [
            self.fold_0.classify(sw, features),
            self.fold_1.classify(sw, features),
            self.fold_2.classify(sw, features),
            self.fold_3.classify(sw, features),
            self.fold_4.classify(sw, features)
        ]
        res = np.asarray(res)
        avg_mat = res.mean(0)
        return avg_mat

    def get_all_scores(self, sw, features):
        res = [
            self.fold_0.classify(sw, features),
            self.fold_1.classify(sw, features),
            self.fold_2.classify(sw, features),
            self.fold_3.classify(sw, features),
            self.fold_4.classify(sw, features)
        ]
        res = np.asarray(res)
        return res

    def run_for_sws(self, sws, features):
        mat = []
        for sw in sws:
            mat.append(list(self.make_avg(sw, features)))
        mat = np.asarray(mat)
        return mat


def folders_test(PRE_NAME):
    # article's features
    features = [['max_winds', 'udns', 'tcp_udp_ratio', 'ethlen'],  # 60
                ['max_winds', 'udns'],  # 120
                ['udns', 'max_winds', 'ethstd', 'remote_ip', 'tcp_udp_ratio'],  # 180
                ['udns', 'max_winds', 'remote_ip'],  # 240 #
                ['udns', 'max_winds', 'remote_ip'],  # 300
                ['udns', 'max_winds', 'remote_ip', 'ethstd'],  # 600
                ['udns', 'max_winds', 'tcp_udp_ratio', 'ethstd'],  # 900
                ['udns', 'max_winds', 'remote_ip'],  # 1200
                ]

    sws = [60, 120, 180, 240, 300, 600, 900, 1200]
    act = Activator('../features2folds/seen_w_all_folds/', PRE_NAME, per_dev=True)
    all_res = []
    for i in xrange(len(sws)):
        print 'for:', features[i]
        mat = act.make_avg(sws[i], features[i])
        print "total score:", np.mean(mat)
        all_res.append(np.mean(mat))
    print all_res


def final_test(PRE_NAME):
    # article's features
    features = [['max_winds', 'udns', 'tcp_udp_ratio', 'ethlen'],  # 60
                ['max_winds', 'udns'],  # 120
                ['udns', 'max_winds', 'ethstd', 'remote_ip', 'tcp_udp_ratio'],  # 180
                ['udns', 'max_winds', 'remote_ip'],  # 240 #
                ['udns', 'max_winds', 'remote_ip'],  # 300
                ['udns', 'max_winds', 'remote_ip', 'ethstd'],  # 600
                ['udns', 'max_winds', 'tcp_udp_ratio', 'ethstd'],  # 900
                ['udns', 'max_winds', 'remote_ip'],  # 1200
                ]

    sws = [60, 120, 180, 240, 300, 600, 900, 1200]
    clas = PerDevClassifier(r'feaatures_files/', PRE_NAME)
    #clas = Classifier('./last_test/')
    res = [
        clas.classify(sws[0], features[0]),
        clas.classify(sws[1], features[1]),
        clas.classify(sws[2], features[2]),
        clas.classify(sws[3], features[3]),
        clas.classify(sws[4], features[4]),
        clas.classify(sws[5], features[5]),
        #clas.classify(sws[6], features[6]),
        clas.classify(sws[7], features[7]),
    ]
    print 'finale test'
    print np.asarray(res)
    #print np.mean(np.asarray(res), 0)


def main():
    print 'starting'
    #folders_test(PRE_NAME)
    final_test(None)


if '__main__' == __name__:
    np.set_printoptions(linewidth=np.inf)
    main()
