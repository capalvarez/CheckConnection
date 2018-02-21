class Status:
    def write_on_file(self, device, file, status):
        file.write(device['name'] + ' ' + device['ip'] + ' ' + status + '\n')

    def write_status(self, device, file):
        pass


class OKStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'OK!')


class FailedStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'FAILED')


class ConnectionRefusedStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'CONNECTION REFUSED')


class DisconnectedStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'DEVICE DISCONNECTED')


class AuthenticationFailedStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, ' AUTHENTICATION FAILED')


class ExpectedFeedbackStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'COMMAND EXPECTED FEEDBACK. TIMEOUT.')


class UnknownDeviceStatus(Status):
    def __init__(self, name):
        self.name = name

    def write_status(self, device, file):
        file.write(self.name + ': FACULTAD U OOMM NO ENCONTRADO \n')


class DeviceTypeUnknownStatus(Status):
    def __init__(self, device_type):
        self.type = device_type

    def write_status(self, device, file):
        self.write_on_file(device, file, 'DEVICE TYPE NOT IN LIST')


class DeviceFileNotFoundStatus(Status):
    def __init__(self, name):
        self.name = name

    def write_status(self, device, file):
        file.write(self.name + ': NO TIENE ARCHIVO DE DISPOSITIVOS ASOCIADO \n')


class SourcesFileNotFoundStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'SOURCES FILE NOT FOUND')


class ConnectionFailedStatus(Status):
    def write_status(self, device, file):
        self.write_on_file(device, file, 'CONNECTION FAILED')
