# Setting up Wireless Android Auto Dongle on Raspberry Pi OS

This guide explains how to set up the Wireless Android Auto Dongle software on a standard Raspberry Pi OS installation.

## 1. Base Setup

1. Download Raspberry Pi OS Lite from https://www.raspberrypi.com/software/operating-systems/
2. Flash the image to your SD card using Raspberry Pi Imager

## 2. System Configuration

After booting up and logging in:

```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip git python3-dbus python3-protobuf bluetooth bluez
```

## 3. USB Gadget Mode Setup

1. Edit `/boot/config.txt`:
```bash
sudo nano /boot/config.txt
```

Add at the end:
```
dtoverlay=dwc2
```

2. Edit `/boot/cmdline.txt`:
```bash
sudo nano /boot/cmdline.txt
```

Add after rootwait:
```
modules-load=dwc2
```

## 4. Install the Software

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/nisargjhaveri/WirelessAndroidAutoDongle
cd WirelessAndroidAutoDongle/aawg

# Install the Python package
sudo pip3 install -e .

# Start the service
sudo systemctl start aawgd
sudo systemctl enable aawgd
```

## Troubleshooting

1. Check service status:
```bash
sudo systemctl status aawgd
journalctl -u aawgd
```

2. Verify USB gadget mode:
```bash
lsmod | grep dwc2
```

3. Check Bluetooth:
```bash
sudo systemctl status bluetooth
