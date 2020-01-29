from datetime import datetime

from config import *

def ping(message):
    if message.text == "/ping" or message.text == "!ping":
        first = datetime.now()
        ping = bot.send_message(message.chat.id, **Ping!**, parse_mode='Markdown')
        second = datetime.now()
        bot.edit_message_text(message.chat.id, ping.chat.id, "**Pong!**\n`{}`".format((second - first).microseconds / 1000), parse_mode='Markdown')
        return true
