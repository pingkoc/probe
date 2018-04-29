#!/bin/env python3
import sys
import re
import re
import pickle
from packet import Packet
from packetcollection import VendorDB, PacketCollection

non_digit = re.compile(r'[^\d.]+')
# Create DB
vendorDB_name = "oui.json"
vendordb = VendorDB(vendorDB_name)
packetdb = PacketCollection(vendordb)

count = 0
try:
    for l in sys.stdin:
        try:
            vs = l.split()
            timestamp = vs[0]
            signal_strength = float(non_digit.sub('', vs[10]))
            da = vs[17][3:]
            sa = vs[18][3:]
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
        count += 1
        if count % 10 == 0:
            print("Total Packets Received", count)
            print("Total Addresses", packetdb.count_addresses_collected())
            print("Resolved Addresses", packetdb.count_resolved_devices())
            print("Vendors", packetdb.sa_to_vendor)
            print("Unresolved Addresses", packetdb.count_unresolved_addresses())
            print()
except KeyboardInterrupt:
    with open('captured_packets.p', 'wb') as f:
        pickle.dump(packetdb, f)
    print('saved to pickle')
    exit()
