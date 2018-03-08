from devices.device import Device
from devices.devices_functions import ping_a_caller, ping_parser_list


class HP(Device):
    def __init__(self):
        Device.__init__(self, ping_a_caller, ping_parser_list)

    def ping(self, source, destination, pings, vrf):
        return self.ping_caller(source, destination, pings)

    def check_syntax(self, output):
        self.check(output, ['Incomplete command found', 'Command not found'],
                   self.incorrect_command)

    def check_ip(self, output):
        self.check(output, ['DNS lookup failed', 'Incorrect input!'],
                   self.invalid_ip)

    def check_source(self, output):
        pass
