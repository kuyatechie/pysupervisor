#!/usr/local/bin/python3

import argparse
import psutil

parser = argparse.ArgumentParser(description='Python implementation of a daemon supervisor')
parser.add_argument('--name', metavar='NAME', dest='name', type=str, required=True,
                    help='A keyword name of the process')
parser.add_argument('--interval', metavar='SEC', dest='interval', type=int, default=5,
                    help='Check interval in seconds. Default value is 5.')
parser.add_argument('--max-retry', metavar='INT', dest='retry', type=int, default=5,
                    help='Number of retry attempts before stopping. Default value is 5.')
parser.add_argument('--restart-delay', metavar='SEC', dest='delay', type=int, default=2,
                    help='Delay time before restarting process in seconds. Default value is 2.')
parser.add_argument('--logfile', metavar='PATH', dest='delay', type=int, default='/var/log/pysupervisor.log',
                    help='Path to logfile. Default value is \'/var/log/pysupervisor.log\'')

if __name__ == '__main__':
    args = parser.parse_args()

    pid_list = list()
    proc_list = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if args.name in p.info['name']]

    if proc_list is not None:
        print('List of matching processes: ')
        for proc in proc_list:
            print(proc['pid'], '\t', proc['name'])
            pid_list.append(proc['pid'])

    pid_capture = input('Which process do you want to monitor: ')

    try:
        pid_input = int(pid_capture)

        if pid_input not in pid_list:
            print('Process ID not in match list. Aborting...')
            exit(1)

        elif not psutil.pid_exists(pid_input):
            print('Process already terminated. Aborting...')
            exit(1)

        else:
            #TODO: Monitor
            proc = psutil.Process(pid_input)
            print('Monitoring pid: ', pid_input, ' process name: ', proc.name())

    except ValueError:
            print('Invalid type for Process ID. Must be integer. Aborting...')
            exit(1)