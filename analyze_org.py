import numpy as np
from scipy import signal
import pickle
from packetcollection import PacketCollection
import matplotlib.pyplot as plt
from datetime import datetime

with open("captured_packets-05021347.p", "rb") as f:
    # with open("captured_packets-05011526.p", "rb") as f:
    pcollection = pickle.load(f)

# Device Count
vendor_count = {}
for sa, vendor in pcollection.sa_to_vendor.items():
    if vendor in vendor_count:
        vendor_count[vendor] += 1
    else:
        vendor_count[vendor] = 1

vendor_list = vendor_count.keys()
count_list = vendor_count.values()

plt.bar(range(len(vendor_list)), count_list)
plt.xticks(range(len(vendor_list)), vendor_list, fontsize=15)
plt.xlabel("Vendor", fontsize=20)
plt.ylabel("Device Count", fontsize=20)
plt.show()
