import re
import warnings
from exceptions.devices_exceptions import SourcesFileNotFound


def read_partition_interfaces(partition_file):
    interfaces = []
    try:
        with open(partition_file, 'r') as file:
            for line in file:
                interfaces.append(line)

        return interfaces
    except FileNotFoundError:
        warnings.warn("Sources file not found " + partition_file)
        raise SourcesFileNotFound


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
