class Device:
    def __init__(self, ping, parser):
        self.ping_caller = ping
        self.ping_parser = parser

    def ping(self, source, destination, pings):
        return self.ping_caller(source, destination, pings)

    def parse_ping(self, ping_result):
        return self.ping_parser(ping_result)