import numpy as np
from scipy import signal
import pickle
from packetcollection import PacketCollection
import matplotlib.pyplot as plt
from datetime import datetime

with open("captured_packets-05011526.p", "rb") as f:
    pcollection = pickle.load(f)

# mac = "5C:AD:CF:1A:2F:BE".lower() ## Austin
mac = "60:03:08:a1:15:d0".lower()  ## Michael
date = "2018:05:01:"
print("MAC Address:", mac)

if mac in pcollection.sa_to_timestamps:
    times = pcollection.sa_to_timestamps[mac]
else:
    print("Not Found")
    exit()

# Time elapsed in microseconds since first probe
times_do = [datetime.strptime(date + t, "%Y:%m:%d:%H:%M:%S.%f") for t in times]
times_from_begin = [
    times_do[i].timestamp() - times_do[0].timestamp()
    for i in range(len(times_do))
]

# plt.hist(times_from_begin, bins=int(times_from_begin[-1]))
# plt.show()

# FFT
fs = 1
times_ms = [int(t * fs) for t in times_from_begin]
timeseries = np.zeros(times_ms[-1] - times_ms[0] + 1)
for t in times_ms:
    timeseries[t] += 1

plt.plot(range(len(timeseries)), timeseries)
plt.xlabel("Time [s]")
plt.ylabel("Probe Count")
plt.show()

# Spectrogram
# f, t, Sxx = signal.spectrogram(timeseries, fs)
# plt.pcolormesh(t, f, Sxx)
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [s]')
# plt.show()

# FFT
# sp = np.fft.rfft(timeseries)
# freq = np.fft.rfftfreq(timeseries.shape[-1])
# plt.plot(freq, sp.real, freq, sp.imag)
# plt.xlabel("Frequency [Hz]")
# plt.ylabel("Amplitude")
# plt.show()
