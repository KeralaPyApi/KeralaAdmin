import keralabot
from keralabot import types

import logging

from config import *
from database import *
import SQL.welcome_sql as sql
from plugins.funcs import get_welcome_type
from keralabot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keralabot.button.base import escape_markdown
from keralabot.button.parse_button import build_keyboard

#VALID_WELCOME_FORMATTERS = ['first']


@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    first_name = message.new_chat_member.first_name
    full_name = "{} {}".format(message.new_chat_member.first_name, message.new_chat_member.last_name)
    mention = "[{}](tg://user?id={})".format(message.new_chat_member.first_name, message.from_user.id)
    members = bot.get_chat_members_count(chat_id)
    cust_welcome = sql.get_welc_pref(chat_id)
    cust_welcome = cust_welcome.replace('{name}', escape_markdown(first_name))
    cust_welcome = cust_welcome.replace('{fullname}', escape_markdown(full_name))
    cust_welcome = cust_welcome.replace('{mention}', (mention))
    cust_welcome = cust_welcome.replace('{title}', escape_markdown(chat_title))
    buttons = sql.get_welc_buttons(chat_id)
    keyb = build_keyboard(buttons)
    keyboard = InlineKeyboardMarkup(keyb)
    if cust_welcome != True:
        welcome = cust_welcome
    else:
        welcome = sql.DEFAULT_WELCOME.format(first=message.from_user.first_name)
    bot.reply_to(message, welcome, parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=['setwelcome'])
def setwelcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    members = bot.get_chat_member(chat_id, user_id)
    if members.status == "administrator" or members.status == "creator":
        text, data_type, content, buttons = get_welcome_type(message)
        sql.set_custom_welcome(chat_id, content or text, data_type, buttons)
        bot.reply_to(message, "Successfully set welcome message for *{}*".format(message.chat.title), parse_mode="Markdown")

@bot.message_handler(commands=['welcome']) #To see welcome format
def seewelcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    members = bot.get_chat_member(chat_id, user_id)
    if members.status == "administrator" or members.status == "creator":
        cust_welcome = sql.get_welc_pref(chat_id)
        bot.reply_to(message, cust_welcome, parse_mode='Markdown')
    else:
        bot.delete_message(message.chat.id, message.message_id)
