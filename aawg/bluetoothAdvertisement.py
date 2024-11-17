import dbus

LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

class BluetoothAdvertisement(dbus.service.Object):
    PATH_BASE = '/org/bluez/example/advertisement'

    def __init__(self, bus, index, advertising_type):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.advertising_type = advertising_type
        self.service_uuids = None
        self.manufacturer_data = None
        self.solicit_uuids = None
        self.type = advertising_type

        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        properties = dict()
        properties['Type'] = self.type
        if self.service_uuids:
            properties['ServiceUUIDs'] = dbus.Array(self.service_uuids)
        if self.manufacturer_data:
            properties['ManufacturerData'] = dbus.Dictionary(self.manufacturer_data,
                                                            signature='ayv')
        if self.solicit_uuids:
            properties['SolicitUUIDs'] = dbus.Array(self.solicit_uuids)

        return {LE_ADVERTISEMENT_IFACE: properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(LE_ADVERTISEMENT_IFACE,
                         in_signature='s',
                         out_signature='')
    def Release(self, object_path):
        print(f'Released {object_path}')
