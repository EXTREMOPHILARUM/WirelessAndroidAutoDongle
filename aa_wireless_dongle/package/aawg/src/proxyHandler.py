import socket
import threading
import select
import os
import signal
import time
from typing import Optional, Tuple
from dataclasses import dataclass

from common import Logger, Config, ConnectionStrategy
from bluetoothHandler import BluetoothHandler

@dataclass
class ProxyConnection:
    usb_fd: int = -1
    tcp_fd: int = -1
    usb_tcp_thread: Optional[threading.Thread] = None
    tcp_usb_thread: Optional[threading.Thread] = None

class ProxyHandler:
    BUFFER_SIZE = 16384
    
    def __init__(self):
        self.logger = Logger("ProxyHandler")
        self.connection = ProxyConnection()
        self.should_exit = threading.Event()
        self.log_communication = False
        
    def start_server(self, port: int) -> Optional[threading.Thread]:
        """Start the TCP server"""
        self.logger.info(f"Starting TCP server on port {port}")
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('', port))
            server_sock.listen(1)
            
            server_thread = threading.Thread(target=self._handle_client, 
                                          args=(server_sock,))
            server_thread.start()
            return server_thread
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            return None
            
    def _handle_client(self, server_sock: socket.socket):
        """Handle incoming client connection"""
        try:
            client_sock, client_addr = server_sock.accept()
            self.connection.tcp_fd = client_sock.fileno()
            server_sock.close()
            
            self.logger.info("TCP server accepted connection")
            
            # Stop bluetooth retry when TCP connected
            BluetoothHandler().instance().stop_connect_with_retry()
            
            # Set socket timeout
            client_sock.settimeout(10.0)
            
            # Open USB accessory
            try:
                usb_fd = os.open("/dev/usb_accessory", os.O_RDWR)
                self.connection.usb_fd = usb_fd
            except OSError as e:
                self.logger.error(f"Error opening /dev/usb_accessory: {e}")
                return
                
            self.logger.info("Starting data forwarding between TCP and USB")
            self._start_forwarding()
            
        except Exception as e:
            self.logger.error(f"Error handling client: {e}")
        finally:
            self._cleanup()
            
    def _start_forwarding(self):
        """Start forwarding data between TCP and USB"""
        self.should_exit.clear()
        
        # Start USB to TCP forwarding thread
        self.connection.usb_tcp_thread = threading.Thread(
            target=self._forward,
            args=("USB", "TCP", self.connection.usb_fd, self.connection.tcp_fd)
        )
        self.connection.usb_tcp_thread.start()
        
        # Start TCP to USB forwarding thread
        self.connection.tcp_usb_thread = threading.Thread(
            target=self._forward,
            args=("TCP", "USB", self.connection.tcp_fd, self.connection.usb_fd)
        )
        self.connection.tcp_usb_thread.start()
        
        # Wait for threads to complete
        self.connection.usb_tcp_thread.join()
        self.connection.tcp_usb_thread.join()
        
    def _forward(self, src_name: str, dst_name: str, src_fd: int, dst_fd: int):
        """Forward data between source and destination file descriptors"""
        try:
            while not self.should_exit.is_set():
                # Use select to wait for data
                readable, _, _ = select.select([src_fd], [], [], 1.0)
                if not readable:
                    continue
                    
                # Read data
                try:
                    data = os.read(src_fd, self.BUFFER_SIZE)
                except OSError as e:
                    self.logger.error(f"Read from {src_name} failed: {e}")
                    break
                    
                if not data:  # EOF
                    break
                    
                if self.log_communication:
                    self.logger.info(f"{len(data)} bytes read from {src_name}")
                    
                # Write data
                try:
                    bytes_written = os.write(dst_fd, data)
                    if self.log_communication:
                        self.logger.info(f"{bytes_written} bytes written to {dst_name}")
                except OSError as e:
                    self.logger.error(f"Write to {dst_name} failed: {e}")
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in forwarding {src_name} to {dst_name}: {e}")
        finally:
            self.stop_forwarding()
            
    def _read_message(self, fd: int) -> Tuple[bool, bytes]:
        """Read a complete message from the file descriptor"""
        try:
            # Read header (4 bytes)
            header = os.read(fd, 4)
            if len(header) != 4:
                return False, b''
                
            # Parse message length
            message_length = (header[2] << 8) + header[3]
            
            # Check if extended header
            FRAME_TYPE_FIRST = 1 << 0
            FRAME_TYPE_LAST = 1 << 1
            FRAME_TYPE_MASK = FRAME_TYPE_FIRST | FRAME_TYPE_LAST
            
            if (header[1] & FRAME_TYPE_MASK) == FRAME_TYPE_FIRST:
                # Read extended header (4 more bytes)
                ext_header = os.read(fd, 4)
                if len(ext_header) != 4:
                    return False, b''
                message_length += 4
                
            # Read message body
            message = os.read(fd, message_length)
            if len(message) != message_length:
                return False, b''
                
            return True, header + message
            
        except Exception as e:
            self.logger.error(f"Error reading message: {e}")
            return False, b''
            
    def stop_forwarding(self):
        """Stop all forwarding threads"""
        self.logger.info("Stopping data forwarding")
        self.should_exit.set()
        
    def _cleanup(self):
        """Clean up resources"""
        self.stop_forwarding()
        
        if self.connection.usb_fd != -1:
            try:
                os.close(self.connection.usb_fd)
            except OSError:
                pass
            self.connection.usb_fd = -1
            
        if self.connection.tcp_fd != -1:
            try:
                os.close(self.connection.tcp_fd)
            except OSError:
                pass
            self.connection.tcp_fd = -1
