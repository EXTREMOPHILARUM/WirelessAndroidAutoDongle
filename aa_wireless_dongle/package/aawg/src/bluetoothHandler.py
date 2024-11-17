import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from typing import Optional, Dict, List
import threading
import time

from common import Logger, Config, ConnectionStrategy

BLUEZ_BUS_NAME = "org.bluez"
BLUEZ_INTERFACE = "org.bluez.Adapter1"
BLUEZ_OBJECT_PATH = "/org/bluez/hci0"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"
ADAPTER_ALIAS_PREFIX = "WirelessAADongle-"
ADAPTER_ALIAS_DONGLE_PREFIX = "AndroidAuto-Dongle-"

class BluetoothHandler:
    def __init__(self):
        self.logger = Logger("BluetoothHandler")
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.adapter = None
        self.adapter_path = None
        self.mainloop = GLib.MainLoop()
        self.connect_retry_thread = None
        self.should_stop_retry = threading.Event()
        self.advertisement = None
        
    def init(self):
        """Initialize the Bluetooth handler"""
        self._init_adapter()
        self._export_profiles()
        self.logger.info("Bluetooth handler initialized")
        
    def _init_adapter(self):
        """Initialize the Bluetooth adapter"""
        try:
            obj = self.bus.get_object(BLUEZ_BUS_NAME, BLUEZ_OBJECT_PATH)
            self.adapter = dbus.Interface(obj, BLUEZ_INTERFACE)
            self.adapter_path = BLUEZ_OBJECT_PATH
            
            # Set adapter alias
            prefix = ADAPTER_ALIAS_DONGLE_PREFIX if Config.instance().get_connection_strategy() == ConnectionStrategy.DONGLE_MODE else ADAPTER_ALIAS_PREFIX
            alias = prefix + Config.instance().get_unique_suffix()
            self.adapter.Set(BLUEZ_INTERFACE, "Alias", alias)
            
            self.logger.info(f"Using bluetooth adapter at path: {self.adapter_path}")
            self.logger.info(f"Bluetooth adapter alias: {alias}")
        except dbus.exceptions.DBusException as e:
            self.logger.error(f"Failed to initialize bluetooth adapter: {e}")
            
    def _export_profiles(self):
        """Export Bluetooth profiles"""
        if not self.adapter:
            return
            
        try:
            self._register_profile("AAWireless", {
                "Name": "AA Wireless",
                "Role": "server",
                "Channel": 8,
                "UUID": "4de17a00-52cb-11e6-bdf4-0800200c9a66"
            })
            self.logger.info("Bluetooth AA Wireless profile active")
            
            if Config.instance().get_connection_strategy() != ConnectionStrategy.DONGLE_MODE:
                self._register_profile("HSP_HS", {
                    "Name": "HSP HS",
                    "UUID": "00001108-0000-1000-8000-00805f9b34fb"
                })
                self.logger.info("HSP Handset profile active")
        except Exception as e:
            self.logger.error(f"Failed to export profiles: {e}")
            
    def _register_profile(self, profile_path: str, properties: Dict):
        """Register a Bluetooth profile"""
        profile_manager = dbus.Interface(
            self.bus.get_object(BLUEZ_BUS_NAME, "/org/bluez"),
            "org.bluez.ProfileManager1"
        )
        profile_manager.RegisterProfile(
            f"/com/aawgd/bluetooth/{profile_path}",
            properties["UUID"],
            properties
        )
        
    def power_on(self):
        """Power on the Bluetooth adapter"""
        if not self.adapter:
            return
            
        try:
            self.adapter.Set(BLUEZ_INTERFACE, "Powered", True)
            self.adapter.Set(BLUEZ_INTERFACE, "Discoverable", True)
            self.adapter.Set(BLUEZ_INTERFACE, "Pairable", True)
            self.logger.info("Bluetooth adapter powered on and made discoverable")
            
            if Config.instance().get_connection_strategy() == ConnectionStrategy.DONGLE_MODE:
                self._start_advertising()
        except Exception as e:
            self.logger.error(f"Failed to power on adapter: {e}")
            
    def _start_advertising(self):
        """Start BLE advertising"""
        try:
            ad_manager = dbus.Interface(
                self.bus.get_object(BLUEZ_BUS_NAME, self.adapter_path),
                LE_ADVERTISING_MANAGER_IFACE
            )
            
            self.advertisement = Advertisement(self.bus, 0)
            ad_manager.RegisterAdvertisement(
                self.advertisement.get_path(), {},
                reply_handler=self._advertising_registered_cb,
                error_handler=self._advertising_error_cb
            )
            self.logger.info("BLE Advertisement started")
        except Exception as e:
            self.logger.error(f"Failed to start advertising: {e}")
            
    def _advertising_registered_cb(self):
        self.logger.info("Advertisement registered successfully")
        
    def _advertising_error_cb(self, error):
        self.logger.error(f"Failed to register advertisement: {error}")
        
    def connect_with_retry(self) -> Optional[threading.Thread]:
        """Start a thread that attempts to connect to devices"""
        if not self.adapter:
            return None
            
        self.should_stop_retry.clear()
        self.connect_retry_thread = threading.Thread(target=self._retry_connect_loop)
        self.connect_retry_thread.start()
        return self.connect_retry_thread
        
    def _retry_connect_loop(self):
        """Loop that continuously attempts to connect to devices"""
        while not self.should_stop_retry.is_set():
            try:
                self._connect_device()
                time.sleep(20)  # Wait before retry
            except Exception as e:
                self.logger.error(f"Error in connect retry loop: {e}")
                
        if Config.instance().get_connection_strategy() != ConnectionStrategy.DONGLE_MODE:
            self.power_off()
            
    def _connect_device(self):
        """Attempt to connect to available devices"""
        om = dbus.Interface(
            self.bus.get_object(BLUEZ_BUS_NAME, "/"),
            "org.freedesktop.DBus.ObjectManager"
        )
        objects = om.GetManagedObjects()
        
        for path, interfaces in objects.items():
            if "org.bluez.Device1" not in interfaces:
                continue
                
            device = interfaces["org.bluez.Device1"]
            self._try_connect_device(path, device)
                
    def _try_connect_device(self, path: str, device: Dict):
        """Try to connect to a specific device"""
        try:
            device_obj = self.bus.get_object(BLUEZ_BUS_NAME, path)
            device_iface = dbus.Interface(device_obj, "org.bluez.Device1")
            
            if device.get("Connected", False):
                self.logger.info(f"Device {path} already connected, disconnecting")
                device_iface.Disconnect()
                
            profile_uuid = "" if Config.instance().get_connection_strategy() == ConnectionStrategy.DONGLE_MODE else "00001112-0000-1000-8000-00805f9b34fb"
            device_iface.ConnectProfile(profile_uuid)
            self.logger.info(f"Successfully connected to device {path}")
        except Exception as e:
            self.logger.error(f"Failed to connect to device {path}: {e}")
            
    def stop_connect_with_retry(self):
        """Stop the connection retry loop"""
        if self.connect_retry_thread:
            self.should_stop_retry.set()
            
    def power_off(self):
        """Power off the Bluetooth adapter"""
        if not self.adapter:
            return
            
        try:
            if Config.instance().get_connection_strategy() == ConnectionStrategy.DONGLE_MODE:
                self._stop_advertising()
            self.adapter.Set(BLUEZ_INTERFACE, "Powered", False)
            self.logger.info("Bluetooth adapter powered off")
        except Exception as e:
            self.logger.error(f"Failed to power off adapter: {e}")
            
    def _stop_advertising(self):
        """Stop BLE advertising"""
        if self.advertisement:
            try:
                ad_manager = dbus.Interface(
                    self.bus.get_object(BLUEZ_BUS_NAME, self.adapter_path),
                    LE_ADVERTISING_MANAGER_IFACE
                )
                ad_manager.UnregisterAdvertisement(self.advertisement.get_path())
                self.advertisement = None
                self.logger.info("BLE Advertisement stopped")
            except Exception as e:
                self.logger.error(f"Failed to stop advertising: {e}")
                
    def cleanup(self):
        """Clean up resources"""
        self.stop_connect_with_retry()
        self.power_off()
        if self.mainloop.is_running():
            self.mainloop.quit()

class Advertisement(dbus.service.Object):
    """BLE Advertisement class"""
    def __init__(self, bus, index):
        self.path = f"/com/aawgd/bluetooth/advertisement{index}"
        self.bus = bus
        super().__init__(bus, self.path)
        
        self.add_service_uuid("4de17a00-52cb-11e6-bdf4-0800200c9a66")
        
    def get_path(self):
        """Get the DBus path of the advertisement"""
        return dbus.ObjectPath(self.path)
        
    @dbus.service.method("org.bluez.LEAdvertisement1",
                        in_signature="", out_signature="")
    def Release(self):
        """Release the advertisement"""
        Logger("Advertisement").info(f"Released {self.path}")
