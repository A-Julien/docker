#!/usr/bin/env python

import RPi.GPIO as GPIO
import json
import sys
import subprocess

import logging, sys
from time import sleep
import paho.mqtt.client as mqtt
import json
import time
from logging.handlers import RotatingFileHandler

DEBUG = True

root = '/opt/gpioMqtt'
# ******************************************#
#               LOGGER                      #
# ******************************************#

# create a file handler
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if DEBUG:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

try :
    handler = RotatingFileHandler(root + '/mqttToPwm.log', mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=2, encoding=None, delay=0)
except IOError as e:
    print("[ERR] can't find folder " + root)
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)

handler.setFormatter(log_formatter)
handler.setLevel(logging.INFO)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# add the handlers to the logger
#logger.addHandler(handler)


# ******************************************#
#               Config                      #
# ******************************************#

try:
    config = json.load(open(root + '/config.json'))
except IOError:
    print "can not find config.json at " + root + "/config.json"
    sys.exit()
# ******************************************#
#               Mqtt Topic                  #
# ******************************************#
MQTT_TOPIC_SUFFIX = config["mqtt"]["MQTT_TOPIC_SUFFIX"]
MQTT_PUB_TOPIC = config["mqtt"]["MQTT_PUB_TOPIC"]

# ******************************************#
#               Mqtt                        #
# ******************************************#

MQTT_BROKER_ADR = config["mqtt"]["MQTT_BROKER_ADR"]
MQTT_BROKER_PORT = int(config["mqtt"]["MQTT_BROKER_PORT"])
MQTT_NAME = config["mqtt"]["MQTT_NAME"]

# ******************************************#
#                GPIO                       #
# ******************************************#

Pin = int(config["GPIO"]["PIN"])


def setupGPIO():
   if config["GPIO"]["mode"] == "BCM":
        GPIO.setmode(GPIO.BCM)
    else:
        GPIO.setmode(GPIO.BOARD)
        
    GPIO.setup(Pin, GPIO.IN, GPIO.IN)
    GPIO.add_event_detect(Pin, GPIO.RISING, callback=cb_rising, bouncetime=200) # Wait for the input to go low, run the function when it does
    GPIO.add_event_detect(Pin, GPIO.FALLING, callback=cb_falling, bouncetime=200) # Wait for the input to go low, run the function when it does

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

def publish_data(data):
    global client
    client.publish("/" + MQTT_TOPIC_SUFFIX + "/" + MQTT_PUB_TOPIC, data)
    logger.info("Data publish on " + MQTT_PUB_TOPIC)

# Create a function to run when the input is high
def cb_rising(channel):
    print('cube charging')
    publish_data("1")

def cb_falling(chanel):
    publish_data("0")

client = mqtt.Client()

def main(): 

    logger.info("Start GPIO")

    setupGPIO()
    
    """Mqtt client"""
    logger.info("Start mqtt client")

    client.on_connect = on_connect
    client.connect(MQTT_BROKER_ADR, MQTT_BROKER_PORT, 60)
    
    client.loop_start()
    logger.info("[CON] Connection to " + MQTT_BROKER_ADR + " broker on port " + str(MQTT_BROKER_PORT))


    while True :
        time.sleep(1)

if __name__ == '__main__':
    main()