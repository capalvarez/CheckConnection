from devices.device import Device
from devices.devices_functions import ping_parser_list, ping_reverse_order
from tests.load_balancer_test import LoadBalancerTest


class A10(Device):
    def __init__(self):
        Device.__init__(self, ping_reverse_order, ping_parser_list)
        self.partitions = []

    def ping(self, source, destination, pings, vrf):
        return self.ping_caller(source, destination, pings)

    def check_syntax(self, output):
        self.check(output, ['Incomplete command', 'Unrecognized command'],
                   self.incorrect_command)

    def check_ip(self, output):
        self.check(output, ['unknown host'], self.invalid_ip)

    def check_source(self, output):
        pass

    def get_partitions(self):
        return self.partitions

    def set_extras(self, device):
        self.partitions = device['Particiones']

    def get_correct_test(self, device, config):
        return LoadBalancerTest(device, config)