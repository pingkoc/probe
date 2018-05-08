#!/bin/env python3
import sys
import re
import pickle
from datetime import datetime, timedelta
from packet import Packet
from packetcollection import VendorDB, PacketCollection

non_digit = re.compile(r'[^\d.]+')
# Create DB
vendorDB_name = "oui.json"
vendordb = VendorDB(vendorDB_name)
packetdb = PacketCollection(vendordb)
last_timestamp = datetime.now()
try:
    for l in sys.stdin:
        try:
            vs = l.split()
            timestamp = vs[0]
            signal_strength = float(non_digit.sub('', vs[10]))
            da = vs[17][3:]
            sa = vs[18][3:]
            assert(len(sa.split(":")) == 6)
            data_rates = []
            if vs[23][-1] is ")":
                bssid = vs[23]
                start = 24
            else:
                bssid = vs[23] + vs[24]
                start = 25

            bssid = bssid[1:-1]

            for v in vs[start:-1]:
                data_rates.append(float(non_digit.sub('', v)))

        except:
            continue
            # for i in range(len(vs)):
            #     print(i, vs[i])

        p = Packet(sa, da, bssid, data_rates, signal_strength, timestamp)

        packetdb.handler(p)

        if datetime.now() - last_timestamp > timedelta(seconds=3):
            last_timestamp = datetime.now()
            print(datetime.now())
            print("Active device count", packetdb.realtime_sa_set_size())
            print("Active device mac", packetdb.realtime_sa_set.keys())
            print("Total Packets Received", len(packetdb.packet_list))
            print("Total Addresses", packetdb.count_addresses_collected())
            print("Resolved Addresses", packetdb.count_resolved_devices())
            print("Vendors", packetdb.sa_to_vendor)
            print("Unresolved Addresses", packetdb.count_unresolved_addresses())
            print("\n")
except KeyboardInterrupt:
    output = 'captured_packets-' + datetime.now().strftime("%y-%d-%H:%M:%S") +'.p'
    with open(output, 'wb') as f:
        pickle.dump(packetdb, f)
    print('saved to pickle')
    exit()
