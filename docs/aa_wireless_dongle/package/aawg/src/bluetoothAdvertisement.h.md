# `bluetoothAdvertisement.h`

The `bluetoothAdvertisement.h` file defines the `BLEAdvertisement` class, which represents a Bluetooth Low Energy (BLE) advertisement object for the Android Auto Wireless Gateway (AAWG) package.

## Includes

```cpp
#include "bluetoothCommon.h"
```

## BLEAdvertisement Class

The `BLEAdvertisement` class inherits from the `DBus::Object` class and provides methods and properties for managing BLE advertisements.

### Public Methods

- `static std::shared_ptr<BLEAdvertisement> create(DBus::Path path);`
  - Creates and returns a shared pointer to a `BLEAdvertisement` object.

### Public Properties

- `std::shared_ptr<DBus::Property<std::string>> type;`
  - Represents the type of the BLE advertisement.
- `std::shared_ptr<DBus::Property<std::vector<std::string>>> serviceUUIDs;`
  - Represents the service UUIDs of the BLE advertisement.
- `std::shared_ptr<DBus::Property<std::string>> localName;`
  - Represents the local name of the BLE advertisement.

### Protected Methods

- `BLEAdvertisement(DBus::Path path);`
  - Constructor that initializes the BLE advertisement object.
- `void Release();`
  - Method called when the BLE advertisement is released.

## Summary

The `bluetoothAdvertisement.h` file defines the `BLEAdvertisement` class, which provides methods and properties for managing BLE advertisements in the AAWG package. The class inherits from the `DBus::Object` class and includes methods for creating and releasing the advertisement, as well as properties for the advertisement type, service UUIDs, and local name.
