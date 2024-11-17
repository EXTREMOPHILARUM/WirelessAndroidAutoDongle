#!/usr/bin/env python3

import os
import sys

def post_image():
    """Handle post-image configuration"""
    try:
        # Source the original raspberrypi post-image script
        os.system("source board/raspberrypi/post-image.sh")
        return 0
        
    except Exception as e:
        print(f"Error in post-image: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(post_image())
