import keralabot
from keralabot import types

import logging

from config import *

@bot.message_handler(filters.types.Message.new_chat_member)
def welcome(message):
    new_members = types.Message.new_chat_member
    for nm in new_members:
        bot.reply_to(message, "Hello {first} welcome.".format(nm.first_name))
