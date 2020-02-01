import keralabot
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *

@bot.message_handler(commands=['id'])
def tg_id(message):
    if message.chat.type == "private":
        bot.reply_to(message, "*Information of user*\n\n*Name* : `{}`\n*ID *: `{}`".format(message.from_user.first_name, message.from_user.id), parse_mode="Markdown")
    if message.chat.type != "private" and message.reply_to_message == None:
        bot.reply_to(message, "*Information of the user*\n\n*Name* : `{}`\n*ID* : `{}`\n\n*Information of the chat*\n\n*Name of chat* : `{}`\n*ID of chat* : `{}`\n*Type of Chat* : `{}`".format(message.from_user.first_name, message.from_user.id, message.chat.title, message.chat.id, message.chat.type), parse_mode="Markdown")
    if message.chat.type != "private" and message.reply_to_message != None:
        bot.reply_to(message, "*Information of the user*\n\n*Name* : `{}`\n*ID* : `{}`\n\n*Information of the chat*\n\n*Name of chat* : `{}`\n*ID of chat* : `{}`\n*Type of Chat* : `{}`".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id, message.chat.title, message.chat.id, message.chat.type), parse_mode="Markdown")

