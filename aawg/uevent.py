import os
import socket
import struct
import threading
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass

from common import Logger

# Netlink constants
NETLINK_KOBJECT_UEVENT = 15
NETLINK_MSG_SIZE = 8 * 1024

@dataclass
class UeventEnv:
    """Class to hold uevent environment variables"""
    env_vars: Dict[str, str] = None
    
    def __post_init__(self):
        if self.env_vars is None:
            self.env_vars = {}
            
    def get(self, key: str, default: str = None) -> str:
        return self.env_vars.get(key, default)

class UeventHandler:
    def __init__(self):
        self.logger = Logger("UeventHandler")
        self.handlers: List[Callable[[UeventEnv], bool]] = []
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        
    def start(self) -> Optional[threading.Thread]:
        """Start the uevent monitoring"""
        self.logger.info("Starting uevent monitoring")
        
        try:
            # Create netlink socket
            sock = socket.socket(
                socket.AF_NETLINK,
                socket.SOCK_DGRAM | socket.SOCK_CLOEXEC,
                NETLINK_KOBJECT_UEVENT
            )
            
            # Bind the socket
            sock.bind((os.getpid(), -1))
            
            # Set socket options
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_PASSCRED, 1)
            
            self.running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(sock,)
            )
            self.monitor_thread.start()
            
            self.logger.info("Uevent monitoring started")
            return self.monitor_thread
            
        except Exception as e:
            self.logger.error(f"Failed to start uevent monitoring: {e}")
            return None
            
    def _monitor_loop(self, sock: socket.socket):
        """Main monitoring loop for uevent messages"""
        while self.running:
            try:
                # Read netlink message
                msg = sock.recv(NETLINK_MSG_SIZE)
                if not msg:
                    continue
                    
                # Parse the message
                env_map = self._parse_uevent_message(msg)
                
                # Process handlers
                self._process_handlers(env_map)
                
            except Exception as e:
                if self.running:  # Only log if we're still supposed to be running
                    self.logger.error(f"Error in uevent monitor loop: {e}")
                    
        sock.close()
        
    def _parse_uevent_message(self, msg: bytes) -> UeventEnv:
        """Parse a uevent message into environment variables"""
        env_map = UeventEnv()
        
        try:
            # Split message into null-terminated strings
            parts = msg.split(b'\0')
            
            # Process each part
            for part in parts:
                if not part:  # Skip empty parts
                    continue
                    
                # Decode the part
                try:
                    decoded = part.decode('utf-8')
                except UnicodeDecodeError:
                    continue
                    
                # Split into key-value if possible
                if '=' in decoded:
                    key, value = decoded.split('=', 1)
                    env_map.env_vars[key] = value
                    
        except Exception as e:
            self.logger.error(f"Error parsing uevent message: {e}")
            
        return env_map
        
    def _process_handlers(self, env_map: UeventEnv):
        """Process all registered handlers with the uevent"""
        # Create a copy of handlers to avoid modification during iteration
        handlers = self.handlers.copy()
        
        # Process each handler
        for handler in handlers:
            try:
                if handler(env_map):
                    # If handler returns True, remove it
                    try:
                        self.handlers.remove(handler)
                    except ValueError:
                        # Handler might have been removed by another thread
                        pass
            except Exception as e:
                self.logger.error(f"Error in uevent handler: {e}")
                
    def add_handler(self, handler: Callable[[UeventEnv], bool]):
        """Add a new uevent handler
        
        Args:
            handler: Callback function that takes a UeventEnv and returns bool.
                    Return True to remove the handler, False to keep it.
        """
        self.handlers.append(handler)
        
    def stop(self):
        """Stop the uevent monitoring"""
        self.running = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join()
            
    def __del__(self):
        """Ensure resources are cleaned up"""
        self.stop()
