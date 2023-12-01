from data_base.db_init import History


def get_history(tg_id: int) -> str:
    """
    Функция, которая позволяет вывести пользователю историю запросов.
    :param tg_id: Телеграмм id пользователя.
    :return: История просмотров или сообщение о пустой истории.
    """
    result = ""
    all_history = History.filter(History.user == tg_id)
    if all_history is None:
        return "Ваша история пуста!"
    for index, record in enumerate(all_history):
        result += f"{index + 1}. {record.info}\n"
    return result


def add_history(tg_id: int, info: str) -> None:
    """
    Функция, которая позволяет записывать запросы пользователя в json-файл под уникальным id.
    :param tg_id: Телеграмм id пользователя
    :param info: Строка с запросом пользователя
    :return: None
    """
    all_history = History.filter(History.user == tg_id)
    if len(all_history) >= 10:
        for hist in all_history:
            min_id = hist.history_id
            break
        History.delete_by_id(min_id)
    History.create(user=tg_id, info=info)
