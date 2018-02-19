from devices.device import Device
from devices.devices_functions import ping_vrf, ping_parser_dot


class WithVRF(Device):
    def __init__(self):
        Device.__init__(self, ping_vrf, ping_parser_dot)
