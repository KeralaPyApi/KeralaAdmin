import re
import time
from typing import Dict, List

import emoji
import keralabot
from keralabot.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import IntEnum, unique


@unique
class Types(IntEnum):
    TEXT = 0
    BUTTON_TEXT = 1
    STICKER = 2
    DOCUMENT = 3
    PHOTO = 4
    AUDIO = 5
    VOICE = 6
    VIDEO = 7


MATCH_MD = re.compile(r'\*(.*?)\*|'
                      r'~(.*?)~|'
                      r'__*(.*?)__|'
                      r'_(.*?)_|'
                      r'`(.*?)`|'
                      r'(?<!\\)(\[.*?\])(\(.*?\))|'
                      r'(?P<esc>[*_`\[])')

# regex to find []() links -> hyperlinks/buttons
LINK_REGEX = re.compile(r'(?<!\\)\[.+?\]\((.*?)\)')
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

def escape_markdown(text):
    text = text.replace('[', '\[')
    text = text.replace('_', '\_')
    text = text.replace('*', '\*')
    text = text.replace('`', '\`')

    return text

try:
    import ujson as json
except ImportError:
    import json

from abc import ABCMeta


class TelegramObject(object):
    """Base class for most telegram objects."""

    __metaclass__ = ABCMeta
    _id_attrs = ()

    def __str__(self):
        return str(self.to_dict())

    def __getitem__(self, item):
        return self.__dict__[item]

    @classmethod
    def de_json(cls, data, bot):
        if not data:
            return None

        data = data.copy()

        return data

    def to_json(self):
        """
        Returns:
            :obj:`str`

        """

        return json.dumps(self.to_dict())

    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            if key in ('bot',
                       '_id_attrs',
                       '_credentials',
                       '_decrypted_credentials',
                       '_decrypted_data',
                       '_decrypted_secret'):
                continue

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        if data.get('from_user'):
            data['from'] = data.pop('from_user', None)
        return data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id_attrs == other._id_attrs
        return super(TelegramObject, self).__eq__(other)  # pylint: disable=no-member

    def __hash__(self):
        if self._id_attrs:
            return hash((self.__class__, self._id_attrs))  # pylint: disable=no-member
        return super(TelegramObject, self).__hash__()


def _selective_escape(to_parse: str) -> str:
    """
    Escape all invalid markdown

    :param to_parse: text to escape
    :return: valid markdown string
    """
    offset = 0  # offset to be used as adding a \ character causes the string to shift
    for match in MATCH_MD.finditer(to_parse):
        if match.group('esc'):
            ent_start = match.start()
            to_parse = to_parse[:ent_start + offset] + '\\' + to_parse[ent_start + offset:]
            offset += 1
    return to_parse

class User(TelegramObject):
    """This object represents a Telegram user or bot.

    Attributes:
        id (:obj:`int`): Unique identifier for this user or bot.
        is_bot (:obj:`bool`): True, if this user is a bot
        first_name (:obj:`str`): User's or bot's first name.
        last_name (:obj:`str`): Optional. User's or bot's last name.
        username (:obj:`str`): Optional. User's or bot's username.
        language_code (:obj:`str`): Optional. IETF language tag of the user's language.
        bot (:class:`telegram.Bot`): Optional. The Bot to use for instance methods.

    Args:
        id (:obj:`int`): Unique identifier for this user or bot.
        is_bot (:obj:`bool`): True, if this user is a bot
        first_name (:obj:`str`): User's or bot's first name.
        last_name (:obj:`str`, optional): User's or bot's last name.
        username (:obj:`str`, optional): User's or bot's username.
        language_code (:obj:`str`, optional): IETF language tag of the user's language.
        bot (:class:`telegram.Bot`, optional): The Bot to use for instance methods.

    """

    def __init__(self,
                 id,
                 first_name,
                 is_bot,
                 last_name=None,
                 username=None,
                 language_code=None,
                 bot=None,
                 **kwargs):
        # Required
        self.id = int(id)
        self.first_name = first_name
        self.is_bot = is_bot
        # Optionals
        self.last_name = last_name
        self.username = username
        self.language_code = language_code

        self.bot = bot

        self._id_attrs = (self.id,)

    @property
    def name(self):
        """:obj:`str`: Convenience property. If available, returns the user's :attr:`username`
        prefixed with "@". If :attr:`username` is not available, returns :attr:`full_name`."""
        if self.username:
            return '@{}'.format(self.username)
        return self.full_name

    @property
    def full_name(self):
        """:obj:`str`: Convenience property. The user's :attr:`first_name`, followed by (if
        available) :attr:`last_name`."""

        if self.last_name:
            return u'{} {}'.format(self.first_name, self.last_name)
        return self.first_name

    @property
    def link(self):
        """:obj:`str`: Convenience property. If :attr:`username` is available, returns a t.me link
        of the user."""

        if self.username:
            return "https://t.me/{}".format(self.username)
        return None

    @classmethod
    def de_json(cls, data, bot):
        if not data:
            return None

        data = super(User, cls).de_json(data, bot)

        return cls(bot=bot, **data)

    def get_profile_photos(self, *args, **kwargs):
        """
        Shortcut for::

                bot.get_user_profile_photos(update.message.from_user.id, *args, **kwargs)

        """

        return self.bot.get_user_profile_photos(self.id, *args, **kwargs)

    @classmethod
    def de_list(cls, data, bot):
        if not data:
            return []

        users = list()
        for user in data:
            users.append(cls.de_json(user, bot))

        return users

    def mention_markdown(self, name=None):
        """
        Args:
            name (:obj:`str`): The name used as a link for the user. Defaults to :attr:`full_name`.

        Returns:
            :obj:`str`: The inline mention for the user as markdown.

        """
        if name:
            return util_mention_markdown(self.id, name)
        return util_mention_markdown(self.id, self.full_name)

    def mention_html(self, name=None):
        """
        Args:
            name (:obj:`str`): The name used as a link for the user. Defaults to :attr:`full_name`.

        Returns:
            :obj:`str`: The inline mention for the user as HTML.

        """
        if name:
            return util_mention_html(self.id, name)
        return util_mention_html(self.id, self.full_name)

    def send_message(self, *args, **kwargs):
        """Shortcut for::

            bot.send_message(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_message(self.id, *args, **kwargs)

    def send_photo(self, *args, **kwargs):
        """Shortcut for::

            bot.send_photo(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_photo(self.id, *args, **kwargs)

    def send_audio(self, *args, **kwargs):
        """Shortcut for::

            bot.send_audio(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_audio(self.id, *args, **kwargs)

    def send_document(self, *args, **kwargs):
        """Shortcut for::

            bot.send_document(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_document(self.id, *args, **kwargs)

    def send_animation(self, *args, **kwargs):
        """Shortcut for::

            bot.send_animation(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_animation(self.id, *args, **kwargs)

    def send_sticker(self, *args, **kwargs):
        """Shortcut for::

            bot.send_sticker(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_sticker(self.id, *args, **kwargs)

    def send_video(self, *args, **kwargs):
        """Shortcut for::

            bot.send_video(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_video(self.id, *args, **kwargs)

    def send_video_note(self, *args, **kwargs):
        """Shortcut for::

            bot.send_video_note(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_video_note(self.id, *args, **kwargs)

    def send_voice(self, *args, **kwargs):
        """Shortcut for::

            bot.send_voice(User.id, *args, **kwargs)

        Where User is the current instance.

        Returns:
            :class:`telegram.Message`: On success, instance representing the message posted.

        """
        return self.bot.send_voice(self.id, *args, **kwargs)

class MessageEntity(TelegramObject):
    """
    This object represents one special entity in a text message. For example, hashtags,
    usernames, URLs, etc.

    Attributes:
        type (:obj:`str`): Type of the entity.
        offset (:obj:`int`): Offset in UTF-16 code units to the start of the entity.
        length (:obj:`int`): Length of the entity in UTF-16 code units.
        url (:obj:`str`): Optional. Url that will be opened after user taps on the text.
        user (:class:`telegram.User`): Optional. The mentioned user.

    Args:
        type (:obj:`str`): Type of the entity. Can be mention (@username), hashtag, bot_command,
            url, email, bold (bold text), italic (italic text), code (monowidth string), pre
            (monowidth block), text_link (for clickable text URLs), text_mention (for users
            without usernames).
        offset (:obj:`int`): Offset in UTF-16 code units to the start of the entity.
        length (:obj:`int`): Length of the entity in UTF-16 code units.
        url (:obj:`str`, optional): For "text_link" only, url that will be opened after usertaps on
            the text.
        user (:class:`telegram.User`, optional): For "text_mention" only, the mentioned user.

    """

    def __init__(self, type, offset, length, url=None, user=None, **kwargs):
        # Required
        self.type = type
        self.offset = offset
        self.length = length
        # Optionals
        self.url = url
        self.user = user

        self._id_attrs = (self.type, self.offset, self.length)

    @classmethod
    def de_json(cls, data, bot):
        data = super(MessageEntity, cls).de_json(data, bot)

        if not data:
            return None

        data['user'] = User.de_json(data.get('user'), bot)

        return cls(**data)

    @classmethod
    def de_list(cls, data, bot):
        if not data:
            return list()

        entities = list()
        for entity in data:
            entities.append(cls.de_json(entity, bot))

        return entities

    MENTION = 'mention'
    """:obj:`str`: 'mention'"""
    HASHTAG = 'hashtag'
    """:obj:`str`: 'hashtag'"""
    CASHTAG = 'cashtag'
    """:obj:`str`: 'cashtag'"""
    PHONE_NUMBER = 'phone_number'
    """:obj:`str`: 'phone_number'"""
    BOT_COMMAND = 'bot_command'
    """:obj:`str`: 'bot_command'"""
    URL = 'url'
    """:obj:`str`: 'url'"""
    EMAIL = 'email'
    """:obj:`str`: 'email'"""
    BOLD = 'bold'
    """:obj:`str`: 'bold'"""
    ITALIC = 'italic'
    """:obj:`str`: 'italic'"""
    CODE = 'code'
    """:obj:`str`: 'code'"""
    PRE = 'pre'
    """:obj:`str`: 'pre'"""
    TEXT_LINK = 'text_link'
    """:obj:`str`: 'text_link'"""
    TEXT_MENTION = 'text_mention'
    """:obj:`str`: 'text_mention'"""
    ALL_TYPES = [
        MENTION, HASHTAG, CASHTAG, PHONE_NUMBER, BOT_COMMAND, URL,
        EMAIL, BOLD, ITALIC, CODE, PRE, TEXT_LINK, TEXT_MENTION
    ]
    """List[:obj:`str`]: List of all the types."""



# This is a fun one.
def _calc_emoji_offset(to_calc) -> int:
    # Get all emoji in text.
    emoticons = emoji.get_emoji_regexp().finditer(to_calc)
    # Check the utf16 length of the emoji to determine the offset it caused.
    # Normal, 1 character emoji don't affect; hence sub 1.
    # special, eg with two emoji characters (eg face, and skin col) will have length 2, so by subbing one we
    # know we'll get one extra offset,
    return sum(len(e.group(0).encode('utf-16-le')) // 2 - 1 for e in emoticons)


def markdown_parser(txt: str, entities: Dict[MessageEntity, str] = None, offset: int = 0) -> str:
    """
    Parse a string, escaping all invalid markdown entities.

    Escapes URL's so as to avoid URL mangling.
    Re-adds any telegram code entities obtained from the entities object.

    :param txt: text to parse
    :param entities: dict of message entities in text
    :param offset: message offset - command and notename length
    :return: valid markdown string
    """
    if not entities:
        entities = {}
    if not txt:
        return ""

    prev = 0
    res = ""
    # Loop over all message entities, and:
    # reinsert code
    # escape free-standing urls
    for ent, ent_text in entities.items():
        if ent.offset < -offset:
            continue

        start = ent.offset + offset  # start of entity
        end = ent.offset + offset + ent.length - 1  # end of entity

        # we only care about code, url, text links
        if ent.type in ("code", "url", "text_link"):
            # count emoji to switch counter
            count = _calc_emoji_offset(txt[:start])
            start -= count
            end -= count

            # URL handling -> do not escape if in [](), escape otherwise.
            if ent.type == "url":
                if any(match.start(1) <= start and end <= match.end(1) for match in LINK_REGEX.finditer(txt)):
                    continue
                # else, check the escapes between the prev and last and forcefully escape the url to avoid mangling
                else:
                    # TODO: investigate possible offset bug when lots of emoji are present
                    res += _selective_escape(txt[prev:start] or "") + escape_markdown(ent_text)

            # code handling
            elif ent.type == "code":
                res += _selective_escape(txt[prev:start]) + '`' + ent_text + '`'

            # handle markdown/html links
            elif ent.type == "text_link":
                res += _selective_escape(txt[prev:start]) + "[{}]({})".format(ent_text, ent.url)

            end += 1

        # anything else
        else:
            continue

        prev = end

    res += _selective_escape(txt[prev:])  # add the rest of the text
    return res


def button_markdown_parser(txt: str, entities: Dict[MessageEntity, str] = None, offset: int = 0) -> (str, List):
    markdown_note = markdown_parser(txt, entities, offset)
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            # create a thruple with button label, url, and newline status
            buttons.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev:match.start(1)]
            prev = match.end(1)
        # if odd, escaped -> move along
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += markdown_note[prev:]

    return note_data, buttons


def get_welcome_type(msg):
    data_type = None
    content = None
    text = ""

    args = msg.text.split(None, 1)  # use python's maxsplit to separate cmd and args

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= 2:
        offset = len(args[1]) - len(msg.text)  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(args[1], entities=None, offset=offset)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif msg.reply_to_message and msg.reply_to_message.sticker:
        content = msg.reply_to_message.sticker.file_id
        text = msg.reply_to_message.text
        data_type = Types.STICKER

    elif msg.reply_to_message and msg.reply_to_message.document:
        content = msg.reply_to_message.document.file_id
        text = msg.reply_to_message.text
        data_type = Types.DOCUMENT

    elif msg.reply_to_message and msg.reply_to_message.photo:
        content = msg.reply_to_message.photo[-1].file_id  # last elem = best quality
        text = msg.reply_to_message.text
        data_type = Types.PHOTO

    elif msg.reply_to_message and msg.reply_to_message.audio:
        content = msg.reply_to_message.audio.file_id
        text = msg.reply_to_message.text
        data_type = Types.AUDIO

    elif msg.reply_to_message and msg.reply_to_message.voice:
        content = msg.reply_to_message.voice.file_id
        text = msg.reply_to_message.text
        data_type = Types.VOICE

    elif msg.reply_to_message and msg.reply_to_message.video:
        content = msg.reply_to_message.video.file_id
        text = msg.reply_to_message.text
        data_type = Types.VIDEO

    return text, data_type, content, buttons

def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn.same_line and keyb:
            keyb[-1].add(InlineKeyboardButton(btn.name, url=btn.url))
        else:
            keyb.append(InlineKeyboardButton(btn.name, url=btn.url))

    return keyb


def revert_buttons(buttons):
    res = ""
    for btn in buttons:
        if btn.same_line:
            res += "\n[{}](buttonurl://{}:same)".format(btn.name, btn.url)
        else:
            res += "\n[{}](buttonurl://{})".format(btn.name, btn.url)

    return res

