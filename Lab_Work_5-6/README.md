# Лабораторна робота №5-6: Розробка графічних інтерфейсів. Django та Flask

**Виконав:** Яковенко Кирило, група БІКСб-12-540  
**Дисципліна:** Програмування

## Опис

Реалізація семи завдань з теми веб-розробки на Python: підготовка проектів Django та Flask, шаблони та відображення контекстних даних, успадкування шаблонів та макет сторінок, проєктування форм із серверною валідацією у Django та Flask, CSRF-захист та безпека форм, порівняльний аналіз підходів до проєктування UI.

## Зміст завдань

1. **Підготовка проектів (django_project/ та flask_project/):** Створення ізольованих віртуальних середовищ, встановлення Django та Flask-WTF, ініціалізація проектів з однаковою предметною областю "Блог", реєстрація додатків, налаштування маршрутів для головної сторінки та сторінки "Про нас".

2. **Шаблони та контекстні дані:** Створення HTML-шаблонів у Django (DTL) та Flask (Jinja2) з передачею контекстних даних (рядкові змінні, числові значення, списки), використання конструкцій `{% for %}`, `{% if %}`, фільтрів (`truncatewords`, `length`, `default`, `upper`), демонстрація можливостей Jinja2 (арифметичні вирази, виклик методів).

3. **Успадкування шаблонів:** Створення базових шаблонів `base.html` з навігацією, підвалом та підключенням статичних файлів, похідні шаблони з перевизначенням блоків `title` та `content`, демонстрація автоматичного оновлення всіх сторінок при зміні базового шаблону.

4. **Форми у Django:** Клас `FeedbackForm` з чотирма полями різних типів (`CharField`, `EmailField`, `ChoiceField`, `TextAreaField`), кастомна валідація через методи `clean_name()` та `clean_message()`, обробка GET/POST, flash-повідомлення через `django.contrib.messages`, паттерн Post/Redirect/Get.

5. **Форми у Flask:** Клас `FeedbackForm` на основі `FlaskForm` з декларативними валідаторами (`DataRequired`, `Length`, `Email`), кастомна валідація через методи `validate_name()` та `validate_message()`, обробка через `validate_on_submit()`, flash-повідомлення та перенаправлення, макрос Jinja2 для уніфікованого рендерингу полів.

6. **CSRF-захист та безпека:** Перевірка наявності `{% csrf_token %}` у Django та `form.hidden_tag()` у Flask, емпірична перевірка за допомогою `curl` (спроба відправки POST-запиту без токена), опис механізмів захисту від XSS через автоматичне екранування в шаблонах.

7. **Порівняльний аналіз:** Порівняльна таблиця Django та Flask за аспектами (шаблонізатор, успадкування, форми, валідація, CSRF, flash-повідомлення, обсяг коду), практичні сценарії вибору фреймворку (швидкий прототип, корпоративний сервіс, мікросервіс), аналіз кількості файлів та шаблонного коду.

## Як запустити

### Django проект

На комп'ютері має бути встановлено **Python 3.10+**.

```bash
Django проект
cd django_project
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Відкрийте у браузері:
Головна: http://127.0.0.1:8000/
Статті: http://127.0.0.1:8000/posts/
Контакти: http://127.0.0.1:8000/contact/

Flask проект
У окремому терміналі:
cd flask_project
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install flask flask-wtf email-validator
pip install -r requirements.txt
python app.py

Відкрийте у браузері:
Головна: http://127.0.0.1:5000/
Статті: http://127.0.0.1:5000/posts
Контакти: http://127.0.0.1:5000/contact

Структура проекту
Lab_Work_5-6/
├── django_project/
│   ├── venv/
│   ├── blog/
│   │   ├── migrations/
│   │   │   ── __init__.py
│   │   ├── static/
│   │   │   ── blog/
│   │   │       └── style.css
│   │   ├── templates/
│   │   │   └── blog/
│   │   │       ├── base.html
│   │   │       ├── index.html
│   │   │       ├── posts.html
│   │   │       └── contact.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py              # Форма зворотного зв'язку
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py               # Маршрути додатка
│   │   └── views.py              # View-функції
│   ├── config/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py           # Налаштування проекту
│   │   ├── urls.py               # Головні маршрути
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
│
├── flask_project/
│   ├── venv/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── posts.html
│   │   └── contact.html
│   ├── app.py                    # Головний файл додатка
│   ├── config.py                 # Конфігурація Flask
│   └── requirements.txt
│
├── ЛР5-6_Яковенко_БІКСб-12-540.pdf  # Повний звіт
├── README.md                     # Ця інструкція
└── .gitignore                    # Налаштування для ігнорування тимчасових файлів

Файли репозиторію
Django проект:
blog/forms.py — клас FeedbackForm з кастомною валідацією
blog/views.py — view-функції index, posts, contact
blog/urls.py — маршрути додатка blog
blog/templates/blog/base.html — базовий шаблон з навігацією
blog/templates/blog/index.html — головна сторінка
blog/templates/blog/posts.html — список статей
blog/templates/blog/contact.html — форма зворотного зв'язку
blog/static/blog/style.css — стилі для Django блогу
config/settings.py — налаштування проекту (INSTALLED_APPS, middleware)
config/urls.py — головні маршрути з include('blog.urls')
manage.py — утиліта керування Django
requirements.txt — залежності Django

Flask проект:
app.py — головний файл з маршрутами, класом FeedbackForm та view-функціями
config.py — конфігурація з SECRET_KEY та шляхами до папок
templates/base.html — базовий шаблон з навігацією
templates/index.html — головна сторінка
templates/posts.html — список статей з макросом Jinja2
templates/contact.html — форма зворотного зв'язку
static/style.css — стилі для Flask блогу
requirements.txt — залежності Flask