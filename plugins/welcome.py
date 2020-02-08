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
    cursor.execute('SELECT welcome FROM chats WHERE chat_id = (?)', (chat_id,))
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
    if welcome is not None:
        welcome = welcome.replace('{id}', str(chat_id))
        welcome = welcome.replace('{title}', markdown(chat_title))
        welcome = welcome.replace('{name}', markdown(first_name))
    else:
        welcome = "Hello {} welcome.".format(message.from_user.first_name)
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['setwelcome'])
def setwelcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    members = bot.get_chat_member(chat_id, user_id)
    if members.status == "administrator" or members.status == "creator":
        welcome_message = message.text[12:]
        set_welcome(chat_id, welcome_message)
        bot.reply_to(chat_id, "Successfully set welcome message for *{}*".format(message.chat.title), parse_mode="Markdown")
