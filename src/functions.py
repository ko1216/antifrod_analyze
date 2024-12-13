import os
import openpyxl
import datetime

FILENAME = FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Тестовое_задание_2_Антифрод_аналитик.xlsx')


def save_rows_to_list(filename=FILENAME) -> list:
    """
    Функция читает данные из Excel файла и
    возвращает отсортированный по дате список из всех строк таблицы, кроме оглавления.
    :param filename: Имя файла
    :return: Список
    """
    rows = []

    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active

    for row in sheet.iter_rows(values_only=True):
        new_row = []
        if 'Provider ID' in row:
            continue
        new_row.append(None if row[0] == '#N/A' else int(row[0]))
        new_row.append(None if not (row[1]) else str(row[1]))
        new_row.append(None if not (row[2]) else str(row[2]))
        new_row.append(None if not (row[3]) else str(row[3]))
        new_row.append(None if not (row[4]) else str(row[4]))
        new_row.append(None if not (row[5]) else str(row[5]))
        new_row.append(None if not (row[6]) else float(row[6]))
        new_row.append(None if not (row[7]) else str(row[7]))
        new_row.append(None if not row[8] else datetime.date.strftime(row[8], '%Y-%m-%d'))
        new_row.append(None if not (row[9]) else str(row[9]))
        new_row.append(None if not (row[10]) else str(row[10]))
        new_row.append(None if not (row[1]) else int(row[11]))
        new_row.append(None if not (row[12]) else int(row[12]))
        new_row.append(None if not (row[13]) else str(row[13]))
        new_row.append(None if not (row[14]) else str(row[14]))
        new_row.append(None if not (row[15]) else str(row[15]))
        new_row.append(None if not (row[16]) else str(row[16]))
        new_row.append(None if not (row[17]) else str(row[17]))
        new_row.append(None if not (row[18]) else str(row[18]))
        new_row.append(None if not (row[19]) else str(row[19]))
        rows.append(new_row)

    rows_sorted_by_date = sorted(rows, key=lambda arr: datetime.datetime.strptime(arr[8], '%Y-%m-%d'))
    return rows_sorted_by_date


rows = save_rows_to_list()
