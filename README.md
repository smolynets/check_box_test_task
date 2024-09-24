# Тестове завдання - Python Backend Developer

## Task Description:
Розробити REST API для створення та перегляду чеків з реєстрацією та авторизацією користувачів.

#### Пеймент ендпоінти:
1. POST - /payments/checks/ - ендпоінт для створення чеку
    #### Приклад тіла запиту
    {
    "pay_type": "cash",
    "amount": 1,
    "products": [
        {
        "name": "string",
        "price_per_unit": 1,
        "quantity": 1,
        "weight": 1
        }
    ],
    "additional_data": {}
    }
Потрібно відправляти або quantity або weight тільки.

2. GET - /payments/checks - список чеків користувача
Приклад юрли зі всіма фільтрами та пагінацією
"/payments/checks?pay_type=cash&start_date=2024-09-24&end_date=2024-09-25&min_total=1&max_total=5&page=1&page_size=10"

3. GET - /payments/checks/{id} - отримання чеку по id

4. GET - /payments/customer-checks/{receipt_link} - отримання відформатованого чеку в текстовому документі

#### OpenAPI/Swagger Specification:
Свагер ендпоінт - /docs


#### Запуск проекту:

##### Створіть .env file:
	cp sample_env .env

##### Для запуску докер контейнерів виконайте:
	docker-compose up --build

##### Сайт буде доступний за наступним посиланням:
	http://0.0.0.0:8000

##### Для запуску всіх тестів:
	docker exec -t backend python -m pytest

##### Для запуску тесту:
	docker exec -t backend python -m pytest -k test_name
