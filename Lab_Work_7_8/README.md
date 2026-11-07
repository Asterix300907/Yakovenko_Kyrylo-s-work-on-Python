# Лабораторна робота №7-8: ORM-запити, агрегація, оптимізація та тестування. Django та Flask

**Виконав:** Яковенко Кирило, група БІКСб-12-540  
**Дисципліна:** Програмування

## Опис

Реалізація семи завдань з теми роботи з ORM та тестування веб-додатків на Python: проектування моделей даних, ORM-запити (CRUD, агрегація, анотація, оптимізація), unit-тестування моделей, інтеграційне тестування HTTP-маршрутів, мок-тестування зовнішніх та внутрішніх залежностей, аналіз покриття коду.

## Зміст завдань

**Завдання 1-2. Проектування моделей даних:** Створення моделей `Author`, `Profile`, `Post`, `Comment`, `Tag` з повним набором зв'язків (OneToOne, OneToMany, ManyToMany) для обох фреймворків. Налаштування обмежень цілісності (`unique`, `nullable`, `CASCADE delete`).

**Завдання 3. CRUD-операції та складні вибірки:** Демонстрація повного циклу створення, читання, оновлення та видалення даних. Використання Q-об'єктів у Django (`|`, `&`, `~`) та аналогів `or_`/`not_` у Flask-SQLAlchemy. Ланцюжки фільтрації.

**Завдання 4. Агрегація, анотація та оптимізація:** Використання `aggregate()` та `annotate()` для обчислення статистики (кількість коментарів, статей на автора). Оптимізація запитів через `select_related`/`prefetch_related` (Django) та `joinedload` (Flask). Демонстрація проблеми N+1.

**Завдання 5. Unit-тестування моделей:** Налаштування PyTest з фікстурами (`conftest.py`). Реалізація тестів створення об'єктів, перевірки обмежень (`IntegrityError`), зв'язків (OneToOne, ManyToMany), каскадного видалення. Параметризований тест через `@pytest.mark.parametrize`.

**Завдання 6. Інтеграційне тестування HTTP-маршрутів:** Створення простих views та маршрутів для обох проектів. Тестування статус-кодів (200, 404), вмісту відповідей, поведінки з чернетками. Використання тестових клієнтів `client` (Django) та `app.test_client()` (Flask).

**Завдання 7. Мок-тестування та аналіз покриття:** Реалізація мок-тестів для ізоляції зовнішніх (`os.path.exists`) та внутрішніх (`datetime`, `timezone.now`) залежностей. Перевірка виклику моків через `assert_called_once_with`. Генерація звіту `coverage` з аналізом прогалин.

## Як запустити

### Django проект

На комп'ютері має бути встановлено Python 3.10+.

```bash
cd django_project
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install django pytest pytest-django pytest-cov
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Відкрийте у браузері:
Головна: http://127.0.0.1:8000/
Статті: http://127.0.0.1:8000/blog/posts/
Детальна стаття: http://127.0.0.1:8000/blog/posts/test-post/

Запуск тестів:
pytest tests/ -v                              # Unit-тести моделей
pytest tests/test_views.py -v                 # Інтеграційні тести маршрутів
pytest tests/test_mocks.py -v                 # Мок-тести
pytest tests/ --cov=blog --cov-report=term-missing  # З покриттям

Flask проект
У окремому терміналі:
cd flask_project
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install flask flask-sqlalchemy flask-migrate pytest pytest-cov
pip install -r requirements.txt
python app.py

Відкрийте у браузері:
Головна: http://127.0.0.1:5000/
API статей: http://127.0.0.1:5000/api/posts

Запуск тестів:
pytest tests/test_models.py -v                # Unit-тести моделей
pytest tests/test_views.py -v                 # Інтеграційні тести маршрутів
pytest tests/test_mocks.py -v                 # Мок-тести
pytest tests/ --cov=app --cov=models --cov-report=term-missing  # З покриттям

Структура проекту
Lab_Work_7-8/
├── django_project/
│   ├── venv/
│   ├── blog/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── blog/
│   │   │       ├── base.html
│   │   │       ├── post_list.html
│   │   │       └── post_detail.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py              # Моделі Author, Profile, Post, Comment, Tag
│   │   ├── views.py               # View-функції post_list, post_detail
│   │   ├── urls.py                # Маршрути додатка
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py        # Фікстури
│   │       ├── test_models.py     # Unit-тести моделей
│   │       ├── test_views.py      # Інтеграційні тести
│   │       └── test_mocks.py      # Мок-тести
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── urls.py
│   ├── manage.py
│   ├── pytest.ini                 # Конфігурація PyTest
│   └── requirements.txt
│
├── flask_project/
│   ├── venv/
│   ├── migrations/                # Alembic міграції
│   ├── templates/
│   │   └── base.html
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py            # Фікстури (app, client, author, post...)
│   │   ├── test_models.py         # Unit-тести моделей
│   │   ├── test_views.py          # Інтеграційні тести
│   │   └── test_mocks.py          # Мок-тести
│   ├── app.py                     # Головний файл додатка
│   ├── models.py                  # Моделі Author, Profile, Post, Comment, Tag
│   ├── pytest.ini                 # Конфігурація PyTest
│   └── requirements.txt
│
├── ЛР7-8_Яковенко_БІКСб-12-540.pdf  # Повний звіт
├── README.md                      # Ця інструкція
└── .gitignore

Ключові файли репозиторію
Django проект:
blog/models.py — моделі даних зі зв'язками та обмеженнями
blog/views.py — view-функції для маршрутів
blog/urls.py — маршрути додатка blog
blog/templates/blog/ — HTML-шаблони
config/settings.py — налаштування проекту
pytest.ini — конфігурація PyTest (DJANGO_SETTINGS_MODULE)
blog/tests/test_models.py — 16 unit-тестів моделей
blog/tests/test_views.py — 4 інтеграційних тести маршрутів
blog/tests/test_mocks.py — 2 мок-тести
Flask проект:
models.py — моделі даних з явним визначенням проміжної таблиці ManyToMany
app.py — головний файл з маршрутами (/, /api/posts)
tests/conftest.py — фікстури для тестування
tests/test_models.py — 6 unit-тестів моделей
tests/test_views.py — 4 інтеграційних тести маршрутів
tests/test_mocks.py — 2 мок-тести
pytest.ini — конфігурація PyTest (відключення pytest-django)