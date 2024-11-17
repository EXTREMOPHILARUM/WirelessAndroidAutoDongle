# `proxyHandler.h`

The `proxyHandler.h` file contains the declaration of the `AAWProxy` class and its member functions for the Android Auto Wireless Gateway (AAWG) package. The `AAWProxy` class is responsible for managing the proxy handler and forwarding data between the TCP and USB connections.

## Classes

### `AAWProxy`

The `AAWProxy` class is responsible for managing the proxy handler and forwarding data between the TCP and USB connections.

#### Member Variables

- `int m_usb_fd`: File descriptor for the USB connection.
- `int m_tcp_fd`: File descriptor for the TCP connection.
- `std::optional<std::thread> m_usb_tcp_thread`: Thread for forwarding data from USB to TCP.
- `std::optional<std::thread> m_tcp_usb_thread`: Thread for forwarding data from TCP to USB.
- `std::atomic<bool> m_log_communication`: Flag to enable logging of communication details.

#### Member Functions

- `std::optional<std::thread> startServer(int32_t port)`: Starts the TCP server and listens for incoming connections.
- `void handleClient(int server_sock)`: Handles the client connection by accepting the connection and forwarding data between the TCP and USB connections.
- `void forward(ProxyDirection direction, std::atomic<bool>& should_exit)`: Forwards data between the TCP and USB connections in the specified direction.
- `void stopForwarding(std::atomic<bool>& should_exit)`: Stops forwarding data between the TCP and USB connections.
- `ssize_t readFully(int fd, unsigned char *buffer, size_t nbyte)`: Reads the specified number of bytes from the file descriptor into the buffer.
- `ssize_t readMessage(int fd, unsigned char *buffer, size_t buffer_len)`: Reads a message from the file descriptor into the buffer.

### `ProxyDirection`

The `ProxyDirection` enum class defines the direction of data forwarding between the TCP and USB connections.

#### Enum Values

- `TCP_to_USB`: Forward data from TCP to USB.
- `USB_to_TCP`: Forward data from USB to TCP.
