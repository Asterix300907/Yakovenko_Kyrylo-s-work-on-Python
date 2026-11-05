# Практична робота №4: Потоки, процеси та паралельне виконання в Python
**Виконав:** Яковенко Кирило, група БІКСб-12-540  
**Дисципліна:** Програмування

## Опис
Реалізація шести завдань з теми паралельного та конкурентного виконання коду в Python: робота з модулями `threading` та `multiprocessing`, синхронізація через `Lock` і `Semaphore`, високорівневий API `concurrent.futures`, міжпотокова комунікація через `queue.Queue` та виявлення дедлоків.

## Зміст завдань
1. **Робота з модулем `threading` (Task1_1.py):** Створення потоків для I/O-bound задач (імітація завантаження файлів), демон-потік `MonitorThread` з `threading.Event` для координованої зупинки, порівняння паралельного та послідовного виконання.
2. **Робота з модулем `multiprocessing` (Task1_2.py):** Паралельне обчислення суми простих чисел через `multiprocessing.Pool` з `starmap()`. Підтвердження справжнього паралелізму через різні PID процесів.
3. **Race condition та `Lock` (Task2_1.py):** Демонстрація втрати даних у банківському рахунку без синхронізації та усунення проблеми через `threading.Lock` як контекстний менеджер.
4. **`Semaphore` та `Event` (Task2_2.py):** Пул з'єднань (`ConnectionPool`) з обмеженням через `Semaphore(3)`, координований старт клієнтів через `Event`, захист лічильників через `Lock`.
5. **`concurrent.futures` (Task3_1.py):** Порівняння `ThreadPoolExecutor` (I/O-bound) та `ProcessPoolExecutor` (CPU-bound), обробка виключень через `future.result()` та `as_completed()`.
6. **Черги та дедлоки (Task3_2.py):** Паттерн Producer-Consumer через `queue.Queue(maxsize=5)` з sentinel-значенням `None`, виявлення дедлоку через `lock.acquire(timeout=...)` та безпечна версія з однаковим порядком захоплення замків.

## Як запустити

На комп'ютері має бути встановлено **Python 3.9+**.  
Зовнішні бібліотеки не потрібні — використовується лише стандартна бібліотека (`threading`, `multiprocessing`, `queue`, `concurrent.futures`, `time`, `random`, `hashlib`, `math`, `os`).

Кожне завдання запускається окремо:

```bash
python Task1_1.py   # Завдання 1.1 — Потоки та MonitorThread
python Task1_2.py   # Завдання 1.2 — Multiprocessing та прості числа
python Task2_1.py   # Завдання 2.1 — Race condition та Lock
python Task2_2.py   # Завдання 2.2 — Semaphore та Event
python Task3_1.py   # Завдання 3.1 — ThreadPoolExecutor та ProcessPoolExecutor
python Task3_2.py   # Завдання 3.2 — Producer-Consumer та дедлоки

Practice_Work_4/
├── Practice_Work_4.py              # Головний файл проекту (Visual Studio)
├── Task1_1.py                      # Завдання 1.1 — Потоки та завантаження файлів
├── Task1_2.py                      # Завдання 1.2 — Multiprocessing та обчислення
├── Task2_1.py                      # Завдання 2.1 — Race condition та Lock
├── Task2_2.py                      # Завдання 2.2 — Semaphore та Event
├── Task3_1.py                      # Завдання 3.1 — concurrent.futures
├── Task3_2.py                      # Завдання 3.2 — Queue та дедлоки
├── ПР4_Яковенко_БІКСб1-25-40_Програмування.pdf  # Повний звіт
├── README.md                       # Ця інструкція
└── .gitignore                      # Налаштування для ігнорування тимчасових файлів

## Файли репозиторію
Файли репозиторію
Task1_1.py — потоки, демон-потік, порівняння паралельного/послідовного виконання
Task1_2.py — multiprocessing.Pool, обчислення простих чисел, PID процесів
Task2_1.py — race condition на банківському рахунку, Lock
Task2_2.py — ConnectionPool, Semaphore, Event, статистика пулу
Task3_1.py — ThreadPoolExecutor, ProcessPoolExecutor, обробка виключень
Task3_2.py — Producer-Consumer, queue.Queue, дедлоки
Practice_Work_4.py — головний файл проекту (Visual Studio)
ПР4_Яковенко_БІКСб1-25-40_Програмування.pdf — повний звіт з теоретичним обґрунтуванням, скріншотами результатів та висновками
`README.md` — ця інструкція.
`.gitignore` — налаштування для ігнорування тимчасових файлів.