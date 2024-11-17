from dataclasses import dataclass

@dataclass
class WifiStartRequest:
    ssid: str
    password: str
