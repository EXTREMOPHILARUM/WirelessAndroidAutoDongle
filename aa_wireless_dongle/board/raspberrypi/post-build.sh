#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path

def post_build():
    """Handle post-build configuration"""
    # Get environment variables
    target_dir = os.environ.get('TARGET_DIR')
    binaries_dir = os.environ.get('BINARIES_DIR')
    
    if not all([target_dir, binaries_dir]):
        print("Error: Required environment variables not set")
        return 1
    
    try:
        # Move config file to binaries directory
        config_src = Path(target_dir) / "etc/aawgd.conf.py"
        config_dst = Path(binaries_dir) / "aawgd.conf.py"
        shutil.move(str(config_src), str(config_dst))
        
        # Create symlink
        config_link = Path(target_dir) / "etc/aawgd.conf.py"
        config_link.symlink_to("/boot/aawgd.conf.py")
        
        # Source the original raspberrypi post-build script
        os.system("source board/raspberrypi/post-build.sh")
        
        return 0
        
    except Exception as e:
        print(f"Error in post-build: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(post_build())
