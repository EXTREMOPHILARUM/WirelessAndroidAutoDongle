import os
import time
import threading
from typing import Optional
from pathlib import Path
import glob
from dataclasses import dataclass
from datetime import timedelta

from common import Logger
from uevent import UeventHandler, UeventEnv

@dataclass
class UsbGadgetConfig:
    DEFAULT_GADGET = "default"
    ACCESSORY_GADGET = "accessory"
    GADGET_CONFIG_PATH = "/sys/kernel/config/usb_gadget"
    UDC_CLASS_PATH = "/sys/class/udc"

class UsbHandler:
    def __init__(self):
        self.logger = Logger("UsbHandler")
        self.udc_name: Optional[str] = None
        self.gadget_enabled = False
        self.accessory_promise: Optional[threading.Event] = None
        
    def init(self):
        """Initialize USB handler"""
        self.logger.info("Initializing USB Handler")
        
        # Disable any active gadgets first
        self.disable_gadget()
        
        # Find UDC name
        try:
            udc_paths = glob.glob(f"{UsbGadgetConfig.UDC_CLASS_PATH}/*")
            for udc_path in udc_paths:
                name = os.path.basename(udc_path)
                if name.startswith('.'):
                    continue
                self.udc_name = name
                break
                
            if self.udc_name:
                self.logger.info(f"Found UDC: {self.udc_name}")
            else:
                self.logger.error("Did not find a valid UDC to use")
                
        except Exception as e:
            self.logger.error(f"Error initializing USB handler: {e}")
            
    def _write_gadget_file(self, gadget_name: str, relative_path: str, content: str):
        """Write content to a gadget file"""
        try:
            file_path = Path(UsbGadgetConfig.GADGET_CONFIG_PATH) / gadget_name / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content + '\n')
        except Exception as e:
            self.logger.error(f"Error writing to gadget file {file_path}: {e}")
            
    def enable_gadget(self, gadget_name: str):
        """Enable a USB gadget"""
        if not self.udc_name:
            self.logger.error("No UDC available")
            return
            
        try:
            self._write_gadget_file(gadget_name, "UDC", self.udc_name)
            self.gadget_enabled = True
            self.logger.info(f"Enabled gadget: {gadget_name}")
        except Exception as e:
            self.logger.error(f"Failed to enable gadget {gadget_name}: {e}")
            
    def disable_gadget(self, gadget_name: Optional[str] = None):
        """Disable a USB gadget or all gadgets if no name specified"""
        try:
            if gadget_name:
                self._write_gadget_file(gadget_name, "UDC", "")
                self.logger.info(f"Disabled gadget: {gadget_name}")
            else:
                # Disable all gadgets
                self._write_gadget_file(UsbGadgetConfig.DEFAULT_GADGET, "UDC", "")
                self._write_gadget_file(UsbGadgetConfig.ACCESSORY_GADGET, "UDC", "")
                self.logger.info("Disabled all USB gadgets")
            self.gadget_enabled = False
        except Exception as e:
            self.logger.error(f"Error disabling gadget(s): {e}")
            
    def switch_to_accessory_gadget(self):
        """Switch from default to accessory gadget"""
        try:
            self.disable_gadget(UsbGadgetConfig.DEFAULT_GADGET)
            time.sleep(0.1)  # 100ms delay to let host recognize the change
            self.enable_gadget(UsbGadgetConfig.ACCESSORY_GADGET)
            self.logger.info("Switched to accessory gadget from default")
        except Exception as e:
            self.logger.error(f"Error switching to accessory gadget: {e}")
            
    def enable_default_and_wait_for_accessory(self, timeout: Optional[timedelta] = None) -> bool:
        """Enable default gadget and wait for accessory mode request
        
        Args:
            timeout: Optional timeout duration. If None, wait indefinitely.
            
        Returns:
            bool: True if accessory mode was requested, False if timeout occurred
        """
        self.accessory_promise = threading.Event()
        
        def accessory_handler(env: UeventEnv) -> bool:
            if (env.get("DEVNAME") == "usb_accessory" and 
                env.get("ACCESSORY") == "START"):
                self.logger.info("Received accessory start request")
                self.switch_to_accessory_gadget()
                self.accessory_promise.set()
                return True
            return False
            
        UeventHandler().instance().add_handler(accessory_handler)
        
        self.enable_gadget(UsbGadgetConfig.DEFAULT_GADGET)
        self.logger.info("Enabled default gadget")
        
        if timeout is None:
            self.accessory_promise.wait()
            return True
        else:
            return self.accessory_promise.wait(timeout.total_seconds())
            
    def cleanup(self):
        """Clean up resources"""
        self.disable_gadget()
        if self.accessory_promise:
            self.accessory_promise.set()  # Unblock any waiting threads
            
    @staticmethod
    def instance():
        """Get singleton instance"""
        if not hasattr(UsbHandler, '_instance'):
            UsbHandler._instance = UsbHandler()
        return UsbHandler._instance
