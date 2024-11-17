#!/bin/bash

# Default Pi IP address when connected to its WiFi
PI_IP="${PI_IP:-10.0.0.1}"
PI_USER="${PI_USER:-root}"
PI_PASS="${PI_PASS:-password}"

# Source directory (Python implementation)
SRC_DIR="aa_wireless_dongle/package/aawg/src"

# Check if source directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo "Error: Source directory $SRC_DIR not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Function to check if Pi is reachable
check_pi() {
    ping -c 1 $PI_IP >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Cannot reach Pi at $PI_IP"
        echo "Make sure you're connected to the Pi's WiFi (SSID: AAWirelessDongle)"
        exit 1
    fi
}

# Function to sync files
sync_files() {
    echo "Syncing Python files to Pi..."
    scp -r ${SRC_DIR}/*.py ${PI_USER}@${PI_IP}:/usr/lib/python3/site-packages/aawgd/
    if [ $? -ne 0 ]; then
        echo "Error: Failed to sync files"
        exit 1
    fi
}

# Function to restart service
restart_service() {
    echo "Restarting aawgd service..."
    ssh ${PI_USER}@${PI_IP} "systemctl restart aawgd"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to restart service"
        exit 1
    fi
}

# Main execution
echo "Checking Pi connection..."
check_pi

sync_files
restart_service

echo "Code synced and service restarted successfully"
echo "You can check service status with: ssh ${PI_USER}@${PI_IP} 'systemctl status aawgd'"
echo "View logs with: ssh ${PI_USER}@${PI_IP} 'journalctl -u aawgd -f'"
