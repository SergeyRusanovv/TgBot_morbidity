from peewee import (
    SqliteDatabase,
    CharField,
    IntegerField,
    Model,
    ForeignKeyField,
    AutoField
)


db = SqliteDatabase("data_base/my_db.db")


class BaseModel(Model):
    """Базовый класс базы данных"""
    class Meta:
        database = db


class User(BaseModel):
    """Модель пользователя"""
    user_id = IntegerField(
        primary_key=True,
        verbose_name="Первичный ключ модели, будет совпадать с Telegram ID",
    )
    username = CharField(verbose_name="Никнейм в Telegram")
    first_name = CharField(verbose_name="Имя в Telegram")
    last_name = CharField(verbose_name="Фамилия в Telegram", null=True)


class History(BaseModel):
    """Модель истории просмотров"""
    history_id = AutoField(verbose_name="Первичный ключ истории просмотров")
    user = ForeignKeyField(
        User,
        verbose_name="Пользователь, которому принадлежит история",
        backref="histories"
    )
    info = CharField(verbose_name="История просмотров")


class Morbidity(BaseModel):
    """Модель заболеваемости"""
    morb_id = AutoField(verbose_name="Первичный ключ заболеваемости")
    country = CharField(verbose_name="Страна")
    morbidity = IntegerField(verbose_name="Заболеваемость в стране")


if __name__ == "__main__":
    db.create_tables(BaseModel.__subclasses__())
