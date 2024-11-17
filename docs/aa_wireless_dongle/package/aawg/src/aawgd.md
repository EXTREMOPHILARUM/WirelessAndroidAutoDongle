# `aawgd.cpp`

The `aawgd.cpp` file is the main entry point for the Android Auto Wireless Gateway Daemon (AAWGD). It initializes the necessary components and manages the connection strategy for the wireless dongle.

## Includes

```cpp
#include <stdio.h>
#include <unistd.h>

#include "common.h"
#include "bluetoothHandler.h"
#include "proxyHandler.h"
#include "uevent.h"
#include "usb.h"
```

## Main Function

The `main` function is the entry point of the AAWGD. It performs the following tasks:

1. Logs the start of the AA Wireless Dongle.
2. Initializes global components such as UeventMonitor, UsbManager, and BluetoothHandler.
3. Determines the connection strategy from the configuration.
4. Powers on the Bluetooth handler if the connection strategy is DONGLE_MODE.
5. Enters an infinite loop to manage the connection strategy and handle connections.

```cpp
int main(void) {
    Logger::instance()->info("AA Wireless Dongle\n");

    // Global init
    std::optional<std::thread> ueventThread =  UeventMonitor::instance().start();
    UsbManager::instance().init();
    BluetoothHandler::instance().init();

    ConnectionStrategy connectionStrategy = Config::instance()->getConnectionStrategy();
    if (connectionStrategy == ConnectionStrategy::DONGLE_MODE) {
        BluetoothHandler::instance().powerOn();
    }

    while (true) {
        Logger::instance()->info("Connection Strategy: %d\n", connectionStrategy);

        // Per connection setup and processing
        if (connectionStrategy == ConnectionStrategy::USB_FIRST) {
            Logger::instance()->info("Waiting for the accessory to connect first\n");
            UsbManager::instance().enableDefaultAndWaitForAccessory();
        }

        AAWProxy proxy;
        std::optional<std::thread> proxyThread = proxy.startServer(Config::instance()->getWifiInfo().port);

        if (!proxyThread) {
            return 1;
        }

        if (connectionStrategy != ConnectionStrategy::DONGLE_MODE) {
            BluetoothHandler::instance().powerOn();
        }

        std::optional<std::thread> btConnectionThread = BluetoothHandler::instance().connectWithRetry();

        proxyThread->join();

        if (btConnectionThread) {
            BluetoothHandler::instance().stopConnectWithRetry();
            btConnectionThread->join();
        }

        UsbManager::instance().disableGadget();

        if (connectionStrategy != ConnectionStrategy::DONGLE_MODE) {
            // sleep for a couple of seconds before retrying
            sleep(2);
        }
    }

    ueventThread->join();

    return 0;
}
```

## Explanation

- The `Logger::instance()->info` calls are used to log information about the dongle's status and actions.
- The `UeventMonitor::instance().start()` function starts monitoring uevents in a separate thread.
- The `UsbManager::instance().init()` function initializes the USB manager.
- The `BluetoothHandler::instance().init()` function initializes the Bluetooth handler.
- The `Config::instance()->getConnectionStrategy()` function retrieves the connection strategy from the configuration.
- The `BluetoothHandler::instance().powerOn()` function powers on the Bluetooth handler if the connection strategy is DONGLE_MODE.
- The `while (true)` loop manages the connection strategy and handles connections.
- The `UsbManager::instance().enableDefaultAndWaitForAccessory()` function enables the default USB gadget and waits for the accessory to connect.
- The `AAWProxy proxy` object is used to handle the proxy server.
- The `proxy.startServer(Config::instance()->getWifiInfo().port)` function starts the proxy server on the specified port.
- The `BluetoothHandler::instance().connectWithRetry()` function attempts to connect to Bluetooth with retries.
- The `proxyThread->join()` and `btConnectionThread->join()` calls wait for the proxy and Bluetooth connection threads to finish.
- The `UsbManager::instance().disableGadget()` function disables the USB gadget.
- The `sleep(2)` call pauses the execution for a couple of seconds before retrying the connection.
- The `ueventThread->join()` call waits for the uevent monitoring thread to finish.
