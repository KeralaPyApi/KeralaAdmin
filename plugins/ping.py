from datetime import datetime

from config import *

@bot.message_handler(commands=['ping'])
def ping(message):
    if message.text == "/ping" or message.text == "!ping":
        first = datetime.now()
        ping = bot.send_message(message.chat.id, "**Ping!**", parse_mode='Markdown')
        second = datetime.now()
        bot.edit_message_text("**Pong!**\n`{}`".format((second - first).microseconds / 1000), message.chat.id, ping.message_id, parse_mode='Markdown')
        return true
