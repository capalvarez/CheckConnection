from devices.device import Device
from devices.devices_functions import ping_source_repeat_caller, ping_parser_dot


class Cisco(Device):
    def __init__(self, ping=ping_source_repeat_caller):
        Device.__init__(self, ping, ping_parser_dot)

    def check_syntax(self, output):
        self.check(output, ['Invalid input detected'], self.incorrect_command)

    def check_ip(self, output):
        self.check(output, ['Unrecognized host or address'], self.invalid_ip)

    def check_source(self, output):
        self.check(output, ['Invalid source address'], self.invalid_source)
