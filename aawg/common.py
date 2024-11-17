import os
import logging
import syslog
from enum import Enum, IntEnum
from typing import Optional, Dict, Any
from dataclasses import dataclass
import fcntl
import socket
import struct

class ConnectionStrategy(Enum):
    DONGLE_MODE = 0
    PHONE_FIRST = 1
    USB_FIRST = 2

class SecurityMode(IntEnum):
    NONE = 0
    WEP = 1
    WPA_PERSONAL = 2
    WPA2_PERSONAL = 3

class AccessPointType(IntEnum):
    STATIC = 0
    DYNAMIC = 1

@dataclass
class WifiInfo:
    ssid: str
    key: str
    bssid: str
    security_mode: SecurityMode
    access_point_type: AccessPointType
    ip_address: str
    port: int

class Logger:
    """Logging utility that mirrors the C++ version's functionality"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Configure logging to both syslog and stderr
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        stderr_handler = logging.StreamHandler()
        
        # Set format
        formatter = logging.Formatter('%(name)s: %(message)s')
        syslog_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)
        
        self.logger.addHandler(syslog_handler)
        self.logger.addHandler(stderr_handler)
        self.logger.setLevel(logging.INFO)
        
    def info(self, message: str, *args):
        """Log an info message"""
        if args:
            message = message % args
        self.logger.info(message)
        syslog.syslog(syslog.LOG_INFO, f"{self.name}: {message}")
        
    def error(self, message: str, *args):
        """Log an error message"""
        if args:
            message = message % args
        self.logger.error(message)
        syslog.syslog(syslog.LOG_ERR, f"{self.name}: {message}")
        
    @staticmethod
    def instance():
        """Get singleton instance"""
        if not hasattr(Logger, '_instance'):
            Logger._instance = Logger('AAWG')
        return Logger._instance

class Config:
    """Configuration management that mirrors the C++ version's functionality"""
    
    def __init__(self):
        self._connection_strategy: Optional[ConnectionStrategy] = None
        self.logger = Logger("Config")
        
    def get_env(self, name: str, default: Any) -> Any:
        """Get environment variable with default value"""
        value = os.environ.get(name)
        if value is None:
            return default
            
        if isinstance(default, int):
            try:
                return int(value)
            except ValueError:
                return default
        return value
        
    def get_mac_address(self, interface: str) -> str:
        """Get MAC address of network interface"""
        try:
            with open(f"/sys/class/net/{interface}/address") as f:
                return f.read().strip()
        except Exception as e:
            self.logger.error(f"Failed to get MAC address for {interface}: {e}")
            return "00:00:00:00:00:00"
            
    def get_unique_suffix(self) -> str:
        """Get unique suffix for device naming"""
        suffix = self.get_env("AAWG_UNIQUE_NAME_SUFFIX", "")
        if suffix:
            return suffix
            
        try:
            with open("/sys/firmware/devicetree/base/serial-number") as f:
                serial = f.read().strip('\0')
                # Pad with zeros and take last 6 characters
                return ("00000000" + serial)[-6:]
        except Exception as e:
            self.logger.error(f"Failed to get serial number: {e}")
            return "000000"
            
    def get_wifi_info(self) -> WifiInfo:
        """Get WiFi configuration information"""
        return WifiInfo(
            ssid=self.get_env("AAWG_WIFI_SSID", "AAWirelessDongle"),
            key=self.get_env("AAWG_WIFI_PASSWORD", "ConnectAAWirelessDongle"),
            bssid=self.get_env("AAWG_WIFI_BSSID", self.get_mac_address("wlan0")),
            security_mode=SecurityMode.WPA2_PERSONAL,
            access_point_type=AccessPointType.DYNAMIC,
            ip_address=self.get_env("AAWG_PROXY_IP_ADDRESS", "10.0.0.1"),
            port=self.get_env("AAWG_PROXY_PORT", 5288)
        )
        
    def get_connection_strategy(self) -> ConnectionStrategy:
        """Get connection strategy configuration"""
        if self._connection_strategy is None:
            strategy_value = self.get_env("AAWG_CONNECTION_STRATEGY", 1)
            
            try:
                self._connection_strategy = ConnectionStrategy(strategy_value)
            except ValueError:
                self._connection_strategy = ConnectionStrategy.PHONE_FIRST
                
        return self._connection_strategy
        
    @staticmethod
    def instance():
        """Get singleton instance"""
        if not hasattr(Config, '_instance'):
            Config._instance = Config()
        return Config._instance
