import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep
import paho.mqtt.client as mqtt
import requests
import json


config = json.load(open('/opt/telegram/config.json'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

chat_id = config["telegrame"]["chat_id"]
token = config["telegrame"]["token"]

# ******************************************#
#               Mqtt Topic                  #
# ******************************************#
MQTT_TOPIC_SUFFIX = config["mqtt"]["MQTT_TOPIC_SUFFIX"]
MQTT_TOPIC_TO_SEND = config["mqtt"]["MQTT_TOPIC_TO_SEND"]
MQTT_PUB_TOPIC = config["mqtt"]["MQTT_PUB_TOPIC"]

# ******************************************#
#               Mqtt                        #
# ******************************************#

MQTT_BROKER_ADR = config["mqtt"]["MQTT_BROKER_ADR"]
MQTT_BROKER_PORT = int(config["mqtt"]["MQTT_BROKER_PORT"])
MQTT_NAME = config["mqtt"]["MQTT_NAME"]

client = mqtt.Client()


#client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC_SUFFIX + '/' + MQTT_TOPIC_TO_SEND)
    logger.info("Connected with result code " + str(rc))
    logger.info(MQTT_TOPIC_SUFFIX + '/' + MQTT_TOPIC_TO_SEND)

def publish_data(data):
    global client
    client.publish(MQTT_TOPIC_SUFFIX + "/" + MQTT_PUB_TOPIC, data)
    logger.info('msg sent')

def on_message(client, userdata, msg):
    global chat_id
    global token
    global start_bot
    logger.info("message received from " + msg.topic + ", value : " + str(msg.payload))
    topic = str(msg.topic).split('/')
    value = str(msg.payload)
    if topic[1] == MQTT_TOPIC_TO_SEND:
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, "sendMessage"),
            data={'chat_id': chat_id, 'text': value}
        ).json()

def start(bot, update):
    global chat_id
    global start_bot
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    chat_id = update.message.chat_id
    logger.info(update.message.text)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def toMqtt(bot, update):
    global start_bot
    """Send a message when the command /start is issued."""
    logger.info(update.message.text)
    publish_data(update.message.text.replace('/tomqtt ', ''))
    update.message.reply_text('msg received')

def echo(bot, update):
    """Echo the user message."""
    logger.info(update.message.text)
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main(): 
    logger.info("Start mqtt client")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_ADR, MQTT_BROKER_PORT, 60)
    
    client.loop_start()

    logger.info("Start telegram bot")
    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tomqtt", toMqtt))

    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.bot.sendMessage(chat_id, "Booting [OK]")
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()