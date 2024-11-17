# `bluetoothHandler.h`

The `bluetoothHandler.h` file defines the `BluetoothHandler` class, which manages the Bluetooth functionality for the Android Auto Wireless Gateway (AAWG) package.

## Includes

```cpp
#include <optional>
#include <thread>

#include "bluetoothCommon.h"
```

## Forward Declarations

The file includes forward declarations for several classes used by the `BluetoothHandler` class.

```cpp
class BluezAdapterProxy;
class AAWirelessProfile;
class HSPHSProfile;
class BLEAdvertisement;
```

## BluetoothHandler Class

The `BluetoothHandler` class manages the Bluetooth functionality for the AAWG package.

### Public Methods

The class provides several public methods for initializing the Bluetooth handler, managing power state, and handling connections with retry logic.

```cpp
class BluetoothHandler {
public:
    static BluetoothHandler& instance();

    void init();
    void powerOn();
    void powerOff();

    std::optional<std::thread> connectWithRetry();
    void stopConnectWithRetry();
```

### Private Methods

The class also includes several private methods for internal use.

```cpp
private:
    BluetoothHandler() {};
    BluetoothHandler(BluetoothHandler const&);
    BluetoothHandler& operator=(BluetoothHandler const&);

    DBus::ManagedObjects getBluezObjects();

    void initAdapter();
    void setPower(bool on);
    void setPairable(bool pairable);
    void exportProfiles();
    void connectDevice();

    void startAdvertising();
    void stopAdvertising();

    void retryConnectLoop();
```

### Private Members

The class defines several private member variables for managing the Bluetooth handler's state.

```cpp
    std::shared_ptr<std::promise<void>> connectWithRetryPromise;

    std::shared_ptr<DBus::Dispatcher> m_dispatcher;
    std::shared_ptr<DBus::Connection> m_connection;
    std::shared_ptr<BluezAdapterProxy> m_adapter;

    std::shared_ptr<AAWirelessProfile> m_aawProfile;
    std::shared_ptr<HSPHSProfile> m_hspProfile;

    std::shared_ptr<BLEAdvertisement> m_leAdvertisement;

    std::string m_adapterAlias;
};
```

## Summary

The `bluetoothHandler.h` file defines the `BluetoothHandler` class, which manages the Bluetooth functionality for the AAWG package. The class provides methods for initializing the Bluetooth handler, managing power state, and handling connections with retry logic. The file also includes forward declarations for several classes used by the `BluetoothHandler` class.
