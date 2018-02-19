from devices.device import Device
from devices.devices_functions import ping_source_ip_caller, ping_parser_dot


class DellForce(Device):
    def __init__(self):
        Device.__init__(self, ping_source_ip_caller, ping_parser_dot)
