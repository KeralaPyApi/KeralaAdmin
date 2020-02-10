import keralabot
from keralabot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *

def markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Help", callback_data="help"),
                               InlineKeyboardButton("Add me to group", url="t.me/{}?startgroup=new".format(botname)))
    return markup

def help_markup():
    help_mark = InlineKeyboardMarkup()
    help_mark.row_width = 2
    help_mark.add(InlineKeyboardButton("Admin", callback_data="admin"), InlineKeyboardButton("Greetings", callback_data="welcome"))
    help_mark.add(InlineKeyboardButton("Google Translate", callback_data="translate"), InlineKeyboardButton("Misc", callback_data="misc"))
    return help_mark

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "private":
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "<b>Hi I am an Admin bot written using KeralaPyApi.</b>", parse_mode="HTML", reply_markup=markup())
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "Hello, How are you")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "help":
        bot.answer_callback_query(call.id, "On beta mode now")
        bot.edit_message_text("There are many things that I can do. But now I am in Beta 🚼 mode.\n\nThese are some of my modules.", call.message.chat.id, call.message.message_id, reply_markup=help_mark())
    if call.data == "admin":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id)
    if call.data == "welcome":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id)
    if call.data == "translate":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id)
    if call.data == "misc":
        bot.edit_message_text("On beta mode now", call.message.chat.id, call.message.message_id)

