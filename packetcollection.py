from packet import Packet
from datetime import datetime, timedelta
import json
vendorDB_name = "oui.json"


class VendorDB:
    def __init__(self, mac_vendor_json_path):
        print("Loading MAC database...")
        with open(mac_vendor_json_path, 'r') as content_file:
            mac_json = content_file.read()
        mac_resolve_list = json.loads(mac_json)
        self.mac_resolve_dict = {
            mac_vendor[0]: mac_vendor[1]
            for mac_vendor in mac_resolve_list
        }

    def find_vendor(self, mac):
        if mac[:8].upper() in self.mac_resolve_dict:
            return self.mac_resolve_dict[mac[:8].upper()]
        return "UNRESOLVED"

    # TODO
    def is_phone_vendor(self, vendor_name):
        return False


class PacketCollection:
    def __init__(self, vendordb):
        self.packet_list = []
        ## Every packet will go into the sa_set and the dictionaries
        self.sa_set = set()
        self.sa_to_timestamps = {}
        self.sa_to_bssids = {}
        self.sa_to_vendor = {}
        # Unresolved sa will go into this set
        self.unresolved_sa_set = set()
        # vendor db is for vendor lookup to resolve randomized mac addresses
        self.vendordb = vendordb
        self.realtime_sa_set = {}
        self.EXPIRE_DELTA = timedelta(seconds=60)

    def count_addresses_collected(self):
        # TODO: Resolve randomized address
        return len(self.sa_set)

    def count_resolved_devices(self):
        return len(self.sa_set) - len(self.unresolved_sa_set)

    def count_unresolved_addresses(self):
        return len(self.unresolved_sa_set)

    def realtime_sa_set_add(self, p):
        self.realtime_sa_set[p.sa] = datetime.now()

    def realtime_sa_set_size(self):
        now = datetime.now()
        remove_set = set()
        for sa in self.realtime_sa_set.keys():
            if now - self.realtime_sa_set[sa] > self.EXPIRE_DELTA:
                remove_set.add(sa)
        for sa in remove_set:
            self.realtime_sa_set.pop(sa)
        return len(self.realtime_sa_set)


    def handler(self, packet):
        # Collect all packets
        self.packet_list.append(packet)

        self.realtime_sa_set_add(packet)

        # Store information about source address
        # TODO: Check here for valid address, Only keep smartphones and resolve MAC addresses
        # Record all sa
        if packet.sa not in self.sa_set:
            self.sa_set.add(packet.sa)
        # Record Timestamp
        if packet.sa not in self.sa_to_timestamps:
            self.sa_to_timestamps[packet.sa] = [packet.timestamp]
        else:
            self.sa_to_timestamps[packet.sa].append(packet.timestamp)
        # Record bssid list for device
        if packet.bssid != "":
            if packet.sa not in self.sa_to_bssids:
                self.sa_to_bssids[packet.sa] = [packet.bssid]
            else:
                self.sa_to_bssids[packet.sa].append(packet.bssid)
        # Resolved vendor information
        packet_vendor = self.vendordb.find_vendor(packet.sa)
        if packet_vendor == "UNRESOLVED":
            self.unresolved_sa_set.add(packet.sa)
        else:
            self.sa_to_vendor[packet.sa] = packet_vendor


# vendordb = VendorDB(vendorDB_name)
# packetdb = PacketCollection(vendordb)
# examplepacket = Packet("5c:ad:cf:1a:2f:be", "Broadcast", "TMobileWingman",
#                        [1.0, 2.0, 5.5, 11.0], -38, '14:42:41.479244')
# packetdb.handler(examplepacket)
# print(packetdb.sa_set)
# print(packetdb.sa_to_vendor[list(packetdb.sa_set)[0]])
# print(packetdb.count_addresses_collected())
# print(packetdb.count_resolved_devices())
# print(packetdb.count_unresolved_addresses())
