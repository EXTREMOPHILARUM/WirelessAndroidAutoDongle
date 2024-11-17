# `bluetoothHandler.cpp`

The `bluetoothHandler.cpp` file implements the Bluetooth handler functionality for the Android Auto Wireless Gateway (AAWG) package.

## Includes

```cpp
#include <stdio.h>

#include "common.h"
#include "bluetoothHandler.h"
#include "bluetoothProfiles.h"
#include "bluetoothAdvertisement.h"
```

## Constants

The file defines several constants for BlueZ interfaces, object paths, and UUIDs.

```cpp
static constexpr const char* ADAPTER_ALIAS_PREFIX = "WirelessAADongle-";
static constexpr const char* ADAPTER_ALIAS_DONGLE_PREFIX = "AndroidAuto-Dongle-";

static constexpr const char* BLUEZ_BUS_NAME = "org.bluez";
static constexpr const char* BLUEZ_ROOT_OBJECT_PATH = "/";
static constexpr const char* BLUEZ_OBJECT_PATH = "/org/bluez";

static constexpr const char* INTERFACE_BLUEZ_ADAPTER = "org.bluez.Adapter1";
static constexpr const char* INTERFACE_BLUEZ_LE_ADVERTISING_MANAGER = "org.bluez.LEAdvertisingManager1";

static constexpr const char* INTERFACE_BLUEZ_DEVICE = "org.bluez.Device1";
static constexpr const char* INTERFACE_BLUEZ_PROFILE_MANAGER = "org.bluez.ProfileManager1";

static constexpr const char* LE_ADVERTISEMENT_OBJECT_PATH = "/com/aawgd/bluetooth/advertisement";

static constexpr const char* AAWG_PROFILE_OBJECT_PATH = "/com/aawgd/bluetooth/aawg";
static constexpr const char* AAWG_PROFILE_UUID = "4de17a00-52cb-11e6-bdf4-0800200c9a66";

static constexpr const char* HSP_HS_PROFILE_OBJECT_PATH = "/com/aawgd/bluetooth/hsp";
static constexpr const char* HSP_AG_UUID = "00001112-0000-1000-8000-00805f9b34fb";
static constexpr const char* HSP_HS_UUID = "00001108-0000-1000-8000-00805f9b34fb";
```

## BluezAdapterProxy Class

The `BluezAdapterProxy` class represents a proxy for the BlueZ adapter. It inherits from the `DBus::ObjectProxy` class.

### Constructor

The constructor initializes the BlueZ adapter proxy and sets up the D-Bus properties and methods.

```cpp
class BluezAdapterProxy: private DBus::ObjectProxy {
    BluezAdapterProxy(std::shared_ptr<DBus::Connection> conn, DBus::Path path): DBus::ObjectProxy(conn, BLUEZ_BUS_NAME, path) {
        alias = this->create_property<std::string>(INTERFACE_BLUEZ_ADAPTER, "Alias");
        powered = this->create_property<bool>(INTERFACE_BLUEZ_ADAPTER, "Powered");
        discoverable = this->create_property<bool>(INTERFACE_BLUEZ_ADAPTER, "Discoverable");
        pairable = this->create_property<bool>(INTERFACE_BLUEZ_ADAPTER, "Pairable");

        registerAdvertisement = this->create_method<void(DBus::Path, DBus::Properties)>(INTERFACE_BLUEZ_LE_ADVERTISING_MANAGER, "RegisterAdvertisement");
        unregisterAdvertisement = this->create_method<void(DBus::Path)>(INTERFACE_BLUEZ_LE_ADVERTISING_MANAGER, "UnregisterAdvertisement");
    }
```

### Static Create Method

The `create` method is a static factory method that creates and returns a shared pointer to a `BluezAdapterProxy` object.

```cpp
public:
    static std::shared_ptr<BluezAdapterProxy> create(std::shared_ptr<DBus::Connection> conn, DBus::Path path)
    {
      return std::shared_ptr<BluezAdapterProxy>(new BluezAdapterProxy(conn, path));
    }
```

### Properties and Methods

The class defines several properties and methods for interacting with the BlueZ adapter.

```cpp
    std::shared_ptr<DBus::PropertyProxy<std::string>> alias;
    std::shared_ptr<DBus::PropertyProxy<bool>> powered;
    std::shared_ptr<DBus::PropertyProxy<bool>> discoverable;
    std::shared_ptr<DBus::PropertyProxy<bool>> pairable;

    std::shared_ptr<DBus::MethodProxy<void(DBus::Path, DBus::Properties)>> registerAdvertisement;
    std::shared_ptr<DBus::MethodProxy<void(DBus::Path)>> unregisterAdvertisement;
};
```

## BluetoothHandler Class

The `BluetoothHandler` class manages the Bluetooth functionality for the AAWG package.

### Singleton Instance

The `instance` method returns a singleton instance of the `BluetoothHandler` class.

```cpp
BluetoothHandler& BluetoothHandler::instance() {
    static BluetoothHandler instance;
    return instance;
}
```

### Initialization

The `init` method initializes the Bluetooth handler, sets up the D-Bus connection, and exports the Bluetooth profiles.

```cpp
void BluetoothHandler::init() {
    m_dispatcher = DBus::StandaloneDispatcher::create();
    m_connection = m_dispatcher->create_connection( DBus::BusType::SYSTEM );

    std::string adapterAliasPrefix = (Config::instance()->getConnectionStrategy() == ConnectionStrategy::DONGLE_MODE) ? ADAPTER_ALIAS_DONGLE_PREFIX : ADAPTER_ALIAS_PREFIX;

    m_adapterAlias = adapterAliasPrefix + Config::instance()->getUniqueSuffix();

    initAdapter();
    exportProfiles();
}
```

### Power Management

The `powerOn` and `powerOff` methods manage the power state of the Bluetooth adapter.

```cpp
void BluetoothHandler::powerOn() {
    if (!m_adapter) {
        return;
    }

    setPower(true);
    setPairable(true);

    if (Config::instance()->getConnectionStrategy() == ConnectionStrategy::DONGLE_MODE) {
        startAdvertising();
    }
}

void BluetoothHandler::powerOff() {
    if (!m_adapter) {
        return;
    }

    if (Config::instance()->getConnectionStrategy() == ConnectionStrategy::DONGLE_MODE) {
        stopAdvertising();
    }
    setPower(false);
}
```

### Connection Management

The `connectWithRetry` and `stopConnectWithRetry` methods manage the Bluetooth connection with retry logic.

```cpp
std::optional<std::thread> BluetoothHandler::connectWithRetry() {
    if (!m_adapter) {
        return std::nullopt;
    }

    connectWithRetryPromise = std::make_shared<std::promise<void>>();
    return std::thread(&BluetoothHandler::retryConnectLoop, this);
}

void BluetoothHandler::stopConnectWithRetry() {
    if (connectWithRetryPromise) {
        connectWithRetryPromise->set_value();
    }
}
```

## Summary

The `bluetoothHandler.cpp` file implements the Bluetooth handler functionality for the AAWG package. It defines the `BluetoothHandler` class, which manages the Bluetooth adapter, profiles, and connections. The file also includes the `BluezAdapterProxy` class, which provides a proxy for interacting with the BlueZ adapter. The `BluetoothHandler` class provides methods for initializing the Bluetooth handler, managing power state, and handling connections with retry logic.
