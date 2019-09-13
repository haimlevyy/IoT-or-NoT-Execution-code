__author__ = 'haim.levy@post.idc.ac.il'

from Classifier import logreg_classifier
from DHCPClassifier import dhcp_classifier
from combiner import combiner


# Summery: This script reads the "features" files created by the "Extractor" script.
#          It tests this data using the attached trained models.
#          It will print classification report to stdout.


# ## INPUT:

# # Put your oracle file here:
ORACLE = "../sample_oracle.csv"

# # Put your features folder here:
FEATURES_FOLDER_PATH = "../pcap2features/features/"

# # Put your dhcp fdb file here:
DHCP_FDB_PATH = "../pcap2features/dhcp_fdb.csv"


def main():
    ## The script will also creates the file "_sets_tmp.csv" as part of it's running.
    ## You may delete it after the script ends or examine it (this file contains the classification results for each slot).
    logreg_classifier(FEATURES_FOLDER_PATH)
    dhcp_dict = dhcp_classifier(DHCP_FDB_PATH, ORACLE)
    combiner(dhcp_dict)


if '__main__' == __name__:
    main()
