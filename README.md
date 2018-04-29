# Estimate Occupancy with Wifi Probes

## How to run

IFACE="en0" sudo tcpdump  -l -e -I -i $IFACE type mgt subtype probe-req | python3 parser.py
