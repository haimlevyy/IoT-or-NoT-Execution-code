# IoT or NoT Execution Code
### requirements
1. python 2.7.X
2. scapy & pcapy
3. numpy & sklearn (anaconda for windows)
### what in the box?
1. "pcap2features/Extractor.py" - script that extracts features from .pcap files.
2. "classifiers/DoClassify.py" - script that classifies IoT vs NoT according to feature files.
### Usage:
For each one of those scripts:
1. At first, you should edit the input variables in the main script file as instructed by the comments. (There is an example with sample files)
2. Go to the script's folder. 
3. Activate the script using python:
```bash
python <script-name>.py
```
### Example:
There is an example included with sample-data.
The sample-data files are:
- sample_oracle.csv
- pcap2features/dhcp_fdb.csv
- pcap2features/tmp_pcap_fdb.csv
- pcap2features/features/*
- classifiers/_set_tmp.csv