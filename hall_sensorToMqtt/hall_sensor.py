import logging
from time import sleep
import paho.mqtt.client as mqtt
import requests
import json
from time import gmtime, strftime
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
    print("["+bcolors.FAIL +"ERR"+bcolors.ENDC+"] can't find folder " + root)
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

def publish_data(data):
    global client
    client.publish(MQTT_TOPIC_SUFFIX + "/" + MQTT_PUB_TOPIC, data)
    logger.info()

def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if GPIO.input(channel):
    # No magnet
    publish_data(0)
    logger.info("No magnet detected")
  else:
    # Magnet
    publish_data(1)
    logger.info("Magnet detected")


def setupGPIO():
    """ GPIO Setup """
    if config["mqtt"]["GPIO"] == "BCM":
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

    client.connect(MQTT_BROKER_ADR, MQTT_BROKER_PORT, 60)
    
    client.loop_start()
   
   

if __name__ == '__main__':
    main()