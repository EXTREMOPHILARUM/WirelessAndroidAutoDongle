# `bluetoothProfiles.h`

The `bluetoothProfiles.h` file defines the Bluetooth profiles for the Android Auto Wireless Gateway (AAWG) package.

## Includes

```cpp
#include "bluetoothCommon.h"
```

## BluezProfile Class

The `BluezProfile` class is an abstract base class for Bluetooth profiles. It inherits from the `DBus::Object` class and provides methods for handling profile release, new connections, and disconnections.

### Public Methods

- `virtual void Release() = 0;`
  - Pure virtual method to handle profile release.
- `virtual void NewConnection(DBus::Path path, std::shared_ptr<DBus::FileDescriptor> fd, DBus::Properties fdProperties) = 0;`
  - Pure virtual method to handle new connections.
- `virtual void RequestDisconnection(DBus::Path path) = 0;`
  - Pure virtual method to handle disconnection requests.

### Protected Methods

- `BluezProfile(DBus::Path path);`
  - Constructor that initializes the BluezProfile object.

## AAWirelessProfile Class

The `AAWirelessProfile` class implements the AA Wireless profile. It inherits from the `BluezProfile` class and provides methods for handling profile release, new connections, and disconnections.

### Public Methods

- `static std::shared_ptr<AAWirelessProfile> create(DBus::Path path);`
  - Creates and returns a shared pointer to an `AAWirelessProfile` object.

### Private Methods

- `void Release() override;`
  - Method to handle profile release.
- `void NewConnection(DBus::Path path, std::shared_ptr<DBus::FileDescriptor> fd, DBus::Properties fdProperties) override;`
  - Method to handle new connections.
- `void RequestDisconnection(DBus::Path path) override;`
  - Method to handle disconnection requests.

### Constructor

- `AAWirelessProfile(DBus::Path path);`
  - Constructor that initializes the AA Wireless profile.

## HSPHSProfile Class

The `HSPHSProfile` class implements the HSP Handset profile. It inherits from the `BluezProfile` class and provides methods for handling profile release, new connections, and disconnections.

### Public Methods

- `static std::shared_ptr<HSPHSProfile> create(DBus::Path path);`
  - Creates and returns a shared pointer to an `HSPHSProfile` object.

### Private Methods

- `void Release() override;`
  - Method to handle profile release.
- `void NewConnection(DBus::Path path, std::shared_ptr<DBus::FileDescriptor> fd, DBus::Properties fdProperties) override;`
  - Method to handle new connections.
- `void RequestDisconnection(DBus::Path path) override;`
  - Method to handle disconnection requests.

### Constructor

- `HSPHSProfile(DBus::Path path);`
  - Constructor that initializes the HSP Handset profile.

## Summary

The `bluetoothProfiles.h` file defines the Bluetooth profiles for the AAWG package. It includes the `BluezProfile` class as an abstract base class for Bluetooth profiles, and the `AAWirelessProfile` and `HSPHSProfile` classes, which implement the AA Wireless and HSP Handset profiles, respectively. These classes provide methods for handling profile release, new connections, and disconnections.
