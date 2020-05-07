# IoT or NoT Research Code
### requirements
1. python 2.7.X
    - yes, the deprecated version :(
2. python packages:
    - scapy (for analyzing packets)
    - pcapy (for reading pcap files)
    - numpy
    - sklearn
    - matplotlib

The code is cross-platform and can be executed on both linux or windows platforms.
I did most of my work on windows, however, I believe that making a workable workspace on linux will be much easier.

For Windows:
- install anaconda 2
- scapy: make sure you install it over the anaconda installation.
- pcapy: same, moreover, because of that WinPcap is deprecated, scapy now using npcap library.
Thats fine, however, pcapy is stil needs the winpcap-header files. you can get it from the package: "winpcap dev" (google it, tip: you should deploy this folder directly on "C:\").
    
For Linux:
- actually I did not test it, but I believe you can get everything you need just from using "apt-get" and "pip install" :)


### what in the box?
In this package you have the latest code of the research;
1. exe_code:
Is mainly the execute code for the classifiers; (but contains a vital script-> pcap2features)

    - pcap2features:
    a vital script, it will turn your huge pcap files into a small features tables called- "fdb" (=features DB, a csv file)
    and features files sorted by IoT and NoT and divided to devices.
        - Usage: see Extractor.py for further instructions.
    - dumps:
    contains bin files of pre-trained models.
    the binary dumps created using "pickle" (python package)
    - classifiers:
    contains the classifiers from the article (appendix not included).
    Note: this is JUST the execution code (using the trained model in the dumps folder).
        - Usage: see DoClassify.py for further instructions
2. DHCP_Trainer
    - This code will make a DHCP Decision Tree.
    - find_fp_auto: will learn dhcp_fdb file into a decision tree and will test and print & export the learned tree.

3. features2folders
    - will turn features files (.txt, those that sorted into IOT/NOT folders) into 5-fold sets (when test's parts have no overlaps).

4. logistic_regression: this one is very important.
    - This folder is the "traffic classifer". You activate "main.py" in order to train/test the model using your desired features set.
    - main.py is just the activator. the real magic is performed in "PerDevClassifier.py" or "Classifier.py".
    - The differences between them:
        - classifier: is TESTING using samples (in order to get balance between devices) - this is essential for learning.
        - PerDevClassifier: is TESTING using ALL the traffic, and achieving balance by averaging TP, FP, ... for each device before continiuing to the next device.
        - Important: as you may feel.. those "modes" require different type of features files (samples/all).
    - find_features.py: is using greedy OR exhustive algorithms in order to find an optimal set of features (using Activator class that declared in main.py in order to activate PerDevClassifier.py ....)

5. CombTrainerTester:
    This folders contains code related to the appendix.
    This code will:
    - train a traffic classifier (trafficClassifier.py)
    - train a unifier classifier (combiner.py)
    - will use a pre-trained decision tree for DHCP (using pickle dumps)
    - After training.. it will perform a test.

