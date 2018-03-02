from devices.devices_functions import ping_source_repeat_caller, ping_parser_list
from devices.device import Device


class DellN(Device):
    def __init__(self):
        Device.__init__(self, ping_source_repeat_caller, ping_parser_list)

    def ping(self, source, destination, pings, vrf):
        return self.ping_caller(source, destination, pings, vrf)

    def check_syntax(self, output):
        self.check(output, ['Invalid input detected', 'Command not found / Incomplete command'],
                   self.incorrect_command)

    def check_ip(self, output):
        self.check(output, ['DNS lookup failed', 'Incorrect input!'],
                   self.invalid_ip)

    def check_source(self, output):
        self.check(output, ['The ping source is invalid'], self.invalid_source)
