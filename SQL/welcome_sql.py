import threading

from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, BigInteger
from SQL.sql import SESSION, BASE

DEFAULT_WELCOME = "Hey {first}, how are you?"
DEFAULT_GOODBYE = "Nice knowing ya!"


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    custom_welcome = Column(UnicodeText, default=DEFAULT_WELCOME)
    def __init__(self, chat_id):
        self.chat_id = chat_id

Welcome.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.custom_welcome
    else:
        # Welcome by default.
        return True, DEFAULT_WELCOME

def set_custom_welcome(chat_id, custom_welcome):

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_welcome:
            welcome_settings.custom_welcome = custom_welcome

        else:
            welcome_settings.custom_welcome = DEFAULT_WELCOME

        SESSION.add(welcome_settings)

        SESSION.commit()
