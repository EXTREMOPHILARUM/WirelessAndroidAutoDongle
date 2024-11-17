# `bluetoothCommon.h`

The `bluetoothCommon.h` file provides common definitions and utilities for Bluetooth functionality in the Android Auto Wireless Gateway (AAWG) package.

## Includes

```cpp
#include <dbus-cxx.h>
```

## DBus Namespace

The `DBus` namespace is extended with additional type definitions for convenience.

### Type Definitions

- `typedef std::map<std::string, DBus::Variant> Properties;`
  - Represents a map of property names to their values.
- `typedef std::map<std::string, Properties> Interfaces;`
  - Represents a map of interface names to their properties.
- `typedef std::map<DBus::Path, Interfaces> ManagedObjects;`
  - Represents a map of object paths to their interfaces and properties.

## Summary

The `bluetoothCommon.h` file provides common definitions and utilities for Bluetooth functionality in the AAWG package. It includes the necessary DBus headers and extends the `DBus` namespace with additional type definitions for properties, interfaces, and managed objects.
