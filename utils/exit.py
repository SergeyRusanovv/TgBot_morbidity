from typing import List
from telebot.types import Message
from config import bot

stopping_words: List[str] = [
    "STOP",
    "EXIT",
    "BREAK",
    "ВЫХОД",
    "ХВАТИТ",
    "ВЫЙДИ",
    "СТОП"
]


def stopping(message: Message) -> bool:
    """
    Функция для проверки стоп слова в сообщении
    :param message:
    :return: Правда или ложь
    """
    if message.text.upper() in stopping_words:
        bot.send_message(message.chat.id, "А мы ведь так хорошо ладили... \U0001F97A")
        return True
    return False
