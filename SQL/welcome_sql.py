import threading
from enum import IntEnum, unique
from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, BigInteger
from SQL.__init__ import SESSION, BASE

DEFAULT_WELCOME = "Hey {first}, how are you?"
DEFAULT_GOODBYE = "Nice knowing ya!"

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


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    welcome_type = Column(Integer, default=Types.TEXT.value)
    custom_welcome = Column(UnicodeText, default=DEFAULT_WELCOME)
    def __init__(self, chat_id):
        self.chat_id = chat_id

class WelcomeButtons(BASE):
    __tablename__ = "welcome_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line



Welcome.__table__.create(checkfirst=True)
WelcomeButtons.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()
WELC_BTN_LOCK = threading.RLock()

def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.custom_welcome
    else:
        # Welcome by default.
        return True, DEFAULT_WELCOME

def set_custom_welcome(chat_id, custom_welcome, welcome_type, buttons=None):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        prev_welcome = SESSION.query(Welcome).filter(Welcome.chat_id == str(chat_id)).all()
        for prev in prev_welcome:
            SESSION.delete(prev)
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        welcome_settings = Welcome(str(chat_id))
        welcome_settings.custom_welcome = custom_welcome
        welcome_settings.welcome_type = welcome_type.value

        SESSION.add(welcome_settings)

        with WELC_BTN_LOCK:
            prev_buttons = SESSION.query(WelcomeButtons).filter(WelcomeButtons.chat_id == str(chat_id)).all()
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = WelcomeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)


        SESSION.commit()

def get_welc_buttons(chat_id):
    try:
        return SESSION.query(WelcomeButtons).filter(WelcomeButtons.chat_id == str(chat_id)).order_by(
            WelcomeButtons.id).all()
    finally:
        SESSION.close()
