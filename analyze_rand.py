import numpy as np
from scipy import signal
import pickle
from packetcollection import PacketCollection
import matplotlib.pyplot as plt
from datetime import datetime

with open("captured_packets-05021347.p", "rb") as f:
    # with open("captured_packets-05011526.p", "rb") as f:
    pcollection = pickle.load(f)

sa_pcount = []
for sa in pcollection.unresolved_sa_set:
    if sa == "Broadcast":
        continue
    sa_pcount.append(len(pcollection.sa_to_timestamps[sa]))

plt.hist(sa_pcount, bins=max(sa_pcount))
plt.xticks(range(max(sa_pcount) + 1))
plt.xlabel("Number of probes")
plt.ylabel("Number of random MAC address")
plt.show()
