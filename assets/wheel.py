#!/usr/bin/python

# setup a supervisor job to start and restart this script
# https://stackoverflow.com/questions/8685695/how-do-i-run-long-term-infinite-python-processes
# mine is here:
'''
[program:wheel] 
command = python /home/hamcam/wheel.py 
directory = /home/hamcam
user = hamcam
autostart = true 
autorestart = true 
stdout_logfile = /var/log/supervisor/wheel.log 
stderr_logfile = /var/log/supervisor/wheel_err.log 
'''

import sys
import time
import logging

import datetime 
import RPi.GPIO as GPIO

INPUT_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def f(channel):
    logging.info('Lap: {}'.format(datetime.datetime.now().isoformat()))

GPIO.add_event_detect(INPUT_PIN, GPIO.RISING, callback=f, bouncetime=200)

def main():
    while 1:
        time.sleep(60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # py3k print('\nExiting by user request.\n', file=sys.stderr)
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)