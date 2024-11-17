# `bluetoothAdvertisement.cpp`

The `bluetoothAdvertisement.cpp` file implements the Bluetooth Low Energy (BLE) advertisement functionality for the Android Auto Wireless Gateway (AAWG) package.

## Includes

```cpp
#include <stdio.h>

#include "common.h"
#include "bluetoothAdvertisement.h"
```

## Constants

The file defines a constant for the BlueZ LE Advertisement interface.

```cpp
static constexpr const char* INTERFACE_BLUEZ_LE_ADVERTISEMENT = "org.bluez.LEAdvertisement1";
```

## BLEAdvertisement Class

The `BLEAdvertisement` class represents a BLE advertisement object. It inherits from the `DBus::Object` class.

### Static Create Method

The `create` method is a static factory method that creates and returns a shared pointer to a `BLEAdvertisement` object.

```cpp
/* static */ std::shared_ptr<BLEAdvertisement> BLEAdvertisement::create(DBus::Path path) {
    return std::shared_ptr<BLEAdvertisement>(new BLEAdvertisement(path));
}
```

### Constructor

The constructor initializes the BLE advertisement object and sets up the D-Bus methods and properties.

```cpp
BLEAdvertisement::BLEAdvertisement(DBus::Path path): DBus::Object(path) {
    this->create_method<void(void)>(INTERFACE_BLUEZ_LE_ADVERTISEMENT, "Release", sigc::mem_fun(*this, &BLEAdvertisement::Release));

    type = this->create_property<std::string>(INTERFACE_BLUEZ_LE_ADVERTISEMENT, "Type", DBus::PropertyAccess::ReadOnly);
    serviceUUIDs = this->create_property<std::vector<std::string>>(INTERFACE_BLUEZ_LE_ADVERTISEMENT, "ServiceUUIDs");
    localName = this->create_property<std::string>(INTERFACE_BLUEZ_LE_ADVERTISEMENT, "LocalName");
}
```

### Release Method

The `Release` method is called when the BLE advertisement is released. It logs a message indicating that the advertisement has been released.

```cpp
void BLEAdvertisement::Release() {
    Logger::instance()->info("Bluetooth LE Advertisement released\n");
}
```

## Summary

The `bluetoothAdvertisement.cpp` file implements the BLE advertisement functionality for the AAWG package. It defines the `BLEAdvertisement` class, which represents a BLE advertisement object and provides methods for creating and releasing the advertisement. The class also sets up the necessary D-Bus methods and properties for the advertisement.
