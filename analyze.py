import numpy as np
from scipy import signal
import pickle
from packetcollection import PacketCollection
import matplotlib.pyplot as plt
from datetime import datetime

with open("captured_packets-05011526.p", "rb") as f:
    pcollection = pickle.load(f)
date = "2018:05:01:"

mac1 = "5C:AD:CF:1A:2F:BE".lower()  ## Austin
mac2 = "60:03:08:a1:15:d0".lower()  ## Michael
mac3 = "a4:34:d9:c4:c8:4f".lower()  ## PK
mac_list = [mac1, mac2, mac3]
color_list = ['red', 'green', 'blue']
label_list = [
    'iPhone 7 iOS 12', 'MacBookPro OSX 10.13', 'Intel Wireless Chipset'
]

print("MAC Addresses:", mac_list)
for mac, color, lab in zip(mac_list, color_list, label_list):

    if mac in pcollection.sa_to_timestamps:
        times = pcollection.sa_to_timestamps[mac]
    else:
        print("Not Found")
        exit()

    # Time elapsed in microseconds since first probe
    times_do = [
        datetime.strptime(date + t, "%Y:%m:%d:%H:%M:%S.%f") for t in times
    ]
    times_from_begin = [
        times_do[i].timestamp() - times_do[0].timestamp()
        for i in range(len(times_do))
    ]

    # FFT
    fs = 1
    times_ms = [int(t * fs) for t in times_from_begin]
    timeseries = np.zeros(times_ms[-1] - times_ms[0] + 1)
    for t in times_ms:
        timeseries[t] += 1

    plt.plot(range(len(timeseries)), timeseries, color=color, label=lab)
plt.xlabel("Time [s]")
plt.ylabel("Probe Count")
plt.legend()
plt.show()
