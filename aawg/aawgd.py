import threading
import time
import signal
from typing import Optional

from common import Logger, Config, ConnectionStrategy
from bluetoothHandler import BluetoothHandler
from proxyHandler import ProxyHandler
from usb import UsbHandler
from uevent import UeventHandler

class AAWG:
    def __init__(self):
        self.logger = Logger("AAWG")
        self.bluetooth_handler = BluetoothHandler()
        self.proxy_handler = ProxyHandler()
        self.usb_handler = UsbHandler()
        self.uevent_handler = UeventHandler()
        self.running = False
        self.uevent_thread = None
        
    def init(self):
        # Global initialization
        self.uevent_thread = self.uevent_handler.start()
        self.usb_handler.init()
        self.bluetooth_handler.init()
        
        strategy = Config.instance().get_connection_strategy()
        if strategy == ConnectionStrategy.DONGLE_MODE:
            self.bluetooth_handler.power_on()
            
    def run(self):
        self.running = True
        self.init()
        
        while self.running:
            strategy = Config.instance().get_connection_strategy()
            self.logger.info(f"Connection Strategy: {strategy}")
            
            if strategy == ConnectionStrategy.USB_FIRST:
                self.logger.info("Waiting for accessory to connect first")
                self.usb_handler.enable_default_and_wait_for_accessory()
                
            # Get WifiInfo object and access port attribute directly
            wifi_info = Config.instance().get_wifi_info()
            proxy_thread = self.proxy_handler.start_server(wifi_info.port)
                
            if not proxy_thread:
                return 1
                
            if strategy != ConnectionStrategy.DONGLE_MODE:
                self.bluetooth_handler.power_on()
                
            bt_thread = self.bluetooth_handler.connect_with_retry()
            
            proxy_thread.join()
            
            if bt_thread:
                self.bluetooth_handler.stop_connect_with_retry()
                bt_thread.join()
                
            self.usb_handler.disable_gadget()
            
            if strategy != ConnectionStrategy.DONGLE_MODE:
                time.sleep(2)
                
        if self.uevent_thread:
            self.uevent_thread.join()

    def cleanup(self, signum, frame):
        self.logger.info("Received signal to shutdown")
        self.running = False
        if self.bluetooth_handler:
            self.bluetooth_handler.cleanup()
        if self.usb_handler:
            self.usb_handler.cleanup()

def main():
    """Main entry point for the daemon"""
    aawg = AAWG()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, aawg.cleanup)
    signal.signal(signal.SIGTERM, aawg.cleanup)
    
    try:
        return aawg.run()
    except Exception as e:
        Logger("AAWG").error(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
