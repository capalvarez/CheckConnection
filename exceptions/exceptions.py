from status.test_status import InvalidIPAddressStatus, IncorrectPingFormatStatus, InvalidIPSourceStatus, PingFailed


class PingFailedException(Exception):
    def get_status(self):
        pass


class InvalidIPAddress(PingFailedException):
    def get_status(self):
        return InvalidIPAddressStatus()


class IncorrectPingFormat(PingFailedException):
    def get_status(self):
        return IncorrectPingFormatStatus()


class InvalidIPSource(PingFailedException):
    def get_status(self):
        return InvalidIPSourceStatus()


class ProblemWithPing(PingFailedException):
    def get_status(self):
        return PingFailed()
