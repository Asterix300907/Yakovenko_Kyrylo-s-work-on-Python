# Самостійна робота №3: Онлайн-Книгарня

**Виконав:** Яковенко Кирило, група БІКСб-12-540  
**Дисципліна:** Програмування

## Опис

Веб-додаток для онлайн-замовлення книг з використанням Flask, Flask-SQLAlchemy та REST API.

## Функціональність

- Перегляд каталогу книг з фільтрацією за жанром
- Детальна інформація про книгу
- Кошик покупок (сесії Flask)
- Оформлення замовлення
- REST API для програмного доступу до даних
- Підтримка світлої/темної теми (cookies)

## Як запустити

```bash
# Встановити залежності
pip install -r requirements.txt

# Запустити додаток
python app.py

# Відкрити в браузері
http://127.0.0.1:5000

Тестування
# Запустити тести
pytest tests/ -v

# Звіт про покриття коду
pytest tests/ --cov=app --cov=models --cov-report=term-missing

Структура проекту
Individual_Work_3/
├── app.py              # Головний файл (маршрути, REST API)
├── models.py           # Моделі БД (Book, Order, OrderItem)
├── templates/          # HTML-шаблони
├── static/             # CSS-стилі
├── tests/              # PyTest тести
└── requirements.txt    # Залежності

Технології
Python 3.15
Flask
Flask-SQLAlchemy
Jinja2
PyTest