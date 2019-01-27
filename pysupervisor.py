#!/usr/local/bin/python3

import argparse

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
