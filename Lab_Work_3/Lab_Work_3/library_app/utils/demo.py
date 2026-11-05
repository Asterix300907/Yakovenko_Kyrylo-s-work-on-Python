"""Демонстрація роботи бібліотечного сервісу.

Модуль показує створення книг, обробку власних винятків,
завантаження даних із JSON-файлу та роботу з __all__.
"""
import json
import os

from library_app.core import (
    BusinessLogicError,
    LibraryError,
    LibraryService,
    ResourceNotFoundError,
    ValidationError,
)


def run_demo() -> None:
    """Демонструє роботу бібліотечного сервісу.

    Returns:
        Нічого не повертає.

    Raises:
        LibraryError: Може виникнути під час демонстрації обробки помилок.
    """
    service = LibraryService()

    print("\n1. ValidationError:")
    try:
        service.add_book("123", "Тестова книга", 2020)
    except ValidationError as error:
        print(f"  Перехоплено: {error}")
        print(f"  Поле: {error.field_name}")
        print(f"  Код: {error.error_code}")

    print("\n2. BusinessLogicError:")
    service.add_book("9780140449136", "Злочин і кара", 1866)

    try:
        service.add_book("9780140449136", "Дублікат", 2020)
    except BusinessLogicError as error:
        print(f"  Перехоплено: {error}")
        print(f"  Правило: {error.rule_name}")

    print("\n3. ResourceNotFoundError:")
    try:
        service.get_book("0000000000000")
    except ResourceNotFoundError as error:
        print(f"  Перехоплено: {error}")
        print(f"  ID ресурсу: {error.resource_id}")

    print("\n4. Перехоплення через базовий клас:")
    try:
        service.add_book("bad-isbn", "Тест", 2020)
    except LibraryError as error:
        print(f"  Тип: {type(error).__name__}")
        print(f"  Повідомлення: {error}")

    print("\n5. Ланцюжок виключень:")
    try:
        service.load_from_file("missing.json")
    except ResourceNotFoundError as error:
        print(f"  Доменне виключення: {error}")
        print(f"  __cause__: {error.__cause__}")
        print(f"  Тип причини: {type(error.__cause__).__name__}")

    print("\n6. Повторне піднесення через raise:")
    file_name = "demo.json"

    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "9780140449136": {
                        "title": "Дублікат",
                        "year": 1866,
                    }
                },
                file,
                ensure_ascii=False,
            )

        try:
            service.load_from_file(file_name)
        except BusinessLogicError as error:
            print(f"  Зовнішній обробник отримав: {error}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

    print("\n7. Перевірка __all__:")
    print("  __all__ обмежує публічні імена пакета core.")
    print("  Доступні імена:", LibraryService.__name__)