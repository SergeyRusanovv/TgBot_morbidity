from handlers.high import high_step1
from handlers.low import low_step1
from handlers.customs import customs_step1
from handlers.search_countries import get_line
from handlers.search_morbidity import get_number
from datetime import datetime
from config import bot
from utils.history import add_history, get_history
from telebot.types import Message
from utils.db_utils import register_user, get_user


@bot.message_handler(commands=["start"])
def start_message(message: Message) -> None:
    """
    Метод для приветствия нового пользователя при выборе им команды /start.
    :return: None
    """
    if get_user(message) is None:
        register_user(message=message)
        bot.send_message(
            message.chat.id,
            "Привет! Я ваш помощник телеграм-бот по заболеваемости COVID-19 в разных странах мира \U0001F590.\n"
            " Готовы узнать что-нибудь новенькое? \U0001F913)))"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Привет! Я ваш помощник телеграм-бот по заболеваемости COVID-19 в разных странах мира \U0001F590.\n"
            f"Рад вас снова видеть {message.from_user.first_name}!"
            " Готовы узнать что-нибудь новенькое? \U0001F913)))"
        )
    return


@bot.message_handler(commands=["help"])
def help_hand(message: Message) -> None:
    """
    Метод для навигации пользователя по функциям телеграмм бота. При его вызове бот выводит текст для навигации и делает запись
    в метод /history.
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    add_history(
        message.chat.id,
        f"/help - навигация по боту, время - {datetime.now()}"
    )
    bot.send_message(
        message.chat.id,
        "Сейчас помогу... \U0001F917\n"
        "/low - вывод стран с наименьшим показателем случаев заболевания в порядке убывания\n"
        "/high - вывод стран с наибольшим показателем случаев заболевания в порядке возрастания\n"
        "/customs - вывод стран с диапазоном заданных значений случаев заболевания (не менее 1 и не более 50)\n"
        "/history - история запросов (последние 10)\n"
        "/search_countries - поиск стран из введенного вами текста (на англ. языке)\n"
        "/search_morbidity - поиск страны по введенному параметру заболеваемость (или ближайшую к параметру)\n"
        "Если вдруг передумаете что то вводить, напишите <выход> \u270D"
    )
    return


@bot.message_handler(commands=["high"])
def high(message: Message) -> None:
    """
    Функция, которая вызывается при выборе пользователем метода /high. Она вызывает функцию high_step1 из папки handlers файла high.py
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    high_step1(message=message)


@bot.message_handler(commands=["low"])
def low(message: Message) -> None:
    """
    Функция, которая вызывается при выборе пользователем метода /low.
    Она вызывает функцию low_step1 из папки handlers файла low.py
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    low_step1(message=message)


@bot.message_handler(commands=["customs"])
def customs(message: Message) -> None:
    """
    Функция, которая вызывается при выборе пользователем метода /customs.
    Она вызывает функцию customs_step1 из папки handlers файла customs.py
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    customs_step1(message=message)


@bot.message_handler(commands=["history"])
def history(message: Message) -> None:
    """
    Метод для вывода пользователю истории запросов.
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    bot.send_message(message.chat.id, f"История:\n{get_history(message.chat.id)}")
    return


@bot.message_handler(commands=["search_countries"])
def search_cou(message: Message) -> None:
    """
    Метод для вывода пользователю стран по совпадению ввода.
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    get_line(message=message)
    return


@bot.message_handler(commands=["search_morbidity"])
def search_morb(message: Message) -> None:
    """
    Метод для поиска страны по введенному параметру заболеваемость (или ближайшую к параметру)
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    get_number(message=message)


@bot.message_handler(content_types=["text"])
def greeting(message: Message) -> None:
    """
    Метод для ответа бота на приветствие пользователя или на некорректно введенную им команду.
    :return: None
    """
    if get_user(message) is None:
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Напишите /start")
        return
    if message.text.upper() == "ПРИВЕТ" or message.text == "/hello-world":
        bot.send_message(message.chat.id, "Здравствуйте, чем могу вам помочь?. \U0001F60E")
    else:
        bot.send_message(
            message.chat.id,
            "Я вас не понимаю. Пожалуйста, введите корректное сообщение или /help. \U0001F62F"
        )


if __name__ == "__main__":
    bot.infinity_polling()
