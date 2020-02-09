import keralabot
from keralabot import types

import logging

from config import *
from database import *
import SQL.welcome_sql as sql

VALID_WELCOME_FORMATTERS = ['first']

def markdown(text):
    text = text.replace(']', '\]')
    text = text.replace('[', '\[')
    text = text.replace('_', '\_')
    text = text.replace('*', '\*')
    text = text.replace('`', '\`')

    return text

def escape_invalid_curly_brackets(text, valids):
    new_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "{":
            if idx + 1 < len(text) and text[idx + 1] == "{":
                idx += 2
                new_text += "{{{{"
                continue
            else:
                success = False
                for v in valids:
                    if text[idx:].startswith('{' + v + '}'):
                        success = True
                        break
                if success:
                    new_text += text[idx: idx + len(v) + 2]
                    idx += len(v) + 2
                    continue
                else:
                    new_text += "{{"

        elif text[idx] == "}":
            if idx + 1 < len(text) and text[idx + 1] == "}":
                idx += 2
                new_text += "}}}}"
                continue
            else:
                new_text += "}}"

        else:
            new_text += text[idx]
        idx += 1

    return new_text

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
    cust_welcome = sql.get_welc_pref(chat_id)
    #valid_format = escape_invalid_curly_brackets(cust_welcome, VALID_WELCOME_FORMATTERS)
    #res = valid_format.format(first=markdown(first_name))                      
    if cust_welcome == True:
        welcome = cust_welcome
    else:
        welcome = sql.DEFAULT_WELCOME.format(first=message.from_user.first_name)
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['setwelcome'])
def setwelcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    members = bot.get_chat_member(chat_id, user_id)
    if members.status == "administrator" or members.status == "creator":
        custom_welcome = message.text[12:]
        sql.set_custom_welcome(chat_id, custom_welcome, sql.Types.TEXT)
        bot.reply_to(message, "Successfully set welcome message for *{}*".format(message.chat.title), parse_mode="Markdown")
