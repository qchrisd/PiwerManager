# PiwerManager
The objective of this module is to monitor the power source and battery life of a Raspberry Pi.

## Hardware
This module relies on using a [PowerBoost 1000C](https://www.adafruit.com/product/2465) to supply power to your Raspberry Pi. The model of Raspberry Pi doesn't matter as long as it has a GPIO available.

## Software
This module is written in [Python 3](https://www.python.org/) and relies on the following libraries:
- [RPi GPIO library](https://pypi.org/project/RPi.GPIO/) to control the GPIO pins.
- [Python Daemon](https://pypi.org/project/python-daemon/) to daemonize the monitor

## Installation
The PiwerMonitor needs the appropriate GPIO pins defined in the config file. The following command should be added to cron to run on boot:

```@reboot python3 ~/PiwerMonitor/monitor.py```
