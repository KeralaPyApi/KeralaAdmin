import keralabot
from keralabot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *

@bot.message_handler(commands=['id'])
def tg_id(message):
    if message.chat.type == "private":
        bot.reply_to(message, "*Information of user*\n\n*Name* : `{}`\n*ID *: `{}`".format(message.from_user.first_name, message.from_user.id) parse_mode="Markdown") 
