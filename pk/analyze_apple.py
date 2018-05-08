import numpy as np
from scipy import signal
import pickle
from packetcollection import PacketCollection
import matplotlib.pyplot as plt
from datetime import datetime

with open("captured_packets-05011526.p", "rb") as f:
    pcollection = pickle.load(f)

austin_mac = "5C:AD:CF:1A:2F:BE".lower()  ## Austin
michael_mac = "60:03:08:a1:15:d0".lower()  ## Michael
date = "2018:05:01:"

# All Apple Devices
target = "Apple"
target_sa_list = []

for sa, company in pcollection.sa_to_vendor.items():
    if company == "Apple" and len(pcollection.sa_to_timestamps[sa]) > 10:
        target_sa_list.append(sa)
print("Number of Apple Devices more than one probe: ", len(target_sa_list))
prob_freq_list = []
for sa in target_sa_list:
    timestamps = pcollection.sa_to_timestamps[sa]
    times_do = [
        datetime.strptime(date + t, "%Y:%m:%d:%H:%M:%S.%f") for t in timestamps
    ]
    times_from_begin = [
        times_do[i].timestamp() - times_do[0].timestamp()
        for i in range(len(times_do))
    ]
    prob_freq_list.append(np.mean(np.diff(times_from_begin)))

# Austin and Michael
phone_laptop = []
for sa in [austin_mac, michael_mac]:
    timestamps = pcollection.sa_to_timestamps[sa]
    times_do = [
        datetime.strptime(date + t, "%Y:%m:%d:%H:%M:%S.%f") for t in timestamps
    ]
    times_from_begin = [
        times_do[i].timestamp() - times_do[0].timestamp()
        for i in range(len(times_do))
    ]
    phone_laptop.append(np.mean(np.diff(times_from_begin)))

plt.hist(prob_freq_list, bins=10, label="All Apple Devices")
plt.axvline(
    x=phone_laptop[0], label="iPhone 7 iOS 8", color="red", linestyle="-.")
plt.axvline(
    x=phone_laptop[1], label="MacBookPro OSX", color="green", linestyle="--")
plt.xlabel("Probe Period [s]")
plt.ylabel("Devices Count")
plt.legend()
plt.show()
