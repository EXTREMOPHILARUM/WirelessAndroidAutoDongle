# `WifiInfoResponse.proto`

The `WifiInfoResponse.proto` file defines the protocol buffer message for WiFi information response. It includes the following components:

## Enums

### `AccessPointType`
The `AccessPointType` enum defines the type of access point. It has the following values:
- `STATIC` (0): Static access point.
- `DYNAMIC` (1): Dynamic access point.

### `SecurityMode`
The `SecurityMode` enum defines the security mode of the WiFi network. It has the following values:
- `UNKNOWN_SECURITY_MODE` (0): Unknown security mode.
- `OPEN` (1): Open network.
- `WEP_64` (2): WEP 64-bit encryption.
- `WEP_128` (3): WEP 128-bit encryption.
- `WPA_PERSONAL` (4): WPA Personal encryption.
- `WPA2_PERSONAL` (8): WPA2 Personal encryption.
- `WPA_WPA2_PERSONAL` (12): WPA/WPA2 Personal encryption.
- `WPA_ENTERPRISE` (20): WPA Enterprise encryption.
- `WPA2_ENTERPRISE` (24): WPA2 Enterprise encryption.
- `WPA_WPA2_ENTERPRISE` (28): WPA/WPA2 Enterprise encryption.

## Message

### `WifiInfoResponse`
The `WifiInfoResponse` message contains the following fields:
- `required string ssid = 1`: The SSID of the WiFi network.
- `required string key = 2`: The key (password) of the WiFi network.
- `required string bssid = 3`: The BSSID of the WiFi network.
- `required SecurityMode security_mode = 4`: The security mode of the WiFi network.
- `required AccessPointType access_point_type = 5`: The type of access point.
