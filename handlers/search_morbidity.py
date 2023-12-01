from utils.history import add_history
from utils.db_utils import all_countries
from datetime import datetime
from utils.check_functions import check_amount_cases
from telebot.types import Message
from config import bot
from utils.exit import stopping


def get_number(message: Message) -> None:
    """
    Функция вызываемая из основного скрипта. Запрашивает у пользователя параметр заболеваемость
    для поиска страны и вызывает функцию case_search передавая этот параметр.
    :return: None
    """
    users_number = bot.send_message(
        message.chat.id,
        "Введите значение заболеваемость"
    )
    bot.register_next_step_handler(users_number, case_search)


def case_search(message: Message) -> None:
    """
    Функция для поиска страны по введенному пользователем параметру заболеваемость.
        Если параметр введен цифрами и не выходит за границы диапазона, то пользователю выводится результат
    поиска (либо ближайший к параметру).
        Иначе вызывается функция get_number.
    :return: None
    """
    if stopping(message=message):
        return
    if check_amount_cases(message=message, value=message.text):
        country_dict = all_countries()
        new_dict = {value: key for key, value in country_dict.items()}
        if int(message.text) in new_dict:
            add_history(
                tg_id=message.chat.id,
                info=f"/search_morbidity - поиск страны по введенному параметру заболеваемость, "
                     f"время {datetime.now()}"
                     f"Параметры: введенный текст - {message.text}"
            )
            bot.send_message(
                message.chat.id,
                f"Страна: {new_dict[int(message.text)]} - {message.text} заболевших")

        else:
            value_1 = int(message.text)
            value_2 = int(message.text)
            while True:
                value_1 += 1
                if value_1 in new_dict:
                    add_history(
                        tg_id=message.chat.id,
                        info=f"/search_morbidity - поиск страны по введенному параметру заболеваемость, "
                             f"время {datetime.now()}"
                             f"Параметры: введенный текст - {message.text}"
                    )
                    bot.send_message(
                        message.chat.id,
                        f"Ближайшая страна по уровню заболеваемости\n"
                        f"{new_dict[value_1]} - {value_1} заболевших"
                    )
                    break

                value_2 += 1
                if value_2 in new_dict:
                    add_history(
                        tg_id=message.chat.id,
                        info=f"/search_morbidity - поиск страны по введенному параметру заболеваемость, "
                             f"время {datetime.now()}"
                             f"Параметры: введенный текст - {message.text}"
                    )
                    bot.send_message(
                        message.chat.id,
                        f"Ближайшая страна по уровню заболеваемости:\n"
                        f"{new_dict[value_2]} - {value_2} заболевших")
                    break

    else:
        get_number(message)
