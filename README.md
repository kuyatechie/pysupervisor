# pysupervisor

## Description

A Python implementation of daemon supervisor

This daemon supervisor is written in Python and is composed of a script file pysupervisor.py. 
Sample shell scripts are also provided for testing purposes.

## System Requirements
This application is developed using Darwin based environment and tested in an Ubuntu based environment (Lubuntu 4.18.0-13-generic #14-Ubuntu) installed in VirtualBox. Though these are just minimum requirements, operational requirements will mostly depends on the scripts being run and the resource usage of the watched processes.

Operating System: Debian based Linux (Fedora based can be used but still untested)

Recommended Operating System: Lubuntu 4.18.0-13-generic #14-Ubuntu (See https://lubuntu.net/downloads/)

Processor: minimum 2 cores

Memory: minimum 2048 MB

Storage: At least 10GB

## Installation
Python 3 and dependencies (tested using Python 3.7.2)

Please follow official documentation on how to install this. https://www.python.org/downloads/


````
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
````

## Usage
The pysupervisor, upon running, basically generates a list of processes containing the name provided in the program args.

Then the user will choose which running process to supervise. 

Supposing you have some process you want to supervise from a given matching list, the pid of that process will be supplied to the app.

Then the application will attach itself to the process and monitor it in daemon.

If the process being watched is terminated, became zombie or ended forcefully, the app will respawn and monitor a new one.

If the process cannot be respawned, it will stop after several number of attempts (user input).


````
arvin$ python3 pysupervisor.py --help
usage: pysupervisor.py [-h] -n NAME [-i SEC] [-r INT] [-d SEC] [-l PATH]

Python implementation of a daemon supervisor

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  A keyword name of the process
  -i SEC, --check-interval SEC
                        Check interval in seconds. Default value is 5.
  -r INT, --max-retry INT
                        Number of retry attempts before stopping. Default
                        value is 5.
  -d SEC, --restart-delay SEC
                        Delay time before restarting process in seconds.
                        Default value is 5.
  -l PATH, --logfile PATH
                        Path to logfile. Default value is
                        '/var/log/pysupervisor.log'
````

It is important to check the permissions of filepath where the app log is saved. 
Otherwise, no log can be recorded and the app will crash.

## Sample Runs
Sample runs are done using test sh scripts provided.

### Using non terminating process
````
$python3 pysupervisor.py --name bash -i 15 -d 10 -l ./pysupervisor.log
List of matching processes: 
351,	bash
368,	bash
1773,	bash
1791,	bash
Which process do you want to monitor (pid): 1791
2019-01-29 23:49:41,246 root         INFO     Monitoring pid: 1791 process name: bash cmd: ['/bin/bash', './test_process_looping.sh']
2019-01-29 23:49:41,246 root         INFO     Process bash with id 1791 is running
2019-01-29 23:49:56,249 root         INFO     Process bash with id 1791 is running
2019-01-29 23:50:11,251 root         INFO     Process bash with id 1791 is running
2019-01-29 23:50:26,252 root         INFO     Process bash with id 1791 is running
2019-01-29 23:50:41,256 root         INFO     Process bash with id 1791 is running
````

### Using a terminating process
````
$ python3 pysupervisor.py --name bash -i 15 -d 10 -l ./pysupervisor.log
List of matching processes: 
351,	bash
368,	bash
1773,	bash
1918,	bash
Which process do you want to monitor (pid): 1918
2019-01-29 23:52:26,262 root         INFO     Monitoring pid: 1918 process name: bash cmd: ['/bin/bash', './test_process_terminating.sh']
2019-01-29 23:52:26,262 root         INFO     Process bash with id 1918 is running
2019-01-29 23:52:41,268 root         WARNING  Process bash with id 1918 terminated and is not existing anymore. Respawning process.
2019-01-29 23:52:41,271 root         INFO     New process bash with pid 1923 respawned.
2019-01-29 23:52:41,271 root         INFO     Retry count down to 4
Process 1923 running. Terminates in 3 iteration.
Process 1923 running. Terminates in 2 iteration.
Process 1923 running. Terminates in 1 iteration.
2019-01-29 23:52:51,273 root         INFO     Process bash with id 1923 is zombie. Respawning process.
2019-01-29 23:52:51,276 root         INFO     New process bash with pid 1927 respawned.
2019-01-29 23:52:51,277 root         INFO     Retry count down to 3
Process 1927 running. Terminates in 3 iteration.
Process 1927 running. Terminates in 2 iteration.
Process 1927 running. Terminates in 1 iteration.
2019-01-29 23:53:01,282 root         INFO     Process bash with id 1927 is zombie. Respawning process.
2019-01-29 23:53:01,285 root         INFO     New process bash with pid 1931 respawned.
2019-01-29 23:53:01,285 root         INFO     Retry count down to 2
Process 1931 running. Terminates in 3 iteration.
Process 1931 running. Terminates in 2 iteration.
Process 1931 running. Terminates in 1 iteration.
2019-01-29 23:53:11,291 root         INFO     Process bash with id 1931 is zombie. Respawning process.
2019-01-29 23:53:11,294 root         INFO     New process bash with pid 1935 respawned.
2019-01-29 23:53:11,295 root         INFO     Retry count down to 1
Process 1935 running. Terminates in 3 iteration.
Process 1935 running. Terminates in 2 iteration.
Process 1935 running. Terminates in 1 iteration.
2019-01-29 23:53:21,298 root         INFO     Process bash with id 1935 is zombie. Respawning process.
2019-01-29 23:53:21,301 root         INFO     New process bash with pid 1939 respawned.
2019-01-29 23:53:21,302 root         INFO     Retry count down to 0
Process 1939 running. Terminates in 3 iteration.
Process 1939 running. Terminates in 2 iteration.
Process 1939 running. Terminates in 1 iteration.
2019-01-29 23:53:31,304 root         WARNING  Max retries reached and process still not running. Aborting...
````

