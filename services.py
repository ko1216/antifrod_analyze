import os
import json
import requests
from dotenv import load_dotenv

from functions import get_currencies_list, rows

load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
CURRENCY_RATES_FILE = 'currency_rates.json'


def fetch_currency_rates(rate: str):
    """
    Функция получает ежедневный курс валюты к евро в период с 29.12.2021 по 30.03.2022
    :param rate: строка
    :return: json
    """
    url = 'https://api.apilayer.com/exchangerates_data/timeseries'
    response = requests.get(url, headers={'apikey': API_KEY},
                            params={
                                'base': rate,
                                'start_date': '2021-12-29',
                                'end_date': '2022-03-30'
                            }
                            )

    if response.status_code == 200:
        return response.json()
    else:
        print(response)


def save_to_json(data: dict) -> None:
    """
    Сохраняет данные в json файл.
    :param data: dict
    """
    with open(CURRENCY_RATES_FILE, 'a') as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE) as f:
                data_list = json.load(f)
                data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w') as f:
                json.dump(data_list, f)


def write_currencies_to_file(data: list) -> None:
    """
    Функция итеррирует список валют для конечной записи их в json файл
    :param data:
    :return:
    """
    for currency in data:
        currency_rates = fetch_currency_rates(currency)
        save_to_json(currency_rates)


write_currencies_to_file(get_currencies_list(rows))
