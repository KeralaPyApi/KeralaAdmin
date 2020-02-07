import keralabot
from keralabot import types

import logging

from config import *
from database import *

def markdown(text):
    text = text.replace(']', '\]')
    text = text.replace('[', '\[')
    text = text.replace('_', '\_')
    text = text.replace('*', '\*')
    text = text.replace('`', '\`')

    return text

def get_welcome(chat_id):
    cursor.execute('SELECT welcome, welcome_enabled FROM chats WHERE chat_id = (?)', (chat_id,))
    try:
        return cursor.fetchone()
    except IndexError:
        return None


def set_welcome(chat_id, welcome):
    cursor.execute('UPDATE chats SET welcome = ? WHERE chat_id = ?', (welcome, chat_id))
    conn.commit()


@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    first_name = message.new_chat_member.first_name
    welcome = get_welcome(chat_id)
    if welcome[1]:
        if welcome[0] is not None:
            welcome = welcome[0].replace('{id}', str(chat_id))
            welcome = welcome.replace('{title}', escape_markdown(chat_title))
            welcome = welcome.replace('{name}', escape_markdown(first_name))
        else:
            welcome = "Hello {} welcome.".format(message.from_user.first_name)
        bot.reply_to(message, welcome)
