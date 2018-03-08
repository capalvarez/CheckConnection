from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
import type_selected as s
import copy
import time
import status.statuses as status
from exceptions.devices_exceptions import DeviceFileNotFound, DeviceTypeUnknown
import warnings
from tests.failed_test import FailedTest
import ruamel.yaml as yaml
from devices.devices_types import get_type
from default_values import default_port
import time


lock = Lock()
results = {}


def read_device_file(input_file, facultad, destination):
    try:
        with open(input_file, 'r') as file:
            devices_to_test = yaml.load(file, Loader=yaml.RoundTripLoader)
            devices = []

            if not devices_to_test:
                return devices

            for k in devices_to_test.keys():
                device = devices_to_test[k]
                device_type = get_type(device['Tipo'])

                devices.append({
                    'machine': {
                        'ip': device['IP'],
                        'name': k,
                        'port': device['Puerto'] if 'Puerto' in device else default_port
                    },
                    'type': device_type,
                    'destination': device['Destino'] if 'Destino' in device else destination,
                    'extras': device_type['controller'].set_extras(device)
                })

        return devices
    except FileNotFoundError:
        warnings.warn("Device file not found for " + facultad.get_name())
        raise DeviceFileNotFound


def single_test(test, facultad):
    status_result = {'tests': [], 'machine': {}}
    test.run_test(status_result)

    lock.acquire()
    print('Saving results for ' + facultad)
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
                list_facultad = read_device_file(file_path, s, config['destination'])

                for t in list_facultad:
                    test = t['type']['controller'].get_correct_test(t, this_config)

                to_check.extend([(test, str(s)) for t in list_facultad])
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
        end_time = time.time()

        if config['repeat_failures']:
            failures_repetitions = 0
            repeat_config = config['repetitions_config']

            if repeat_config['repetitions'] > failures_repetitions:
                connection_failed = list(filter(lambda x: x['status'].needs_repeat(), results.values()))
                time.sleep(repeat_config['wait_time'])

                pool = ThreadPool(config['threads'])
                pool.starmap(single_test, connection_failed)

                pool.close()
                pool.join()

        if config['measure_time']:
            print('Tiempo total de prueba: ' + str(end_time - start_time))

        return results

