#!/usr/local/bin/python3

import argparse
import psutil
import time
import subprocess
import logging

logger = logging.getLogger()

parser = argparse.ArgumentParser(description='Python implementation of a daemon supervisor')

parser.add_argument('-n', '--name', metavar='NAME', dest='name', type=str, required=True,
                    help='A keyword name of the process')

parser.add_argument('-i', '--check-interval', metavar='SEC', dest='interval', type=int, default=5,
                    help='Check interval in seconds. Default value is 5.')

parser.add_argument('-r', '--max-retry', metavar='INT', dest='retry', type=int, default=5,
                    help='Number of retry attempts before stopping. Default value is 5.')

parser.add_argument('-d', '--restart-delay', metavar='SEC', dest='delay', type=int, default=5,
                    help='Delay time before restarting process in seconds. Default value is 5.')

parser.add_argument('-l', '--logfile', metavar='PATH', dest='logfile', type=str, default='/var/log/pysupervisor.log',
                    help='Path to logfile. Default value is \'/var/log/pysupervisor.log\'')


def monitor_process(proc, interval, retry, delay, cmd):
    default_retries = retry
    while retry > 0:
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
            status = str(proc.status()).replace('psutil.', '')

            if proc.is_running() and proc.status() is not psutil.STATUS_ZOMBIE:
                logger.info('Process {} with id {} is {}'.format(pinfo['name'], pinfo['pid'], status))
                time.sleep(interval)
                if retry is not default_retries:
                    retry = default_retries
                    logger.info('Retry count restored to {}'.format(default_retries))

            elif proc.status() in [psutil.STATUS_IDLE,
                                   psutil.STATUS_PARKED,
                                   psutil.STATUS_SLEEPING,
                                   psutil.STATUS_WAKING]:
                logger.info('Process {}  with id {} is {}'.format(pinfo['name'], pinfo['pid'], status))
                time.sleep(interval)

            else:
                logger.info('Process {} with id {} is {}. Respawning process.'.format(pinfo['name'], pinfo['pid'], status))
                new_proc = subprocess.Popen(cmd)
                proc = psutil.Process(new_proc.pid)
                logger.info('New process {} with pid {} respawned.'.format(proc.name(), proc.pid))
                retry = retry - 1
                logger.info('Retry count down to {}'.format(str(retry)))
                time.sleep(delay)

        except psutil.NoSuchProcess:
            logger.warning('Process {} with id {} terminated and is not existing anymore. Respawning process.'
                           .format(pinfo['name'], pinfo['pid'], status))
            new_proc = subprocess.Popen(cmd)
            proc = psutil.Process(new_proc.pid)
            logger.info('New process {} with pid {} respawned.'.format(proc.name(), proc.pid))
            retry = retry - 1
            logger.info('Retry count down to {}'.format(str(retry)))
            time.sleep(delay)

    logger.warning('Max retries reached and process still not running. Aborting...')
    exit(60)


if __name__ == '__main__':
    # Initiate argument parser
    args = parser.parse_args()

    # Initiate logging module
    streamhandler = logging.StreamHandler()
    filehandler = logging.FileHandler(filename=args.logfile)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    streamhandler.setFormatter(formatter)

    logger.addHandler(streamhandler)
    logger.addHandler(filehandler)
    logger.setLevel(logging.INFO)

    # List all process containing name
    pid_list = list()
    proc_list = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if args.name in p.info['name']]

    if len(proc_list) is not 0:
        print('List of matching processes: ')
        for proc in proc_list:
            print("{},\t{}".format(proc['pid'],  proc['name']))
            pid_list.append(proc['pid'])
    else:
        logger.warning('Process name does not match any running process. Aborting...')
        exit(20)

    # Let user choose which process needs to be monitored
    pid_capture = input('Which process do you want to monitor (pid): ')

    # Main flow for monitoring process
    try:
        pid_input = int(pid_capture)

        if pid_input not in pid_list:
            logger.warning('Process ID not in match list. Aborting...')
            exit(30)

        elif not psutil.pid_exists(pid_input):
            logger.warning('Process already terminated. Aborting...')
            exit(40)

        else:
            proc = psutil.Process(pid_input)
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
            logger.info('Monitoring pid: {} process name: {} cmd: {}'.format(pinfo['pid'], pinfo['name'], pinfo['cmdline']))
            monitor_process(proc, args.interval, args.retry, args.delay, proc.cmdline())

    except ValueError:
            logger.warning('Invalid type for Process ID. Must be integer. Aborting...')
            exit(50)

    except Exception as err:
            logger.critical('Unexpected error: {}. Aborting...'.format(err))
            exit(60)
