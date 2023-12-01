from datetime import datetime
from utils.history import add_history
from handlers.methods_result import result
from config import bot
from utils.check_functions import check_amount_cases, check_amount_countries
from telebot.types import Message
from utils.exit import stopping


def high_step1(message: Message) -> None:
    """
    Функция, которая вызывается из основного скрипта при выборе пользователя /high. У него запрашивается параметр:
    количество случаев заболеваемости, результат функция передает в следующую функцию low_step2.
    :return: None
    """
    amount_cases = bot.send_message(
        message.chat.id,
        "Введите количество случаев заболеваемости, от которых начать поиск"
    )
    bot.register_next_step_handler(amount_cases, high_step2)


def high_step2(message: Message) -> None:
    """
    Функция, которая вызывается функцией high_step1. В ней проверяется корректность ввода параметра message
    (количество случаев заболеваемости).
        Если он введен цифрами и не выходит за пределы диапазона, у пользователя
    запрашивается следующий параметр - количество стран, вызывается функция high_step2 куда передается этот и
    предыдущий параметр.
        Иначе, снова вызывается функция high_step1.
    :param message: Количество случаев заболеваемости
    :return: None
    """
    if stopping(message=message):
        return
    if check_amount_cases(message=message, value=message.text):
        amount_countries = bot.send_message(
            message.chat.id,
            "Введите количество стран, которые вы хотите увидеть"
        )
        bot.register_next_step_handler(amount_countries, high_step3, message)
    else:
        high_step1(message=message)


def high_step3(message: Message, message_step2: Message) -> None:
    """
        Функция, которая вызывается функцией high_step2. В ней проверяется корректность ввода
    параметра message (количество стран).
        Если он введен цифрами и не выходит за пределы диапазона, в метод /history
    записывается вызов метода /high с указанными пользователем параметрами, вызывается
    метод класса High result в который передается 2 параметра: количество случаев заболеваемости и
    количество стран, после этого бот выводит результат с указанными параметрами.
        Иначе снова вызывается функция high_step2.
    :param message: Количество стран
    :param message_step2: Количество случаев заболеваемости
    :return: None
    """
    if stopping(message=message):
        return
    if check_amount_countries(message=message, value=message.text):
        add_history(
            tg_id=message.chat.id,
            info=f"/high - вывод стран с наибольшим показателем заболеваемости, время - {datetime.now()}. "
            f"Параметры: заболеваемость {message_step2.text}, кол-во стран: {message.text}"
        )

        bot.send_message(message.chat.id, result(
            amount_cases=int(message_step2.text),
            amount_countries=int(message.text),
            flag="high")
        )
    else:
        high_step2(message=message_step2)
