# Описание проекта

Этот проект предназначен для анализа операций с целью выявления подозрительных транзакций, которые могут свидетельствовать о мошенничестве. Реализованы различные сценарии проверки, а также генерация итогового отчета с выявленными аномалиями. Код поддерживает интеграцию с API для получения данных о курсах валют, что позволяет анализировать операции с учетом валютных различий.

## Функциональность

- Проверка транзакций на наличие аномалий (повторяющиеся суммы, последовательности операций и т.д.).
- Генерация цепочек операций с флагами, указывающими на подозрительные транзакции.
- Выделение успешных транзакций среди подозрительных для дальнейшего анализа.
- Итоговый отчет с визуализацией данных.

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone [<URL-репозитория>](https://github.com/ko1216/antifrod_analyze)
cd antifrod_analyze
```

### 2. Установка зависимостей
Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями. Убедитесь, что Poetry установлен, затем выполните команду:
poetry install

### 3. Настройка окружения
Для работы с API необходимо создать файл `.env` в корне проекта и указать ваш API-ключ. Получить API-ключ можно по [этой ссылке](https://apilayer.com/marketplace/exchangerates_data-api?utm_source=apilayermarketplace&utm_medium=featured).

Пример содержимого `.env` файла:
```
EXCHANGE_RATE_API_KEY=ваш_api_ключ
```

### 4. Запуск анализа
Для запуска основного файла выполните:
```bash
poetry run python main.py
```

## Визуализация результатов
Итоговый отчет формируется в формате Excel и содержит все выявленные подозрительные операции. Для успешных транзакций среди подозрительных дополнительно подсвечивается их статус.

Также в отчете представлены графики, которые помогают визуально оценить распределение подозрительных операций и их успешность.

## Дополнительные сведения

Если у вас возникли вопросы или предложения по улучшению проекта, создайте issue в этом репозитории или свяжитесь с автором.