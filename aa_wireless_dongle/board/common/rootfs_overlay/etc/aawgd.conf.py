#!/usr/bin/env python3

"""Common configuration options for Android Auto Wireless Dongle"""

import os

# Set the connection strategy to use
# 0 - Dongle mode. Waits for both dongle and headunit bluetooth connections and then starts the wifi and usb connections.
# 1 - Phone first (default). Waits for the phone bluetooth and wifi to connect first, and then starts the usb connection.
# 2 - Usb first. Waits for the usb to connect first, and then starts the bluetooth and wifi connection with phone.
os.environ["AAWG_CONNECTION_STRATEGY"] = "1"

# Override bluetooth name suffix
# Set a custom suffix to replace unique id used in "WirelessAADongle-<suffix>" or "AndroidAuto-Dongle-<suffix>"
# os.environ["AAWG_UNIQUE_NAME_SUFFIX"] = ""
