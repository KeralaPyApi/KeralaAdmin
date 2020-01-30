import keralabot
from config import *

@bot.message_handler(commands=['id'])
def get_id(message):
    if message.chat.type == "private":
        bot.reply_to(message, "*Information of the user*\n\n*Name :* `{}`\n*Username :* `{}`\n*User ID :* `{}`".format(message.from.first_name, message.from.username, message.from.id), parse_mode='Markdown')
        return
