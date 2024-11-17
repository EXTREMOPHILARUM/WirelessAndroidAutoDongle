# `common.cpp` File

The `common.cpp` file contains common utilities and configurations used throughout the Android Auto Wireless Gateway (AAWG) package. It includes the following components:

## Config Class

The `Config` class provides configuration settings and environment variables for the AAWG package. It includes methods to retrieve WiFi information, connection strategy, unique suffix, and environment variables.

### Methods

- `static Config* instance()`: Returns the singleton instance of the `Config` class.
- `WifiInfo getWifiInfo()`: Retrieves the WiFi information.
- `ConnectionStrategy getConnectionStrategy()`: Retrieves the connection strategy.
- `std::string getUniqueSuffix()`: Retrieves the unique suffix.
- `int32_t getenv(std::string name, int32_t defaultValue)`: Retrieves an environment variable as an integer.
- `std::string getenv(std::string name, std::string defaultValue)`: Retrieves an environment variable as a string.
- `std::string getMacAddress(std::string interface)`: Retrieves the MAC address of a network interface.

## Logger Class

The `Logger` class provides logging functionality for the AAWG package. It includes methods to log informational messages.

### Methods

- `static Logger* instance()`: Returns the singleton instance of the `Logger` class.
- `void info(const char *format, ...)`: Logs an informational message.

## Enums

The `common.cpp` file also defines the following enums:

- `SecurityMode`: Represents the security mode for WiFi.
- `AccessPointType`: Represents the access point type for WiFi.
- `ConnectionStrategy`: Represents the connection strategy for the AAWG package.

## Structs

The `common.cpp` file defines the following structs:

- `WifiInfo`: Represents the WiFi information, including SSID, key, BSSID, security mode, access point type, IP address, and port.
