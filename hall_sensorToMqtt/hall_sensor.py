import logging, sys
from time import sleep
import paho.mqtt.client as mqtt
import json
import time
from logging.handlers import RotatingFileHandler
import RPi.GPIO as GPIO

DEBUG = True

root = '/opt/hall_sensor'
# ******************************************#
#               LOGGER                      #
# ******************************************#

# create a file handler
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if DEBUG:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

try :
    handler = RotatingFileHandler(root + '/hall_sensor.log', mode='a', maxBytes=5 * 1024 * 1024,
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
    logger.error("can not find conf.json at " + root + "/conf.json")
    sys.exit()


# ******************************************#
#                GPIO                       #
# ******************************************#

Pin = int(config["GPIO"]["PIN"])

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

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

def publish_data(data):
    global client
    client.publish("/" + MQTT_TOPIC_SUFFIX + "/" + MQTT_PUB_TOPIC, data)
    logger.info("Data publish on " + MQTT_PUB_TOPIC)

def sensorCallback(channel):
  if GPIO.input(channel):
    # No magnet
    publish_data("0")
    logger.info("No magnet detected")
  else:
    # Magnet
    publish_data("1")
    logger.info("Magnet detected")


def setupGPIO():
    """ GPIO Setup """
    if config["GPIO"]["mode"] == "BCM":
        GPIO.setmode(GPIO.BCM)
    else:
        GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(Pin , GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Pin, GPIO.BOTH, callback=sensorCallback, bouncetime=200)


def main(): 

    logger.info("Start GPIO")

    setupGPIO()
    
    """Mqtt client"""
    logger.info("Start mqtt client")

    client.on_connect = on_connect
    client.connect(MQTT_BROKER_ADR, MQTT_BROKER_PORT, 60)
    
    client.loop_start()
    logger.info("[CON] Connection to " + MQTT_BROKER_ADR + " broker on port " + str(MQTT_BROKER_PORT))

    logger.info("Pushing data on /" + MQTT_TOPIC_SUFFIX + "/" + MQTT_PUB_TOPIC)


    while True :
        time.sleep(.1)   
   

if __name__ == '__main__':
    main()
