import keralabot
from keralabot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *
from typing import Optional, List

def markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Help", callback_data="help"),
                               InlineKeyboardButton("Add me to group", url="t.me/{}?startgroup=new".format(botname)))
    return markup

def help_markup():
    help_markup = InlineKeyboardMarkup()
    help_markup.row_width = 2
    help_markup.add(InlineKeyboardButton("Admin", callback_data="admin"), InlineKeyboardButton("Greetings", callback_data="welcome"))
    help_markup.add(InlineKeyboardButton("Google Translate", callback_data="translate"), InlineKeyboardButton("Misc", callback_data="misc"))
    return help_markup

def help_back():
    help_back = InlineKeyboardMarkup()
    help_back.row_width = 1
    help_back.add(InlineKeyboardButton("🔙 Back", callback_data="help_back"))
    return help_back

@bot.message_handler(commands=['start'])
def start(message, *args):
    args = List[str]
    if message.chat.type == "private":
        if args >= 1:
            if args[0].lower() == "help":
                callback_query(message)
        else: 
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(message, "<b>Hi I am an Admin bot written using KeralaPyApi.</b>", parse_mode="HTML", reply_markup=markup())
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "Hello, How are you")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "help":
        bot.answer_callback_query(call.id, "On beta mode now")
        bot.edit_message_text("There are many things that I can do. But now I am in Beta 🚼 mode.\n\nThese are some of my modules.", call.message.chat.id, call.message.message_id, reply_markup=help_markup())
    if call.data == "admin":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id, reply_markup=help_back())
    if call.data == "welcome":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id, reply_markup=help_back())
    if call.data == "translate":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id, reply_markup=help_back())
    if call.data == "misc":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id, reply_markup=help_back())
    if call.data == "help_back":
        bot.edit_message_text("There are many things that I can do. But now I am in Beta 🚼 mode.\n\nThese are some of my modules.", call.message.chat.id, call.message.message_id, reply_markup=help_markup())


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, " ~Strike~\n*bold*", parse_mode="MarkdownV2")
