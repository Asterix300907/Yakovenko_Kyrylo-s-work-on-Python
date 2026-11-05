"""
Лабораторна робота №3, Завдання 2.
Ієрархія доменних виключень, ланцюжки виключень, повторне піднесення.

Схема ієрархії:

Exception
└── LibraryError
    ├── ValidationError
    ├── ResourceNotFoundError
    └── BusinessLogicError
"""

import json
import os
from typing import Optional


class LibraryError(Exception):
    """Базове виключення бібліотечної системи."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ValidationError(LibraryError):
    """Помилка валідації даних."""

    def __init__(
        self,
        message: str,
        field_name: str,
        error_code: str = "VAL_001",
    ) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.error_code = error_code

    def __str__(self) -> str:
        return (
            f"[{self.error_code}] Поле '{self.field_name}': "
            f"{self.message}"
        )


class ResourceNotFoundError(LibraryError):
    """Помилка відсутності ресурсу."""

    def __init__(
        self,
        message: str,
        resource_id: str,
        resource_type: str = "Unknown",
    ) -> None:
        super().__init__(message)
        self.resource_id = resource_id
        self.resource_type = resource_type

    def __str__(self) -> str:
        return (
            f"{self.resource_type} '{self.resource_id}' не знайдено: "
            f"{self.message}"
        )


class BusinessLogicError(LibraryError):
    """Порушення бізнес-правила."""

    def __init__(
        self,
        message: str,
        rule_name: str,
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message)
        self.rule_name = rule_name
        self.details = details or {}

    def __str__(self) -> str:
        return f"Порушено правило '{self.rule_name}': {self.message}"


class LibraryService:
    """Сервіс керування книгами."""

    def __init__(self) -> None:
        self._books: dict[str, dict] = {}

    def add_book(self, isbn: str, title: str, year: int) -> None:
        """Додає книгу після перевірки вхідних даних."""

        if len(isbn) != 13 or not isbn.isdigit():
            raise ValidationError(
                "ISBN має містити 13 цифр",
                field_name="isbn",
                error_code="VAL_001",
            )

        if year < 1000 or year > 2100:
            raise ValidationError(
                "Рік має бути в діапазоні від 1000 до 2100",
                field_name="year",
                error_code="VAL_002",
            )

        if isbn in self._books:
            raise BusinessLogicError(
                "Книга з таким ISBN уже існує",
                rule_name="unique_isbn",
                details={"isbn": isbn},
            )

        self._books[isbn] = {
            "title": title,
            "year": year,
        }

    def get_book(self, isbn: str) -> dict:
        """Повертає книгу за ISBN."""

        if isbn not in self._books:
            raise ResourceNotFoundError(
                "Книга відсутня в каталозі",
                resource_id=isbn,
                resource_type="Book",
            )

        return self._books[isbn]

    def load_from_file(self, path: str) -> None:
        """Завантажує книги з JSON-файлу.

        FileNotFoundError і JSONDecodeError перетворюються
        на доменні виключення через raise ... from ...
        """

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as error:
            raise ResourceNotFoundError(
                f"Файл '{path}' не знайдено",
                resource_id=path,
                resource_type="File",
            ) from error
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"Файл '{path}' містить некоректний JSON",
                field_name="file_content",
                error_code="VAL_JSON",
            ) from error

        for isbn, info in data.items():
            try:
                self.add_book(
                    isbn,
                    info["title"],
                    info["year"],
                )
            except LibraryError as error:
                print(f"[ЛОГ] Помилка під час імпорту ISBN {isbn}: {error}")
                raise


def main() -> None:
    print("=" * 60)
    print("Завдання 2: Ієрархія власних виключень")
    print("=" * 60)

    service = LibraryService()

    print("\n1. ValidationError:")
    try:
        service.add_book("123", "Тестова книга", 2020)
    except ValidationError as error:
        print(f"Перехоплено: {error}")
        print(f"Поле: {error.field_name}")
        print(f"Код: {error.error_code}")

    print("\n2. BusinessLogicError:")
    service.add_book("9780140449136", "Злочин і кара", 1866)

    try:
        service.add_book("9780140449136", "Дублікат", 2020)
    except BusinessLogicError as error:
        print(f"Перехоплено: {error}")
        print(f"Назва правила: {error.rule_name}")
        print(f"Додаткові дані: {error.details}")

    print("\n3. ResourceNotFoundError:")
    try:
        service.get_book("0000000000000")
    except ResourceNotFoundError as error:
        print(f"Перехоплено: {error}")
        print(f"Тип ресурсу: {error.resource_type}")
        print(f"Ідентифікатор: {error.resource_id}")

    print("\n4. Перехоплення через базовий клас LibraryError:")
    try:
        service.add_book("bad-isbn", "Тест", 2020)
    except LibraryError as error:
        print(
            f"Перехоплено через LibraryError: "
            f"{type(error).__name__}: {error}"
        )

    print("\n5. Ланцюжок виключень:")
    try:
        service.load_from_file("missing.json")
    except ResourceNotFoundError as error:
        print(f"Доменне виключення: {error}")
        print(f"Оригінальна причина (__cause__): {error.__cause__}")
        print(
            f"Тип оригінальної причини: "
            f"{type(error.__cause__).__name__}"
        )

    print("\n6. Повторне піднесення через raise:")
    test_file = "test.json"

    try:
        with open(test_file, "w", encoding="utf-8") as file:
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
            service.load_from_file(test_file)
        except BusinessLogicError as error:
            print(f"Головний обробник отримав: {error}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

    print("\nРоботу завершено.")


if __name__ == "__main__":
    main()