__author__ = 'haim.levy@post.idc.ac.il'

from pcap2fdb.main import pcap2fdb
from fdb2features.main import fdb2features
from DHCP2fdb.main import dhcp2fdb

# Summery: This script reads .pcap files (can handle huge files) and extracts relevant features for further classification.
#          This script associates the collected features with the tagged devices in the 'oracle' file.


# ## INPUT:

# # Put your .pcap files here as a list.
# # The files should be in chronological order. (The order of the files DO matter)
PCAPS = [
    ## this is an example, the actual files are not included.
    "part01.pcap",
    "part02.pcap",
    "part03.pcap",
    "part04.pcap",
]

# # Put your oracle here:
ORACLE = "../sample_oracle.csv"


# ## OUTPUT:

# # Put your output folder here: (folder should be already exist)
OUT_FOLDER_PATH = "./features/"

# # Put your output dhcp features file here: (will be created)
OUT_DHCP_FDB_PATH = "./dhcp_fdb.csv"


def main():
    ## The script will also creates the file "tmp_pcap_fdb.csv" as part of it's running.
    ## You may delete it after the script ends or examine it (this file contains the extracted features).
    pcap2fdb(PCAPS, ORACLE, "tmp_pcap_fdb.csv")
    fdb2features(ORACLE, "./tmp_pcap_fdb.csv", OUT_FOLDER_PATH)
    dhcp2fdb(PCAPS, ORACLE, OUT_DHCP_FDB_PATH)


if '__main__' == __name__:
    main()
