from utils.db_utils import all_countries
from config import bot
from telebot.types import Message


def check_amount_cases(message: Message, value: str) -> bool:
    """
    Функция для проверки параметра 'случаи заболеваемости'. Он должен входить за диапазон и введен цифрами.
    :param value: Значение, введенное пользователем
    :return: bool
    """
    morbidity_list = all_countries()
    try:
        int(value)
    except ValueError:
        bot.send_message(message.chat.id, "Введены символы, отличные от цифр")
        return False
    if (int(value) < min(morbidity_list.values())
            or int(value) > max(morbidity_list.values())):
        bot.send_message(message.chat.id, "Случаи заболеваемости выходят за границы диапазона")
        return False
    return True


def check_amount_countries(message: Message, value: str) -> bool:
    """
    Функция для проверки параметра 'количество стран'. Они должны входить в диапазон от 1 до 50 и введены цифрами.
    :param value: Значение, введенное пользователем
    :return: bool
    """
    try:
        int(value)
    except ValueError:
        bot.send_message(message.chat.id, "Введены символы, отличные от цифр")
        return False
    if (int(value) < 1) or (int(value) > 50):
        bot.send_message(message.chat.id, "Количество стран выходит за пределы диапазона")
        return False
    return True
