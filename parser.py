#!/bin/env python3
import sys
import re
from packet import Packet
non_digit = re.compile(r'[^\d.]+')
import re

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

    except ValueError as e:
        print('Parse error', e)
        # for i in range(len(vs)):
        #     print(i, vs[i])
            
    p = Packet(sa, da, bssid, data_rates, signal_strength, timestamp)
    print(p)

