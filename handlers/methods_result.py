from data_base.db_init import Morbidity


def result(amount_cases: int, amount_countries: int, flag: str, amount_cases_max: int = None) -> str:
    """
    Метод класса для вывода отсортированного результата стран по заболеваемости в порядке возрастания.
    :param amount_cases: Порог заболеваемости
    :param amount_countries: Количество стран
    :param flag: Флаг для выполнения определенного ORM запроса
    :param amount_cases_max: Верхний порог заболеваемости для метода custom
    :return: строка с отсортированными данными
    """

    result: str = ""
    if flag == "custom":
        if amount_cases_max < amount_cases:
            amount_cases_max, amount_cases = amount_cases, amount_cases_max
        all_countries = (
            Morbidity.select().
            where(Morbidity.morbidity.between(amount_cases, amount_cases_max)).
            order_by(Morbidity.morbidity).
            limit(amount_countries).
            execute()
        )
    elif flag == "high":
        all_countries = (
            Morbidity.select().
            where(Morbidity.morbidity > amount_cases).
            order_by(Morbidity.morbidity).
            limit(amount_countries).execute()
        )
    elif flag == "low":
        all_countries = (
            Morbidity.select().
            where(Morbidity.morbidity < amount_cases).
            order_by(-Morbidity.morbidity).
            limit(amount_countries).
            execute()
        )

    for country in all_countries:
        result += f"{country.country} - {country.morbidity}\n"
    return result
