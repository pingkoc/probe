class Packet:
    def __init__(self, sa, da, bssid, data_rates, signal_strength, timestamp):
        self.timestamp = timestamp
        self.signal_strength = signal_strength
        self.sa = sa
        self.da = da
        self.bssid = bssid
        self.data_rates = data_rates

    def __str__(self):
        return str(self.__dict__)

