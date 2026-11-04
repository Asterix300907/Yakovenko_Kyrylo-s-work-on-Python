"""Точка входу: демонстрація системи + мультипоточність."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from models import Author, Book, Reader
from library import LibraryManager
from patterns import AuthorSearch, YearSearch
from exceptions import LibraryError

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("Main")


def demo_basic():
    """Базова демонстрація: створення об'єктів, додавання, пошук."""
    print("\n=== 1. Базова демонстрація ===")
    lib = LibraryManager()

    author1 = Author("Федір Достоєвський", "Росія")
    author2 = Author("Лесь Українка", "Україна")

    lib.add_book(Book("Злочин і кара", author1, "9780140449136", 1866))
    lib.add_book(Book("Лісова пісня", author2, "9789660357327", 1911))
    lib.add_book(Book("Брати Карамазови", author1, "9780374528379", 1880))

    reader = Reader("Кирило", "kyrylo@example.com", 20)
    lib.register_reader(reader)

    lib.borrow_book(reader.email, "9780140449136")

    print("\nПошук за автором 'Достоєвський':")
    for b in lib.find_books("Достоєвський", AuthorSearch()):
        print(" ", b)

    print("\nПошук за роком 1866:")
    for b in lib.find_books("1866", YearSearch()):
        print(" ", b)

    print("\nСтатистика:", lib.stats)


def worker_task(lib: LibraryManager, isbn: str, reader_email: str):
    """Завдання для потоку: взяти/повернути книгу."""
    try:
        lib.borrow_book(reader_email, isbn)
        time.sleep(0.1)  # імітація роботи
        lib.return_book(reader_email, isbn)
        return f" Успішно: {isbn}"
    except LibraryError as e:
        return f" Помилка: {e}"


def demo_multithreading():
    """Демонстрація мультипоточності."""
    print("\n=== 2. Мультипоточність ===")
    lib = LibraryManager()
    lib.reset()

    # Додаємо книги та читачів для тесту
    author = Author("Тестовий Автор", "UA")
    isbns = [
        "9780140449136",
        "9789660357327",
        "9780374528379",
        "9780306406157",
        "9780262033848",
    ]

    for i, isbn in enumerate(isbns):
        lib.add_book(Book(f"Книга {i}", author, isbn, 2020))

    reader = Reader("Тест", "test@example.com")
    lib.register_reader(reader)

    print("Виконання 5 потоків одночасно...")
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(worker_task, lib, isbn, reader.email): isbn
            for isbn in isbns
        }
        for future in as_completed(futures):
            print(" ", future.result())

    print("\nФінальна статистика:", lib.stats)


def demo_exceptions():
    """Демонстрація обробки виключень."""
    print("\n=== 3. Обробка виключень ===")
    
    from decorators import validate_email, validate_isbn
    from exceptions import InvalidEmailError, InvalidISBNError

    try:
        validate_isbn(lambda isbn: None)(isbn="123")
    except InvalidISBNError as error:
        print(f"  Перехоплено: {error}")

    try:
        validate_email(lambda email: None)(email="not-an-email")
    except InvalidEmailError as error:
        print(f"  Перехоплено: {error}")


def main():
    demo_basic()
    demo_exceptions()
    demo_multithreading()
    print("\n Роботу завершено.")


if __name__ == "__main__":
    main()
