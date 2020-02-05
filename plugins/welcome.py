import keralabot
from keralabot import types

import logging

from config import *

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    if message.new_chat_member != None:
        bot.reply_to(message, "Hello {} welcome.".format(message.from_user.first_name))
