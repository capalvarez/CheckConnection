from devices.device import Device
from devices.devices_functions import ping_source_ip_caller, ping_parser_dot


class DellForce(Device):
    def __init__(self):
        Device.__init__(self, ping_source_ip_caller, ping_parser_dot)

    def check_syntax(self, output):
        self.check(output, ['Error: Invalid input'], self.incorrect_command)

    def check_ip(self, output):
        self.check(output, ['Error: Unrecognized host or address'],
                   self.invalid_ip)

    def check_source(self, output):
        self.check(output, ['Invalid source IP address'], self.invalid_source)