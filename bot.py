# coding=UTF-8

from config import *

import import_directory
import_directory.do('plugins', globals())

# Pool for messages
bot.polling(none_stop=True)
