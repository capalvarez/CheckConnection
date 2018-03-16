from tests.correct_test import CorrectTest
from exceptions.devices_exceptions import SourcesFileNotFound
import status.statuses as status
from tests.read_from_file import read_sources_file
import warnings


class SwitchTest(CorrectTest):
    def __init__(self, origin, config):
        CorrectTest.__init__(self, origin, config)

    def obtain_sources(self, status_result):
        origin_ip = self.origin['machine']['ip'].replace('.', '-')
        source_file = self.config['sources_path'] + '/' + origin_ip + '.txt'

        try:
            return read_sources_file(source_file)
        except SourcesFileNotFound:
            status_result['status'] = status.SourcesFileNotFoundStatus()

    def run_single_test(self, source, connection, status_result):
        try:
            command = self.origin['type']['controller'].ping(source['ip'], self.origin['destination'],
                                                             self.config['pings'], source['vrf'])
            # print(command)
            output = connection.send_command_expect(command)
            return [output]
        except OSError:
            warnings.warn("Command expected feedback for: " + status_result['machine']['name'] + ' ' +
                          status_result['machine']['ip'])
            status_result['status'] = status.ExpectedFeedbackStatus

    def get_test_format(self, source):
        return [dict(ip=source['ip'], name=source['name'],
                     status=source['results'][0].decide_status())]
