__author__ = 'haim.levy@post.idc.ac.il'

from TrafficClassifier import traffic_classifier
from DHCPClassifier import dhcp_classifier
from OnDemandDHCPClassifier import OnDemandDHCPClassifier
from combiner import combiner

# todo:  changes to make:
#    1.  I want to add this on the combiner:
#    1.1   enrich every classification result with it's time-tag
#    1.2   change dhcp-classi to be "on-demand" (I'm gonna call it only when I have data)
#    1.3   change the ranking scheme in combiner.


# Summery: This script reads the "features" files created by the "Extractor" script.
#          It tests this data using the attached trained models.
#          It will print classification report to stdout.


# ## INPUT:

# # Put your oracle file here:
ORACLE = r"test_oracle.csv"

# # Put your features folder here:
FEATURES_FOLDER_PATH = r"test\\"

# # Put your dhcp fdb file here:
DHCP_FDB_PATH = r"full_dhcp_db.csv"


def main():
    # # The script will also creates the file "_sets_tmp.csv" as part of it's running.
    # # You may delete it after the script ends or examine it (this file contains the classification results for each slot).
    traffic_classifier(FEATURES_FOLDER_PATH)
    dhcp_classifier(DHCP_FDB_PATH, ORACLE)
    dhcp_on_demand = OnDemandDHCPClassifier(DHCP_FDB_PATH, ORACLE)
    combiner(dhcp_on_demand, FEATURES_FOLDER_PATH)


if '__main__' == __name__:
    main()
