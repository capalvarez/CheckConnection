import os
from netmiko import ConnectHandler
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
from getpass import getpass
import default_values
import argparse
import analyzer.analyze_test_results as analyze
import file_reader.read_from_file as reader

import time

current_path = os.path.dirname(os.path.realpath(__file__))
lock = Lock()


def obtain_ips_to_test(connection):
    output = connection.send_command('show ip inter brie')
    print(output)


def run_test(test, config):
    device = {
        'device_type': test['type'],
        'ip': test['machine']['ip'],
        'username': config['user'],
        'password': config['pswd'],
        'verbose': True
    }

    connection = ConnectHandler(**device)
    results = []

    sources = obtain_ips_to_test(connection)

    for s in sources:
        for c in test['cmds']:
            output = connection.send_command('ping ' + c + ' count ' + config['pings'] + ' source ' + s)
            hits, fails = analyze.analyze_result(output)
            result = (100.0*hits)/(hits+fails)
            results.append(result)

    connection.disconnect()

    analyze.write_results(test['machine'], results, test['cmds'], config['output'])


def run_test_parallel(config, number_threads):
    open(config['output'], 'w+')
    tests = reader.read_test_file(config['input'])
    pool = ThreadPool(number_threads)

    tests_args = [[t, config] for t in tests]
    start = time.time()
    pool.starmap(run_test, tests_args)

    pool.close()
    pool.join()

    print("Execution time = {0:.5f}".format(time.time() - start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--packets', nargs='?', default=default_values.number_pings)
    parser.add_argument('--threads', nargs='?', default=default_values.default_threads)

    args = parser.parse_args()

    config = {
        'pings': args.packets,
    }

    run_test_parallel(config, args.threads)
