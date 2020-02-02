import keralabot

import logging

from config import *

@bot.message_handler(commands=['ban'])
def ban(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    members = bot.get_chat_member(chat_id, user_id)
    if message.chat.type == "private":
        bot.reply_to(message, "This command is meant to be used in Groups")
    if message.reply_to_message == None and members.status == "administrator" or members.status == "creator":
        ban_user = message.text[5:]
        if ban_user == None:
            bot.reply_to(message, "Reply to a message or send me the ID of the user")
        else:
            bot.kick_chat_member(message.chat.id, ban_user)
    else:
        bot.reply_to(message, "Who are you Non - Admin to command me")
    if message.reply_to_message != None and members.status == "administrator" or members.status == "creator":
        bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    else:
        bot.reply_to(message, "Who are you Non - Admin to command me")

