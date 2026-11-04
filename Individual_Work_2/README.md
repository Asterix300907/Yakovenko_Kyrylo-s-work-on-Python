# Самостійна робота №2: Об'єктно-орієнтована система управління бібліотекою
**Виконав:** Яковенко Кирило, група БІКСб1-25-40д
**Дисципліна:** Програмування

## Опис
Розробка об'єктно-орієнтованої системи управління базою даних книг у бібліотеці з використанням метакласів для логування створення об'єктів, декораторів для валідації даних, паттернів проектування (Singleton, Observer, Strategy), обробки виключень та мультипоточності.

## Зміст завдань
1. **Модульна структура проекту:** розділення коду на модулі за відповідальністю (exceptions, metaclasses, decorators, models, patterns, library, main).
2. **Власні класи виключень:** ієрархія виключень (LibraryError, InvalidISBNError, InvalidEmailError, BookNotFoundError, BookAlreadyExistsError, ReaderLimitError) для обробки некоректного вводу та помилок бізнес-логіки.
3. **Метакласи:** LoggingMeta для автоматичного логування створення об'єктів з лічильником екземплярів, SingletonMeta з потокобезпечною реалізацією паттерну Singleton через threading.Lock.
4. **Декоратори валідації:** @validate_isbn (перевірка ISBN-13), @validate_email (перевірка формату email), @validate_positive (перевірка додатних чисел) з використанням inspect.signature для універсальності.
5. **Моделі даних:** класи Author, Book, Reader з валідацією через декоратори, методами borrow/return_book для управління позиками книг.
6. **Паттерни проектування:** Singleton (LibraryManager), Observer (сповіщення читачів через EmailNotifier), Strategy (TitleSearch, AuthorSearch, YearSearch для пошуку книг).
7. **Мультипоточність:** демонстрація потокобезпечної роботи системи через ThreadPoolExecutor з одночасним виконанням операцій взяття/повернення книг.

## Як запустити
1. На комп'ютері має бути встановлено Python 3.9+
2. Зовнішні бібліотеки не потрібні (використовується лише стандартна бібліотека: re, inspect, functools, logging, threading, concurrent.futures).
3. Запустіть основний файл командою: `python Individual_Work_2.py`.

## Файли репозиторію
- exceptions.py — ієрархія власних виключень
- metaclasses.py — LoggingMeta та SingletonMeta
- decorators.py — декоратори валідації (@validate_isbn, @validate_email, @validate_positive)
- models.py — класи Author, Book, Reader
- patterns.py — паттерни Singleton, Observer, Strategy
- library.py — LibraryManager (головний контролер)
- Individual_Work_2.py — точка входу з демонстрацією функціональності
- СР2_Яковенко_БІКСб1-25-40_Програмування.pdf — повний звіт з архітектурою, скріншотами результатів та висновками
- `README.md` — ця інструкція.
- `.gitignore` — налаштування для ігнорування тимчасових файлів.