from devices.devices_types import get_type
from IPy import IP


def is_ip_address(value):
    values = value.split()

    for v in values:
        try:
            IP(v)
            return True
        except ValueError:
            continue

    return False


def read_devices(devs_type, f):
    ips = []
    next_ip = f.readline().rstrip()

    while True:
        if is_ip_address(next_ip):
            ip = next_ip.split()
            cmds, next_ip = read_ip(f)
            ips.append({
                'machine': {
                    'ip': ip[1],
                    'name': ip[0]
                },
                'type': devs_type,
                'cmds': cmds
            })

        if not is_ip_address(next_ip):
            return ips, next_ip


def read_ip(f):
    cmds = []

    while True:
        line = f.readline()
        if line.startswith('#'):
            cmds.append(line[1:].strip())
        else:
            return cmds, line.rstrip()


def read_test_file(input_file):
    devices_to_test = []
    file = open(input_file, 'r')

    device_type_line = file.readline().rstrip()

    while True:
        if not device_type_line:
            return devices_to_test

        devs_type = get_type(device_type_line)
        devices, device_type_line = read_devices(devs_type, file)
        devices_to_test.extend(devices)
