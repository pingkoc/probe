# Estimate Occupancy with Wifi Probes

## How to run

sudo tcpdump -l -s 256 -e -i en0 type mgt subtype probe-req | python3 parser.py
