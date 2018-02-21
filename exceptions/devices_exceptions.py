class DeviceTypeUnknown(Exception):
    def __init__(self, unknown):
        self.unknown = unknown

    def get_unknown_type(self):
        return self.unknown


class DeviceFileNotFound(Exception):
    pass


class SourcesFileNotFound(Exception):
    pass


class UnknownFacultadOrOOMM(Exception):
    pass