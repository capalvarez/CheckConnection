import re
from exceptions.exceptions import PingFailedException


#HP
def ping_a_caller(source, destination, pings):
    return 'ping ' + ' -a ' + source + ' -c ' + pings + ' ' + destination


#Dell
def ping_source_ip_caller(source, destination, pings, vrf):
    return 'ping vrf ' + vrf + ' ' + destination + ' count ' + pings + ' source ip ' + source


#Cisco
def ping_source_repeat_caller(source, destination, pings, vrf):
    if vrf:
        return 'ping vrf ' + vrf + ' ' + destination + ' repeat ' + pings + ' source ' + source
    else:
        return 'ping ' + destination + ' repeat ' + pings + ' source ' + source


def ping_parser_dot(output):
    results = re.compile('\n[\.!.]+\n')
    match_results = results.search(output)

    if match_results:
        match_results.group()
        start, end = match_results.span()
        total_packets = output[start:end].replace('\n', '')
        hits = total_packets.count('!')
        fails = total_packets.count('.')

        return hits, fails
    else:
        raise PingFailedException


def ping_parser_list(output):
    total = re.compile('\d+ packet\(?s\)? transmitted')
    hits = re.compile('\d+ packet\(?s\)? received')

    match_total = total.search(output)
    match_hits = hits.search(output)

    total_packets = 0
    hits_packets = 0

    if match_total and match_hits:
        match_total.group()
        start_total, end_total = match_total.span()
        total_packets = int(output[start_total:end_total].rstrip().split()[0])

        match_hits.group()
        start_hits, end_hits = match_hits.span()
        hits_packets = int(output[start_hits:end_hits].rstrip().split()[0])

        return hits_packets, (total_packets - hits_packets)
    else:
        raise PingFailedException


