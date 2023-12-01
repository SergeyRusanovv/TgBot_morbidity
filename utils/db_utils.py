from typing import Dict
from peewee import IntegrityError
from data_base.db_init import Morbidity, User
from telebot.types import Message


def all_countries() -> Dict[str, int]:
    """
    Функция для получения всех стран с заболеваемостью
    :return: словарь со странами и заболеваемостью
    """
    countries = Morbidity.select().execute()
    return {morb.country: morb.morbidity for morb in countries}


def register_user(message: Message) -> None:
    """
    Функция для регистрации нового пользователя
    :return: None
    """
    User.create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )


def get_user(message: Message) -> (User or bool):
    """Функция для получения конкретного пользователя из базы данных"""
    try:
        return User.get_or_none(User.user_id == message.from_user.id)
    except IntegrityError:
        return None
