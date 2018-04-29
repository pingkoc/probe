class Packet:
    def __init__(self, sa, da, bssid, data_rates, signal_strength, timestamp):
        self.sa = sa
        self.da = da
        self.bssid = bssid
        self.data_rates = data_rates
        self.signal_strength = signal_strength
        self.timestamp = timestamp

