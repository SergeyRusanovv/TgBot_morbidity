from datetime import datetime
from utils.history import add_history
from handlers.methods_result import result
from config import bot
from utils.check_functions import check_amount_cases, check_amount_countries
from telebot.types import Message
from utils.exit import stopping


def customs_step1(message: Message) -> None:
    """
    Функция, которая вызывается из основного скрипта при выборе пользователя /customs. У него запрашивается параметр:
    минимальное количество случаев заболеваемости, результат функция передает в следующую функцию customs_step2.
    :return: None
    """
    amount_cases_min = bot.send_message(
        message.chat.id,
        "Введите минимальное количество случаев заболеваемости, от которых начать поиск"
    )
    bot.register_next_step_handler(amount_cases_min, customs_step2)


def customs_step2(message: Message) -> None:
    """
    Функция, которая вызывается функцией customs_step1. В ней проверяется корректность ввода параметра message
    (минимальное количество случаев заболеваемости).
        Если он введен цифрами и не выходит за пределы диапазона, у пользователя запрашивается следующий параметр -
    максимальное количество случаев заболеваемости, вызывается функция customs_step3 куда передается этот и
    предыдущий параметр.
        Иначе, снова вызывается функция customs_step1.
    :param message: Минимальное количество случаев заболеваемости
    :return: None
    """
    if stopping(message=message):
        return
    if check_amount_cases(message=message, value=message.text):
        amount_cases_max = bot.send_message(
            message.chat.id,
            "Введите максимальное количество случаев заболеваемости"
        )
        bot.register_next_step_handler(amount_cases_max, customs_step3, message)
    else:
        customs_step1(message=message)


def customs_step3(message: Message, message_step2: Message) -> None:
    """
    Функция, которая вызывается функцией customs_step2. В ней проверяется корректность ввода параметра message
    (максимальное количество случаев заболеваемости).
        Если он введен цифрами и не выходит за пределы диапазона, у пользователя запрашивается следующий параметр -
    у пользователя запрашивается следующий параметр - количество стран, вызывается функция customs_step4
    куда передается минимальное и максимальное количество случаев заболеваемости и количество стран.
        Иначе, снова вызывается функция customs_step2.
    :param message: Минимальное количество случаев заболеваемости
    :param message_step2: Максимальное количество случаев заболеваемости
    :return: None
    """
    if stopping(message=message):
        return
    if check_amount_cases(message=message, value=message.text):
        amount_countries = bot.send_message(
            message.chat.id,
            "Введите количество стран, которые вы хотите увидеть"
        )
        bot.register_next_step_handler(amount_countries, customs_step4, message_step2, message)
    else:
        customs_step2(message=message_step2)


def customs_step4(message: Message, message_step1: Message, message_step2: Message) -> None:
    """
        Функция, которая вызывается функцией customs_step3. В ней проверяется корректность ввода параметра
    message (количество стран).
        Если он введен цифрами и не выходит за пределы диапазона, в метод /history записывается вызов
    метода /customs с указанными пользователем параметрами и формируется ответ.
        Иначе снова вызывается функция customs_step3.
    :param message: Количество стран
    :param message_step2: Максимальное количество случаев заболеваемости.
    :param message_step1: Минимальное количество случаев заболеваемости.
    :return: None
    """
    if stopping(message=message):
        return
    if check_amount_countries(message=message, value=message.text):
        add_history(
            tg_id=message.chat.id,
            info=f"/customs - вывод стран с наибольшим показателем заболеваемости, время - {datetime.now()}. " 
            f"Параметры: нижний порог заболеваемости {message_step1.text}, "
            f"верхний порог заболеваемости {message_step2.text}, " 
            f"Количество стран: {message.text}"
        )

        bot.send_message(message.chat.id, result(
            amount_cases=int(message_step1.text),
            amount_cases_max=int(message_step2.text),
            amount_countries=int(message.text),
            flag="custom")
        )
    else:
        customs_step3(message=message_step2, message_step2=message_step2)
