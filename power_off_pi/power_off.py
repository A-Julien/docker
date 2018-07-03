#!/usr/bin/env python

import RPi.GPIO as GPIO
import json
import sys
import subprocess

root = "/opt/powerOff"

# ******************************************#
#               Config                      #
# ******************************************#

try:
    config = json.load(open(root + '/config.json'))
except IOError:
    print "can not find config.json at " + root + "/config.json"
    sys.exit()


# ******************************************#
#                GPIO                       #
# ******************************************#

PowerPin = int(config["GPIO"]["Pin"])
GPIO.setmode(GPIO.BCM)
GPIO.setup(PowerPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.wait_for_edge(PowerPin, GPIO.FALLING) 

subprocess.call(['shutdown', 'now', '-P'], shell=False) #Shutdown pi and power