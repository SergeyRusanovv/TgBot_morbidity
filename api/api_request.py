import json
import requests
from data_base.db_init import Morbidity


def api_request() -> None:
    """
    Функция для API запроса информации о странах и их заболеваемости с
    последующей записью результата в базу данных
    :return: None
    """
    all_text = json.loads(requests.get(
        "https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=1").text)
    for line in all_text:
        Morbidity.create(
            country=line["country"],
            morbidity=int(line["timeline"]["10/29/23"])
        )


if __name__ == "__main__":
    api_request()
