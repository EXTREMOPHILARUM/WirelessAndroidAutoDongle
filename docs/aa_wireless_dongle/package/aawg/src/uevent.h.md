# `uevent.h` File

The `uevent.h` file contains the declaration of the `UeventMonitor` class and related types for the Android Auto Wireless Gateway (AAWG) package. It includes the following components:

## UeventMonitor Class

The `UeventMonitor` class is responsible for monitoring uevents and handling them using registered handlers. It includes methods to start the monitoring loop, add handlers, and process uevents.

### Methods

- `static UeventMonitor& instance()`: Returns the singleton instance of the `UeventMonitor` class.
- `std::optional<std::thread> start()`: Starts the uevent monitoring loop in a separate thread.
- `void addHandler(std::function<bool(UeventEnv)> handler)`: Adds a handler to be called for upcoming uevents.

### Private Methods

- `void monitorLoop(int nl_socket)`: The main loop for monitoring uevents.
- `UeventMonitor()`: Private constructor to enforce singleton pattern.

### Member Variables

- `std::list<std::function<bool(UeventEnv)>> handlers`: List of handlers to be called for each uevent.

## UeventEnv Type

The `UeventEnv` type is a typedef for a `std::map<std::string, std::string>`, representing the environment variables of a uevent.
