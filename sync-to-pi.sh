#!/bin/bash

# Default Pi IP address when connected to its WiFi
PI_IP="${PI_IP:-pi4}"
PI_USER="${PI_USER:-extremo}"
PI_PASS="${PI_PASS:-@Lcazar31}"

# Source directory (Python implementation)
SRC_DIR="aawg"

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
    # First copy files to a temporary location
    ssh ${PI_USER}@${PI_IP} "mkdir -p ~/temp_aawg"
    scp -r ${SRC_DIR}/*.py ${PI_USER}@${PI_IP}:~/temp_aawg/
    scp ${SRC_DIR}/aawgd ${PI_USER}@${PI_IP}:~/temp_aawg/
    
    # Then use sudo to move them to both locations
    ssh ${PI_USER}@${PI_IP} "sudo mkdir -p /usr/local/lib/aawgd && \
                            sudo cp ~/temp_aawg/*.py /usr/local/lib/aawgd/ && \
                            sudo chmod 644 /usr/local/lib/aawgd/*.py && \
                            sudo cp ~/temp_aawg/aawgd /usr/local/bin/ && \
                            sudo chmod 755 /usr/local/bin/aawgd && \
                            sudo chown -R root:root /usr/local/lib/aawgd && \
                            sudo chown root:root /usr/local/bin/aawgd && \
                            sudo mkdir -p /home/extremo/WirelessAndroidAutoDongle/aawg && \
                            sudo cp ~/temp_aawg/*.py /home/extremo/WirelessAndroidAutoDongle/aawg/ && \
                            sudo chown -R extremo:extremo /home/extremo/WirelessAndroidAutoDongle/aawg && \
                            rm -rf ~/temp_aawg"
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to sync files"
        exit 1
    fi
}

# Function to restart service
restart_service() {
    echo "Restarting aawgd service..."
    ssh ${PI_USER}@${PI_IP} "sudo systemctl restart aawgd"
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
echo "You can check service status with: ssh ${PI_USER}@${PI_IP} 'sudo systemctl status aawgd'"
echo "View logs with: ssh ${PI_USER}@${PI_IP} 'sudo journalctl -u aawgd -f'"
