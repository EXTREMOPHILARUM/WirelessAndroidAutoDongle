from dataclasses import dataclass

@dataclass
class WifiInfoResponse:
    ssid: str
    bssid: str
    signal_strength: int
