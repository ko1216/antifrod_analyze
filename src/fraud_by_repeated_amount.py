import datetime
import pandas as pd


def find_unique_users(data: list) -> list:
    """
    Функция возвращает список всех уникальных пользователей из общей таблицы операций
    :param data: Список всех операций
    :return: Список уникальных пользователей
    """
    unique_users = set()

    for row in data:
        if row[13]:
            unique_users.add(row[13])

    return list(unique_users)


def detect_repeated_amounts(data: list) -> list:
    """
    Функция ищет и возвращает список повторяющихся сумм для пользователя по его id в таблице.
    Считает фродом все повторяющиеся операции (больше или 3) с разными payment_id, записывает с 1 операции
    в цепочке в эту же дату или в следующие с разницей в 1 день между операциями, если они повторяются каждый день.

    :param data: Список всех операций
    :return: Список повторяющихся операций.
    """
    repeated_amounts = []
    users_id = find_unique_users(data)

    for user_id in users_id:
        user_operations = []
        for row in data:
            if user_id == row[13] and row[6] and row[7] and row[8]:
                user_operations.append(row)

        # Словарь для отслеживания повторяющихся сумм
        repeated_tracker = {}
        processed_payment_ids = set()

        for idx, operation in enumerate(user_operations):
            operation_date = datetime.datetime.strptime(operation[8], '%Y-%m-%d').date()
            amount_currency_pair = (operation[6], operation[7])
            payment_id = operation[2]
            prev_operations = []

            if payment_id in processed_payment_ids:
                continue

            if amount_currency_pair in repeated_tracker:
                last_date = repeated_tracker[amount_currency_pair]
                if (operation_date - last_date).days <= 1:
                    for prev_operation in user_operations[:idx]:
                        prev_operation_date = datetime.datetime.strptime(prev_operation[8], '%Y-%m-%d').date()
                        prev_payment_id = prev_operation[2]

                        if prev_payment_id in processed_payment_ids:
                            continue

                        if (prev_operation[6], prev_operation[7]) == amount_currency_pair and (
                                (operation_date - prev_operation_date).days <= 1 or
                                prev_operation_date == operation_date
                        ) and prev_payment_id != payment_id and prev_payment_id not in repeated_amounts:
                                prev_operations.append(prev_operation)

                    if prev_operations:
                        repeated_amounts.append(prev_operations[0])
                        processed_payment_ids.add(prev_operations[0][2])

                    repeated_amounts.append(operation)
                    processed_payment_ids.add(payment_id)

                    repeated_tracker[amount_currency_pair] = operation_date
                else:
                    del repeated_tracker[amount_currency_pair]
            else:
                repeated_tracker[amount_currency_pair] = operation_date

            processed_payment_ids.add(payment_id)

    # Считаем, что всего 2 повторяющиеся операции не являются подозрительными
    filtered_repeated_amounts = []
    grouped_by_user = {}

    for operation in repeated_amounts:
        user_id = operation[13]
        amount_currency_pair = (operation[6], operation[7])

        key = (user_id, amount_currency_pair)
        if key not in grouped_by_user:
            grouped_by_user[key] = []
        grouped_by_user[key].append(operation)

    for operations in grouped_by_user.values():
        if len(operations) > 2:
            filtered_repeated_amounts.extend(operations)

    print(f"Длина filtered_repeated_amounts перед записью: {len(filtered_repeated_amounts)}")
    return filtered_repeated_amounts
