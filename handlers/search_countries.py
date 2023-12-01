import re
from typing import Dict, List
from config import bot
from utils.history import add_history
from datetime import datetime
from telebot.types import Message
from utils.db_utils import all_countries
from utils.exit import stopping


def get_line(message: Message) -> None:
    """
    Функция вызываемая из основного скрипта. Запрашивает у пользователя текст для поиска стран и вызывает функцию
    search_countries передавая этот текст.
    :return: None
    """
    users_line = bot.send_message(
        message.chat.id,
        "Введите текст для поиска стран по совпадениям."
    )
    bot.register_next_step_handler(users_line, search_countries)


def search_countries(message: Message) -> None:
    """
    Функция для поиска стран по введенному пользователем тексту. Пользователю выводится результат поиска либо сообщение:
    совпадений не найдено.
    :return: None
    """
    if stopping(message=message):
        return
    dict_countries: Dict[str: int] = all_countries()
    lst_countries: List[str] = ["3" + country + "3" for country in dict_countries.keys()]
    result_search: List[str] = re.findall(rf"\b\d{message.text.capitalize()}\D*", string=str(lst_countries))

    if len(result_search) == 0:
        add_history(
            tg_id=message.chat.id,
            info=f"/search_countries - поиск стран по введенному тексту, время - {datetime.now()}. "
                 f"Параметры: введенный текст - {message.text}. Совпадений нет.")
        bot.send_message(message.chat.id, "Совпадений не найдено!")
    else:
        str_res: str = ""
        for word in result_search:
            a = word.replace("3", "")
            str_res += f"Страна: {a} - {dict_countries[a]} заболевших\n"
        add_history(
            tg_id=message.chat.id,
            info=f"/search_countries - поиск стран по введенному тексту, время - {datetime.now()}. "
                 f"Параметры: введенный текст - {message.text}.")
        bot.send_message(message.chat.id, str_res)
