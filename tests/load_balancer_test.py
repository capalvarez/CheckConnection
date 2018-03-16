from tests.correct_test import CorrectTest
from exceptions.devices_exceptions import SourcesFileNotFound
import status.statuses as status
from tests.read_from_file import read_partition_interfaces
import re


class LoadBalancerTest(CorrectTest):
    def __init__(self, origin, config):
        CorrectTest.__init__(self, origin, config)

    def obtain_sources(self, status_result):
        controller = self.origin['type']['controller']
        partitions = controller.get_partitions()
        sources = []

        for p in partitions:
            partition_file = self.config['sources_path'] + '/' + p.lower() + '.txt'

            try:
                sources.append({'partition':p, 'interfaces':read_partition_interfaces(partition_file)})
            except SourcesFileNotFound:
                status_result['status'] = status.SourcesFileNotFoundStatus()

        return sources

    def run_single_test(self, source, connection, status_result):
        cmd = 'active-partition ' + source['partition']
        prompt = re.escape('['+source['partition']+']#')
        original_prompt = re.escape(connection.base_prompt)

        connection.send_command_expect(cmd, expect_string=prompt)

        output = []
        for s in source['interfaces']:
            command = self.origin['type']['controller'].ping(s, self.origin['destination'], self.config['pings'], '')
            output.append(connection.send_command_expect(command))

        cmd = 'active-partition shared'
        connection.send_command_expect(cmd, expect_string=original_prompt)

        return output

    def get_test_format(self, source):
        tests = []

        for i in range(0, len(source['results'])):
            tests.append(dict(ip=source['interfaces'][i], name=source['partition'],
                              status=source['results'][i].decide_status()))

        return tests
