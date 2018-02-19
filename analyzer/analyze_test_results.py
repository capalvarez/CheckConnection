from status.statuses import OKStatus, FailedStatus


def write_results(results, output_file):
    file = open(output_file, 'w')

    for institution_results in results.values():
        for switch in institution_results:
            device = switch['machine']
            switch['status'].write_status(device, file)

            ips = switch['tests']

            for ip in ips:
                ip['status'].write_test(ip, file)

    file.close()


def analyze_results(results, ping_results, sources):
    for i in range(0, len(sources)):
        test = dict(ip=sources[i]['ip'], name=sources[i]['name'],
                    status=ping_results[i].decide_status())

        results['tests'].append(test)

    success = list(map(lambda r: r['status'].isOK(), results['tests']))

    final_result = all(success)
    if final_result:
        results['status'] = OKStatus()
    else:
        results['status'] = FailedStatus()

    return results

