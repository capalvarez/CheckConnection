from devices.devices_types import get_type
import re
from default_values import default_port, default_destination
import warnings
from exceptions.devices_exceptions import DeviceFileNotFound, SourcesFileNotFound
import ruamel.yaml as yaml


def read_device_file(input_file, facultad):
    try:
        with open(input_file, 'r') as file:
            devices_to_test = yaml.load(file, Loader=yaml.RoundTripLoader)
            devices = []

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
                    'destination': device['Destino'] if 'Destino' in device else default_destination
                })

        return devices
    except FileNotFoundError:
        warnings.warn("Device file not found for " + facultad.get_name())
        raise DeviceFileNotFound


def read_sources_file(sources_file):
    sources = []

    try:
        with open(sources_file, 'r') as file:
            for line in file:
                if line.rstrip():
                    name, ip, vrf = separate_source_ip_name(line.rstrip())
                    sources.append({
                        'ip': ip,
                        'name': name,
                        'vrf': vrf
                    })

        return sources
    except FileNotFoundError:
        warnings.warn("Sources file not found " + sources_file)
        raise SourcesFileNotFound


def separate_source_ip_name(string):
    ip = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}'
                    + '(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')

    match = ip.search(string)
    if match:
        match.group()
        start_ip, end_ip = match.span()
        name = string[:start_ip].rstrip()
        ip = string[start_ip:end_ip]
        vrf = ''

        if end_ip < len(string):
            vrf = string[end_ip + 1:]

        return name, ip, vrf
