from tests.test import Test
from exceptions.exceptions import PingFailedException
from status.test_status import OKTestStatus
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import warnings
import status.statuses as status
import paramiko
from status.statuses import OKStatus, FailedStatus


class CorrectTest(Test):
    def __init__(self, origin, config):
        self.origin = origin
        self.config = config

    def run_test(self, status_result):
        try:
            device = {
                'device_type': self.origin['type']['name'],
                'ip': self.origin['machine']['ip'],
                'username': self.config['user'],
                'password': self.config['pswd'],
                'secret': self.config['pswd'],
                'port': self.origin['machine']['port'],
                'verbose': True
            }

            status_result['machine'] = self.origin['machine']
            sources = self.obtain_sources(status_result)

            if sources:
                connection = self.connect_to_device(device, status_result)
                if connection:
                    connection.enable()

                    for source in sources:
                        output = self.run_single_test(source, connection, status_result)
                        source_results = []

                        for o in output:
                            try:
                                hits, fails = self.origin['type']['controller'].parse_ping(o)
                                result = (100.0 * hits) / (hits + fails)
                                source_results.append(OKTestStatus(result))
                            except PingFailedException as e:
                                source_results.append(e.get_status())

                        source['results'] = source_results
                    self.analyze_results(status_result, sources)

                    connection.exit_enable_mode()
                    connection.disconnect()
        except (paramiko.SSHException, EOFError):
                warnings.warn("Could not connect to: " + status_result['machine']['name'] + ' ' +
                              status_result['machine']['ip'])
                status_result['status'] = status.ConnectionFailedStatus()
                status_result['test_instance'] = self

    def obtain_sources(self, status_result):
        pass

    def run_single_test(self, source, connection, status_result):
        pass

    def analyze_results(self, results, sources):
        for i in range(0, len(sources)):
            test = self.get_test_format(sources[i])

            results['tests'].extend(test)

        success = list(map(lambda r: r['status'].isOK(), results['tests']))

        final_result = all(success)
        if final_result:
            results['status'] = OKStatus()
        else:
            results['status'] = FailedStatus()

        return results

    def get_test_format(self, source):
        pass

    def connect_to_device(self, device, status_result):
        try:
            connection = ConnectHandler(**device)
            return connection
        except ConnectionRefusedError:
            warnings.warn("Connection refused: " + status_result['machine']['name'] + ' ' + status_result['machine']['ip'])
            status_result['status'] = status.ConnectionRefusedStatus()
        except NetMikoTimeoutException:
            warnings.warn("Connection timeout: " + status_result['machine']['name'] + ' ' +
                          status_result['machine']['ip'])
            status_result['status'] = status.DisconnectedStatus()
        except NetMikoAuthenticationException:
            warnings.warn("Authentication failed: " + status_result['machine']['name'] + ' ' +
                          status_result['machine']['ip'])
            status_result['status'] = status.AuthenticationFailedStatus()
        except UnicodeDecodeError:
            warnings.warn("Connection failed: " + status_result['machine']['name'] + ' ' +
                          status_result['machine']['ip'])
            status_result['status'] = status.ConnectionFailedStatus()
            status_result['test_instance'] = self




