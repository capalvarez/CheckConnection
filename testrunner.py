from read_from_file import read_device_file, read_sources_file
from analyzer.analyze_test_results import analyze_results
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import type_selected as s
import copy
import time
import status.statuses as status
from exceptions.exceptions import PingFailedException
from status.test_status import OKTestStatus
from exceptions.devices_exceptions import DeviceFileNotFound, SourcesFileNotFound, DeviceTypeUnknown
import warnings


lock = Lock()
results = {}


class CorrectTest:
    def __init__(self, origin, config):
        self.origin = origin
        self.config = config

    def run_test(self, status_result):
        device = {
            'device_type': self.origin['type']['name'],
            'ip': self.origin['machine']['ip'],
            'username': self.config['user'],
            'password': self.config['pswd'],
            'port': self.origin['machine']['port'],
            'verbose': True
        }

        ping_results = []

        origin_ip = self.origin['machine']['ip'].replace('.', '-')
        source_file = self.config['sources_path'] + '/' + origin_ip + '.txt'

        status_result['machine'] = self.origin['machine']
        sources = obtain_test_ips(source_file, status_result)

        if sources:
            connection = connect_to_device(device, status_result)
            if connection:
                controller = self.origin['type']['controller']

                for source in sources:
                    command = controller.ping(source['ip'], self.config['destination'], self.config['pings'],
                                              source['vrf'])
                    output = connection.send_command_expect(command)

                    try:
                        hits, fails = self.origin['type']['controller'].parse_ping(output)
                        result = (100.0 * hits) / (hits + fails)
                        ping_results.append(OKTestStatus(result))
                    except PingFailedException as e:
                        ping_results.append(e.get_status())

                analyze_results(status_result, ping_results, sources)
                connection.disconnect()


class FailedTest:
    def __init__(self, status):
        self.status = status

    def run_test(self, status_result):
        status_result['status'] = self.status


def connect_to_device(device, status_result):
    try:
        connection = ConnectHandler(**device)
        return connection
    except ConnectionRefusedError:
        warnings.warn("Connection refused: " + status_result['machine']['name'] + ' ' + status_result['machine']['ip'])
        status_result['status'] = status.ConnectionRefusedStatus()
    except OSError:
        warnings.warn("Command expected feedback for: " + status_result['machine']['name'] + ' ' +
                      status_result['machine']['ip'])
        status_result['status'] = status.ExpectedFeedbackStatus
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


def obtain_test_ips(source_file, status_result):
    try:
        return read_sources_file(source_file)
    except SourcesFileNotFound:
        status_result['status'] = status.SourcesFileNotFoundStatus()


def single_test(test, facultad):
    status_result = {'tests': [], 'machine': {}}
    test.run_test(status_result)

    lock.acquire()
    results[facultad].append(status_result)
    lock.release()


class TestRunner:
    def __init__(self, controller):
        self.selected = s.TypeSelected()
        self.results = []
        self.controller = controller

    def add_facultad(self, selected):
        self.selected.add_facultad(selected)

    def add_oomm(self, selected):
        self.selected.add_oomm(selected)

    def add_facultades(self, selected):
        self.selected.add_facultades(selected)

    def add_oomms(self, selected):
        self.selected.add_oomms(selected)

    def add_datacenter(self, selected):
        self.selected.add_datacenter(selected)

    def add_datacenters(self, selected):
        self.selected.add_datacenters(selected)

    def get_selected(self):
        return str(self.selected)

    def delete_selected(self):
        self.selected.clear()

    def run_selected_tests(self, config):
        to_check = []
        start_time = 0

        if config['measure_time']:
            start_time = time.time()

        for s in self.selected.get_all():
            results[str(s)] = []
            try:
                file_name, sources_path = self.controller.get_file_name(s)
                file_path = s.get_base_path() + file_name

                this_config = copy.deepcopy(config)

                this_config['sources_path'] = s.get_complete_sources_path(sources_path)
                list_facultad = read_device_file(file_path, s)
                to_check.extend([(CorrectTest(t, this_config), str(s)) for t in list_facultad])
            except DeviceFileNotFound:
                warnings.warn("Facultad o OOMM no tiene archivo asociado")
                to_check.append((FailedTest(status.DeviceFileNotFoundStatus(s.get_name())), str(s)))
            except DeviceTypeUnknown as e:
                warnings.warn("Tipo de dispositivo no conocido")
                to_check.append((FailedTest(status.DeviceTypeUnknownStatus(e.get_unknown_type())), str(s)))

        pool = ThreadPool(config['threads'])
        pool.starmap(single_test, to_check)

        pool.close()
        pool.join()

        if config['measure_time']:
            end_time = time.time()
            print('Tiempo total de prueba: ' + str(end_time - start_time))

        return results

