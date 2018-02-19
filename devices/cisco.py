from devices.device import Device
from devices.devices_functions import ping_source_repeat_caller, ping_parser_dot


class Cisco(Device):
    def __init__(self):
        Device.__init__(self, ping_source_repeat_caller, ping_parser_dot)