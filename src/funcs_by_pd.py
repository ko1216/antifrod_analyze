import pandas as pd


def detect_recipient_changes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ищет смену реквизитов получателя после 3 и более операций с одним.
    Предварительно фильтрует дубликаты по Payment ID.

    :param df: Исходный DataFrame с транзакциями.
    :return: DataFrame с операциями, где сменился получатель.
    """
    df = df[df['Account Number'].notna()]
    df = df.drop_duplicates(subset=['Payment ID'], keep='first').copy()

    group_cols = ['Merchant ID', 'Project ID', 'Customer ID']
    df['Unique_Recipients'] = df.groupby(group_cols)['Account Number'].transform('nunique')
    df = df[df['Unique_Recipients'] > 3]

    df['Previous_Recipient'] = df.groupby(group_cols)['Account Number'].shift(1)
    df['Recipient_Change'] = (df['Account Number'] != df['Previous_Recipient']) & df['Previous_Recipient'].notna()

    recipient_change = df.groupby(group_cols).filter(
        lambda x: (x['Recipient_Change'].cumsum() > 3).any()
    )

    return recipient_change


def detect_login_region_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ищет смену региона входа и смену реквизитов получателя.
    Если владелец карты отсутствует или сменился, это считается фродом.
    Пропускает строки с Operation Type = 'commission'.

    :param df: Исходный DataFrame с транзакциями.
    :return: DataFrame с цепочками операций, включая те, которые являются фродом.
    """
    # Здесь оставляем возможность ячейке из столбца кард холдер быть пустой на случай использования карты без имени
    df = df[df[['Country By IP Name', 'Account Number']].notna().all(axis=1)]
    df = df.drop_duplicates(subset=['Payment ID'], keep='first').copy()
    df = df[df['Operation Type'] != 'commission']

    group_cols = ['Merchant ID', 'Project ID', 'Customer ID']
    df['Unique_Recipients'] = df.groupby(group_cols)['Account Number'].transform('nunique')
    df['Unique_Countries'] = df.groupby(group_cols)['Country By IP Name'].transform('nunique')

    df['Previous_Region'] = df.groupby(group_cols)['Country By IP Name'].shift(1)
    df['Previous_Account'] = df.groupby(group_cols)['Account Number'].shift(1)
    df['Previous_Card_Holder'] = df.groupby(group_cols)['Card Holder'].shift(1)

    df['Region_Change'] = (df['Country By IP Name'] != df['Previous_Region']) & df['Previous_Region'].notna()
    df['Recipient_Change'] = (
            (df['Account Number'] != df['Previous_Account']) &
            (
                (df['Card Holder'] != df['Previous_Card_Holder']) |
                (df['Card Holder'].isna() & df['Previous_Card_Holder'].notna()) |
                (df['Previous_Card_Holder'].isna() & df['Card Holder'].isna()) |
                (df['Previous_Card_Holder'].notna() & df['Card Holder'].isna())
            ) &
            df['Previous_Account'].notna()
    )

    df['Fraudulent'] = df['Region_Change'] & df['Recipient_Change']

    df = df[(df['Unique_Recipients'] > 1) & (df['Unique_Countries'] > 1)]

    fraud_users = df[df['Fraudulent']]['Customer ID'].unique()
    result = df[df['Customer ID'].isin(fraud_users)]

    result = result.drop(columns=[
        'Unique_Recipients', 'Unique_Countries', 'Previous_Region',
        'Previous_Account', 'Previous_Card_Holder', 'Region_Change', 'Recipient_Change'
    ])

    return result
