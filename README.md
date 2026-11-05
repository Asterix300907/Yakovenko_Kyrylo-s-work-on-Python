# Практична робота №5: Ініціалізація та конфігурація веб-проектів з Django та Flask
**Виконав:** Яковенко Кирило, група БІКСб-12-540  
**Дисципліна:** Програмування

## Опис
Реалізація шести завдань з теми веб-розробки на Python: підготовка середовища, створення та конфігурація проектів на Django і Flask, автоматичний аналіз конфігурації та порівняння архітектур фреймворків.

## Зміст завдань

1. **Віртуальне середовище та pip (Task1_1.py):** Створення venv, встановлення Django та Flask, фіксація залежностей у `requirements.txt`, скрипт перевірки середовища.
2. **Відтворення середовища (Task1_2.py):** Генератор `requirements.txt` через `pip list --format=json`, перевірка відтворюваності в новому venv2.
3. **Django-проект (mysite/):** Ініціалізація проекту, створення додатка `pages`, маршрутизація (`/`, `/about/`, `/contact/`), обробка GET-параметрів.
4. **Аналіз settings.py (Task2_2.py):** Парсинг конфігурації Django через `ast`, перевірка безпеки (DEBUG, SECRET_KEY, ALLOWED_HOSTS).
5. **Flask-проект (myflaskapp/):** Паттерн Application Factory, класи конфігурації, маршрути (`/`, `/about`, `/api/info`, `/greet/<name>`), JSON-відповіді.
6. **Порівняння структур (Task3_2.py):** Автоматичне сканування Django та Flask проектів, деревоподібне відображення, порівняльна таблиця.

## Як запустити

На комп'ютері має бути встановлено **Python 3.10+**.  
Зовнішні бібліотеки: `django`, `flask` (встановлюються через `pip install -r requirements.txt`).

Кожне завдання запускається окремо:
```bash
Частина 1 — Підготовка середовища

python -m venv venv
venv\Scripts\activate
pip install django flask
pip freeze > requirements.txt
python Task1_1.py

Частина 2 — Django
python -m django startproject mysite
cd mysite
python manage.py startapp pages
python manage.py runserver
python Task2_2.py 

Частина 3 — Flask
cd myflaskapp
pip install -r requirements.txt
python app.py

Порівняльний аналіз
python Task3_2.py

Структура проекту
Practice_Work_5/
├── Task1_1.py                          # Завдання 1.1 — перевірка середовища
├── Task1_2.py                          # Завдання 1.2 — генератор requirements.txt
├── Task2_2.py                          # Завдання 2.2 — аналізатор settings.py
├── Task3_2.py                          # Завдання 3.2 — порівняння структур
├── requirements.txt                    # Залежності Django + Flask
├── mysite/                             # Django-проект
│   ├── manage.py
│   ├── mysite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── pages/                          # Додаток pages
│       ├── views.py
│       ├── urls.py
│       └── migrations/
├── myflaskapp/                         # Flask-проект
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── static/
│   │   └── style.css
│   └── templates/
├── ПР5_Яковенко_БІКСб-12-540_Програмування.pdf  # Повний звіт
├── README.md                           # Ця інструкція
└── .gitignore                          # Налаштування для ігнорування тимчасових файлів

## Файли репозиторію
Файли репозиторію
Task1_1.py — перевірка Python та встановлених пакетів (django, flask)
Task1_2.py — генератор та верифікатор requirements.txt через subprocess + JSON
Task2_2.py — аналіз settings.py через ast, перевірка безпеки
Task3_2.py — порівняння структур Django та Flask проектів
mysite/ — Django-проект з додатком pages (3 маршрути, обробка GET)
myflaskapp/ — Flask-проект з Application Factory (4 маршрути, JSON API)
requirements.txt — зафіксовані версії залежностей
ПР5_Яковенко_БІКСб-12-540_Програмування.pdf — повний звіт з теоретичним обґрунтуванням, скріншотами результатів та висновками
`README.md` — ця інструкція.
`.gitignore` — налаштування для ігнорування тимчасових файлів.