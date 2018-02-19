import itertools
import default_values


def write_results(results, output_file):
    file = open(output_file, 'w')

    for institution_results in results.values():
        for switch in institution_results:
            print(switch)

            device = switch['machine']
            if switch['status'] == 'DISCONNECTED':
                file.write(device['name'] + ' ' + device['ip'] + ' CONNECT FAILED \n')
                continue

            if switch['status'] == 'CONNECTION REFUSED':
                file.write(device['name'] + ' ' + device['ip'] + ' CONNECT REFUSED \n')
                continue

            ips = switch['tests']

            if switch['status'] == 'OK':
                file.write(device['name'] + ' ' + device['ip'] + ' OK! \n')
            else:
                file.write(device['name'] + ' ' + device['ip'] + ' FAILED \n')

            for i in range(0, len(ips)):
                if not ips[i]['status'] == 'OK':
                    file.write('\t' + ips[i]['name'] + ' ' + ips[i]['ip'] + ' ' + str(ips[i]['hits']) +
                               '% TESTS SUCCESSFUL \n')
                else:
                    file.write('\t' + ips[i]['name'] + ' ' + ips[i]['ip'] + ' OK! \n')

    file.close()


def analyze_results(ping_results, sources):
    results = {}
    success = list(map(lambda r: r >= default_values.success_threshold, ping_results))

    final_result = all(success)
    if final_result:
        results['status'] = 'OK'
    else:
        results['status'] = 'FAILED'

    results['tests'] = []

    for i in range(0, len(sources)):
        test = {'ip': sources[i]['ip'],
                'name': sources[i]['name'],
                'hits': 100.0}

        if success[i]:
            test['status'] = 'OK'
        else:
            test['status'] = 'FAILED'
            test['hits'] = ping_results[i]

        results['tests'].append(test)

    return results

