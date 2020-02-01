import keralabot

import logging

from config import *


@bot.message_handler(commands=['pin'])
def pin(message):
    if message.chat.type == "private":
        bot.reply_to(message, "This command is meant to be used in Groups")
    elif message.reply_to_message == None:
        bot.reply_to(message, "Reply to a message to be pinned")
    else:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
