from devices.devices_types import get_type
from IPy import IP
import re
from default_values import default_port
import warnings
from exceptions.devices_exceptions import DeviceTypeUnknown, DeviceFileNotFound, SourcesFileNotFound


def is_ip_address(value):
    values = value.split()

    for v in values:
        try:
            value = v.split(':')
            IP(value[0])
            return True
        except ValueError:
            continue

    return False


def read_devices(devs_type, file):
    ips = []

    while True:
        next_ip = file.readline().rstrip()

        if is_ip_address(next_ip):
            name, ip, port = separate_source_ip_name(next_ip)
            ips.append({
                'machine': {
                    'ip': ip,
                    'name': name,
                    'port': port
                },
                'type': devs_type,
            })

        if not is_ip_address(next_ip):
            return ips, next_ip


def read_device_file(input_file, facultad):
    devices_to_test = []

    try:
        file = open(input_file, 'r')
    except FileNotFoundError:
        warnings.warn("Device file not found for " + facultad.get_name())
        raise DeviceFileNotFound

    device_type_line = file.readline().rstrip()

    while True:
        if not device_type_line:
            return devices_to_test

        devs_type = get_type(device_type_line)
        devices, device_type_line = read_devices(devs_type, file)
        devices_to_test.extend(devices)


def read_sources_file(sources_file):
    sources = []

    try:
        with open(sources_file, 'r') as file:
            for line in file:
                if line.rstrip():
                    name, ip, port = separate_source_ip_name(line.rstrip())
                    sources.append({
                        'ip': ip,
                        'name': name
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

        if end_ip < len(string):
            return name, ip, int(string[end_ip+1:])
        else:
            return name, ip, default_port


