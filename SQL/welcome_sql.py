import threading

from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, BigInteger
from SQL.sql import SESSION, BASE

DEFAULT_WELCOME = "Hey {first}, how are you?"
DEFAULT_GOODBYE = "Nice knowing ya!"


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    welcome_type = Column(Integer, default=Types.TEXT.value)
    custom_welcome = Column(UnicodeText, default=DEFAULT_WELCOME)
    def __init__(self, chat_id):
        self.chat_id = chat_id

Welcome.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.custom_welcome, welc.welcome_type
    else:
        # Welcome by default.
        return True, DEFAULT_WELCOME, Types.TEXT

def set_custom_welcome(chat_id, custom_welcome, welcome_type):

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_welcome:
            welcome_settings.custom_welcome = custom_welcome
            welcome_settings.welcome_type = welcome_type.value

        else:
            welcome_settings.custom_welcome = DEFAULT_WELCOME
            welcome_settings.welcome_type = Types.TEXT.value
        SESSION.add(welcome_settings)

        SESSION.commit()
