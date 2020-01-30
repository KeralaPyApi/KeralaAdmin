import keralabot
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *

@bot.message_handler(commands=['id'])
def getids(message):
    if message.chat.type == "private":
        bot.reply_to(message, "*Information of the user*\n\n*Name :* `{}`\n*Username :* `{}`\n*User ID :* `{}`".format(message.from.first_name, message.from.username, message.from.id), parse_mode='Markdown')
        return
