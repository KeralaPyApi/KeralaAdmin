#####################################
import os

token = os.environ.get("TOKEN", "")

admin_id = int(os.environ.get("ADMIN_ID", ""))
admin_name = os.environ.get("ADMIN_USERNAME", "")
botname = os.environ.get("BOT_NAME", "") # USERNAME of the bot without '@'

#####################################

import keralabot

from keralabot import types

bot = keralabot.bot(token)

