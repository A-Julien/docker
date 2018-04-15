import logging, sys
from time import sleep
import paho.mqtt.client as mqtt
import json
import time
from logging.handlers import RotatingFileHandler
import RPi.GPIO as GPIO

DEBUG = True

root = '/opt/mqttToPwm'
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
    logger.error("can not find conf.json at " + root + "/conf.json")
    sys.exit()


# ******************************************#
#                GPIO                       #
# ******************************************#

PinR = int(config["GPIO"]["PinR"])
PinL = int(config["GPIO"]["PinL"])
pR = None
pL = None

# ******************************************#
#               Mqtt Topic                  #
# ******************************************#
MQTT_TOPIC_SUFFIX = config["mqtt"]["MQTT_TOPIC_SUFFIX"]
MQTT_TOPIC_RIGHT = config["mqtt"]["MQTT_TOPIC_RIGHT"]
MQTT_TOPIC_LEFT = config["mqtt"]["MQTT_TOPIC_LEFT"]

# ******************************************#
#               Mqtt                        #
# ******************************************#

MQTT_BROKER_ADR = config["mqtt"]["MQTT_BROKER_ADR"]
MQTT_BROKER_PORT = int(config["mqtt"]["MQTT_BROKER_PORT"])
MQTT_NAME = config["mqtt"]["MQTT_NAME"]

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC_SUFFIX + '/' + MQTT_TOPIC_RIGHT)
    client.subscribe(MQTT_TOPIC_SUFFIX + '/' + MQTT_TOPIC_LEFT)
    logger.info("Connected with result code " + str(rc))
    logger.info(MQTT_TOPIC_SUFFIX + '/' + MQTT_TOPIC_RIGHT)
    logger.info(MQTT_TOPIC_SUFFIX + '/' + MQTT_TOPIC_LEFT)

def on_message(client, userdata, msg):
    global pL
    global pR

    logger.info("message received from " + msg.topic + ", value : " + str(msg.payload))
    topic = str(msg.topic).split('/')
    value = int(msg.payload)
    try:
        if( value < 0 or value > 100):
            raise Exception
    except:
        logger.error( "[ERR] 0 > Duty cycle < 100")
    if topic[1] == MQTT_TOPIC_RIGHT:
        pR.ChangeDutyCycle(value)
    elif topic[1] == MQTT_TOPIC_LEFT:
        pL.ChangeDutyCycle(value)
    else:
        logger.error("[ERR] No topic available for " + topic[1])

def setupGPIO():
    global pL
    global pR

    """ GPIO Setup """
    if config["GPIO"]["Mode"] == "BCM":
        GPIO.setmode(GPIO.BCM)
    else:
        GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PinR, GPIO.OUT)
    GPIO.setup(PinL, GPIO.OUT)

    pR = GPIO.PWM(PinR, int(config["GPIO"]["Rfreq"]))
    pL = GPIO.PWM(PinL, int(config["GPIO"]["Lfreq"]))

    pR.start(0) 
    pL.start(0)             

def main(): 

    logger.info("Start GPIO")

    setupGPIO()
    
    """Mqtt client"""
    logger.info("Start mqtt client")

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_ADR, MQTT_BROKER_PORT, 60)
    
    client.loop_start()
    logger.info("[CON] Connection to " + MQTT_BROKER_ADR + " broker on port " + str(MQTT_BROKER_PORT))


    while True :
        time.sleep(.1)   
   

if __name__ == '__main__':
    main()
