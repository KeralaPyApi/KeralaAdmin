import keralabot

import json
import time

import logging

from config import *
from database import *


@bot.message_handler(commands=['pin'])
def pin(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    members = bot.get_chat_member(chat_id, user_id)
    if message.chat.type == "private":
        bot.reply_to(message, "This command is meant to be used in Groups")
        return
    if message.reply_to_message == None:
        bot.reply_to(message, "Reply to a message to be pinned")
        return
    if members.status == "administrator" or members.status == "creator":
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.delete_message(message.chat.id, message.message_id)      #Added delete some command for misuse of that
        return
    if members.status != "administrator":
        bot.reply_to(message, "You need to be an Admin to pin the message")
        return
