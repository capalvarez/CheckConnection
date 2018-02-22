class Status:
    def __init__(self, status):
        self.status = status

    def write_status(self, device, file):
        file.write(device['name'] + ' ' + device['ip'] + ' ' + self.status + '\n')

    def print_status(self, hide):
        return self.status


class OKStatus(Status):
    def __init__(self):
        Status.__init__(self, 'OK!')

    def print_status(self, hide):
        if not hide:
            return self.status


class FailedStatus(Status):
    def __init__(self):
        Status.__init__(self, 'FAILED')


class ConnectionRefusedStatus(Status):
    def __init__(self):
        Status.__init__(self, 'CONNECTION REFUSED')


class DisconnectedStatus(Status):
    def __init__(self):
        Status.__init__(self, 'DEVICE DISCONNECTED')


class AuthenticationFailedStatus(Status):
    def __init__(self):
        Status.__init__(self, 'AUTHENTICATION FAILED')


class ExpectedFeedbackStatus(Status):
    def __init__(self):
        Status.__init__(self, 'COMMAND EXPECTED FEEDBACK. TIMEOUT.')


class DeviceTypeUnknownStatus(Status):
    def __init__(self, device_type):
        Status.__init__(self, 'DEVICE TYPE NOT IN LIST')
        self.type = device_type


class DeviceFileNotFoundStatus(Status):
    def __init__(self, name):
        Status.__init__(self, 'NO TIENE ARCHIVO DE DISPOSITIVOS ASOCIADO')
        self.name = name

    def write_status(self, device, file):
        file.write(self.name + ': NO TIENE ARCHIVO DE DISPOSITIVOS ASOCIADO \n')


class SourcesFileNotFoundStatus(Status):
    def __init__(self):
        Status.__init__(self, 'SOURCES FILE NOT FOUND')


class ConnectionFailedStatus(Status):
    def __init__(self):
        Status.__init__(self, 'CONNECTION FAILED')