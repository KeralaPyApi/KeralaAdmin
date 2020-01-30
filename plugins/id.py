from config import *

@bot.message_handler(commands=['id'])
def get_id(message):
    if message.chat.type == "private":
        if 'username' in message.from:
            username = message.from.username
        else:
            username = ''
        bot.reply_to(message.chat.id, '''*Information of the user*

*Name :* `{}`
*Username :* `{}`
*User ID :* `{}`'''.format(message.from.first_name, username, message.from.id), parse_mode='Markdown')
        return
