from exceptions.exceptions import PingFailedException, IncorrectPingFormat, InvalidIPSource, InvalidIPAddress, \
    ProblemWithPing
import re
from tests.switch_test import SwitchTest


class Device:
    def __init__(self, ping, parser):
        self.ping_caller = ping
        self.ping_parser = parser

    def parse_ping(self, ping_result):
        try:
            return self.ping_parser(ping_result)
        except PingFailedException:
            self.check_syntax(ping_result)
            self.check_source(ping_result)
            self.check_ip(ping_result)
            raise ProblemWithPing

    def check_syntax(self, output):
        pass

    def check_source(self, output):
        pass

    def check_ip(self, output):
        pass

    def incorrect_command(self):
        raise IncorrectPingFormat

    def invalid_source(self):
        raise InvalidIPSource

    def invalid_ip(self):
        raise InvalidIPAddress

    def check(self, output, regex_patterns, response):
        for regex in regex_patterns:
            error = re.compile(regex)
            error_results = error.search(output)

            if error_results:
                response()

    def set_extras(self, device):
        pass

    def get_correct_test(self, device, config):
        return SwitchTest(device, config)
