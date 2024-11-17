from common import Logger

class BluetoothProfiles:
    def __init__(self):
        self.logger = Logger("BluetoothProfiles")
        self.profiles = {}

    def add_profile(self, name, profile):
        self.logger.debug(f"Adding profile: {name}")
        self.profiles[name] = profile

    def get_profile(self, name):
        self.logger.debug(f"Getting profile: {name}")
        return self.profiles.get(name)
