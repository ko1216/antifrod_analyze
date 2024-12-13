import pandas as pd
from src.funcs_by_pd import detect_recipient_changes, detect_login_region_change
from src.fraud_by_repeated_amount import detect_repeated_amounts
from src.fraud_by_amount import get_currencies_list, write_currencies_to_file, find_frod_by_amount
from src.functions import rows

input_file = 'Тестовое_задание_2_Антифрод_аналитик.xlsx'
data_df = pd.read_excel(input_file)
data_df = data_df.sort_values(by=['Customer ID', 'Operation created at Date'])


def write_to_excel(dataframes, sheet_names, output_file):
    """
    Записывает несколько DataFrame в один Excel-файл на разных листах.
    :param dataframes: Список DataFrame для записи.
    :param sheet_names: Список имен листов для каждого DataFrame.
    :param output_file: Имя выходного Excel-файла.
    """
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for df, sheet in zip(dataframes, sheet_names):
            df.to_excel(writer, sheet_name=sheet, index=False)


recipient_changes = detect_recipient_changes(data_df)
login_region_changes = detect_login_region_change(data_df)

repeated_fraud = detect_repeated_amounts(rows)
repeated_fraud_df = pd.DataFrame(repeated_fraud, columns=data_df.columns)

unique_currency = get_currencies_list(rows)
write_currencies_to_file(unique_currency)
foreign_amount = 5000
rub_amount = 500000
amount_fraud = find_frod_by_amount(rows, foreign_amount, rub_amount)
amount_fraud_df = pd.DataFrame(amount_fraud, columns=data_df.columns)

output_file = "fraud_analysis_results.xlsx"
dataframes = [
    recipient_changes,
    login_region_changes,
    repeated_fraud_df,
    amount_fraud_df
]
sheet_names = [
    "Смена реквизитов",
    "Смена региона входа и кардхолдера",
    "Больше 2 повторяющихся сумм",
    "Фрод по сумме вывода"
]
write_to_excel(dataframes, sheet_names, output_file)

print(f"Результаты анализа записаны в файл {output_file}.")
