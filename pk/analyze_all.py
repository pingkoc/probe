import numpy as np
from scipy import signal
import pickle
from packetcollection import PacketCollection
import matplotlib.pyplot as plt
from datetime import datetime

with open("captured_packets-05021347.p", "rb") as f:
    pcollection = pickle.load(f)

fs = 1
packet_list = pcollection.packet_list
times = [float(p.timestamp) for p in packet_list]
times_from_begin = [t - times[0] for t in times]
elapsed_s = int(times[-1] - times[0])

probe_count = np.zeros(elapsed_s + 1)
for t in times_from_begin:
    probe_count[int(t)] += 1
print(probe_count)
# plt.plot(range(elapsed_s + 1), probe_count)
plt.hist(times_from_begin, bins=elapsed_s // 60)
plt.show()
