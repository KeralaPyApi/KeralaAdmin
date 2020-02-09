import keralabot
import logging

logger = keralabot.logger
keralabot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

from config import *
from googletrans import Translator

@bot.message_handler(commands=['tr'])
def translate(message):
    to_translate_text = message.reply_to_message.text
    lang = message.text[4:]
    if lang == None:
        lang = "en"
    translator = Translator()
    try:
        translated = translator.translate(to_translate_text, dest=lang)
        src_lang = translated.src
        translated_text = translated.text
        bot.reply_to(message, "Translated from {} to {}.\n\n{}.".format(src_lang, lang, translated_text))
    except:
        bot.reply_to(message, "Error in Translation")
