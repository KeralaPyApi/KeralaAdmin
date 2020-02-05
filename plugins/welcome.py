import keralabot
from keralabot import types

import logging

from config import *

@bot.message_handler(func=lambda message: True)
def welcome(message):
    if message.new_chat_member != None:
        bot.reply_to(message, "Hello {first} welcome.".format(message.new_chat_member.first_name))
