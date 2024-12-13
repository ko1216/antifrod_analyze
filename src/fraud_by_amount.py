import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
CURRENCY_RATES_FILE = 'currency_rates.json'


def get_currencies_list(data: list) -> list:
    """
    Функция записывает весь список используемых валют из отчета за исключением USD, EUR, RUB
    :param data: Список всех операций
    :return: Список
    """
    currencies = set()
    for row in data:
        if row[7] != 'USD' and row[7] != 'EUR' and row[7] != 'RUB' and row[7]:
            currencies.add(row[7])
    return list(currencies)


def fetch_currency_rates(rate: str):
    """
    Функция получает ежедневный курс валюты к евро в период с 29.12.2021 по 30.03.2022 в формате json
    :param rate: Сокращенное название валюты - строка.
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


def save_to_json(data: dict, filename=CURRENCY_RATES_FILE) -> None:
    """
    Сохраняет данные json в файл.
    :param data: dict
    """
    with open(filename, 'a') as f:
        if os.stat(filename).st_size == 0:
            json.dump([data], f)
        else:
            with open(filename) as f:
                data_list = json.load(f)
                data_list.append(data)
            with open(filename, 'w') as f:
                json.dump(data_list, f, indent=4)


def write_currencies_to_file(data: list) -> None:
    """
    Функция итеррирует по списку уникальных валют, полученных функцией get_currencies_list
    и вызывает функцию fetch_currency_rates для получения ежедневного курса валюты для каждой.
    :param data: Список уникальных валют, используемых в общем списке операций (кроме RUB, USD, EUR)
    """
    for currency in data:
        currency_rates = fetch_currency_rates(currency)
        save_to_json(currency_rates)


def find_frod_by_amount(data: list, foreign_amount: int, rub_amount: int, filename=CURRENCY_RATES_FILE) -> list:
    """
    Функция ищет все строки из списка операция, где сумма операции более:
    500 000 рублей, 5 000 USD или EUR,
    эквивалент отличной валюты более 5 000 USD, сверяя по дате операции и курсу этой валюты на дату.
    :param data: Список всех операций, который возвращается функцией save_rows_to_list()
    :param foreign_amount: Максимальная сумма в иностранной валюте, которую нужно проверить
    :param rub_amount: Максимальная сумма в рублях, которую нужно проверить
    :param filename: Имя файла
    :return: Список операций превышающих суммы, переданные в качестве аргументов
    """
    frod_positions = []

    with open(filename) as f:
        currency_rates_list = json.load(f)

    for row in data:
        if not row[7] or not row[6] or not row[8]:  # Проверка наличия валюты, суммы и даты
            continue

        amount = row[6]
        currency = row[7]
        date = row[8]

        if currency == 'USD' and amount >= foreign_amount:
            frod_positions.append(row)
        elif currency == 'EUR' and amount >= foreign_amount:
            frod_positions.append(row)
        elif currency == 'RUB' and amount >= rub_amount:
            frod_positions.append(row)
        elif currency not in {'USD', 'RUB', 'EUR'}:
            for rates_entry in currency_rates_list:
                if rates_entry["base"] == currency:
                    rate_on_date = rates_entry["rates"].get(date, {}).get("USD")
                    if rate_on_date:
                        amount_in_usd = amount * rate_on_date
                        if amount_in_usd >= foreign_amount:
                            frod_positions.append(row)
                    break
        else:
            continue

    return frod_positions
