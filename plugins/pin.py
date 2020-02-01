import keralabot

import logging

from config import *
from database import *

def is_admin(chat_id, user_id, reply_id=None):
    if int(chat_id) < 0:  # Groups and supergoups IDs.
        dic = {}
        cursor.execute('SELECT cached_admins FROM chats WHERE chat_id = ?', (int(chat_id),))
        adms = cursor.fetchone()[0]
        if adms:
            cached_admins = json.loads(adms)
        else:
            cached_admins = {'expires': 0}

        if cached_admins['expires'] > time.time():
            adm_id = cached_admins['admins_list']
        else:
            adms = bot.get_chat_administrators(chat_id)
            adm_id = []
            for ids in adms:
                adm_id.append(ids['user']['id'])
            cursor.execute('UPDATE chats SET cached_admins = ? WHERE chat_id = ?', (json.dumps(dict(admins_list=adm_id, expires=int(time.time()) + 1200)), chat_id))
            conn.commit()

        if user_id in adm_id:
            dic['user'] = True
        else:
            dic['user'] = False

        if reply_id in adm_id:
            dic['reply'] = True
        else:
            dic['reply'] = False

        if bot_id in adm_id:
            dic['bot'] = True
        else:
            dic['bot'] = False

    else:  # User IDs.
        dic = dict(user=False, reply=False, bot=False)

    return dic


@bot.message_handler(commands=['pin'])
def pin(message):
    reply_id = None
    adm = is_admin(message.chat.id, message.from_user.id, reply_id)
    if message.chat.type == "private":
        bot.reply_to(message, "This command is meant to be used in Groups")
    if message.reply_to_message == None:
        bot.reply_to(message, "Reply to a message to be pinned")
    if message.reply_to_message.id == adm:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
