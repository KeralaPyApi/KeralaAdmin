import keralabot
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "private":
        bot.reply_to(message, "<b>Hi I am an Admin bot written using KeralaPyApi.</b>", parse_mode="HTML")
    else:
        bot.reply_to(message,"Hello, How are you")
    
