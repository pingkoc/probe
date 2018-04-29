import pyshark
import pickle
import time
import datetime

from pyshark.packet import layer

captured_packets = []
monitor_iface = 'wlp0s20f0u1'


def packetHandler(pkt):
    global captured_packets
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    captured_packets.append((st, pkt))
    print("Packets captured:", len(captured_packets))


capture = pyshark.LiveCapture(
    interface=monitor_iface,
    bpf_filter='type mgt subtype probe-req',
    output_file="./captured.pcap")

# while True:
#     try:
#         capture = pyshark.LiveCapture(
#             interface=monitor_iface, bpf_filter='type mgt subtype probe-req')
#         capture.apply_on_packets(packetHandler)
#     except KeyboardInterrupt:
#         with open("captured_packets.p", "wb") as f:
#             pickle.dump(captured_packets, f)
#         print(captured_packets)
#         print("Saved to file")
#         exit()
