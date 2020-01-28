import keralabot
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *

@bot.message_handler(commands=['start'])
def start(message, args[]):
    if len(args) >= 1:
            if args[0].lower() == "help":
            bot.reply_to(message, "Help")
    if message.chat.type == "private":
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "<b>Hi I am an Admin bot written using KeralaPyApi.</b>", parse_mode="HTML")
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "Hello, How are you")
    
