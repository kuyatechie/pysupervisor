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

It is important to check the permissions of filename where the app log is saved. 
Otherwise, no log can be recorded and the app will crash.

## Example
TODO