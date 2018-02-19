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

lock = Lock()
results = {}


def connect_to_device(device, status_results):
    try:
        connection = ConnectHandler(**device)
        return connection
    except ConnectionRefusedError:
        status_results['status'] = status.ConnectionRefusedStatus()
    except OSError:
        status_results['status'] = status.ExpectedFeedbackStatus
    except NetMikoTimeoutException:
        status_results['status'] = status.DisconnectedStatus()
    except NetMikoAuthenticationException:
        status_results['status'] = status.AuthenticationFailedStatus()


def single_test(origin, config):
    device = {
        'device_type': origin['type']['name'],
        'ip': origin['machine']['ip'],
        'username': config['user'],
        'password': config['pswd'],
        'port': origin['machine']['port'],
        'verbose': True
    }

    ping_results = []

    origin_ip = origin['machine']['ip'].replace('.', '-')
    source_file = config['sources_path'] + '/' + origin_ip + '.txt'

    sources = read_sources_file(source_file)
    status_result = {'tests': []}

    connection = connect_to_device(device, status_result)
    if connection:
        if 'delay' in origin['type']:
            device['global_delay_factor'] = origin['type']['delay']
        else:
            device['global_delay_factor'] = 1

        controller = origin['type']['controller']

        for source in sources:
            command = controller.ping(source['ip'], config['destination'], config['pings'])
            output = connection.send_command(command)

            try:
                hits, fails = origin['type']['controller'].parse_ping(output)
                result = (100.0 * hits) / (hits + fails)
                ping_results.append(OKTestStatus(result))

            except PingFailedException as e:
                ping_results.append(e.get_status())

        analyze_results(status_result, ping_results, sources)

        connection.disconnect()

    status_result['machine'] = origin['machine']
    lock.acquire()
    results[origin['facultad']].append(status_result)
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
            file_name, sources_path = s.get_file_name()
            file_path = s.get_base_path() + file_name

            this_config = copy.deepcopy(config)

            this_config['sources_path'] = s.get_complete_sources_path(sources_path)
            list_facultad = read_device_file(file_path, str(s))
            to_check.extend([[t, this_config] for t in list_facultad])

        pool = ThreadPool(config['threads'])
        pool.starmap(single_test, to_check)

        pool.close()
        pool.join()

        if config['measure_time']:
            end_time = time.time()
            print('Tiempo total de prueba: ' + str(end_time - start_time))

        return results

