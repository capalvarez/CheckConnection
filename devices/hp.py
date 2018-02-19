from devices.device import Device
from devices.devices_functions import ping_a_caller, ping_parser_list


class HP(Device):
    def __init__(self):
        Device.__init__(self, ping_a_caller, ping_parser_list)