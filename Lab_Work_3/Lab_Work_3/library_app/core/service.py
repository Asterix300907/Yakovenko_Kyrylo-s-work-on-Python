"""Сервіс для керування книгами в бібліотечному каталозі."""
import json

from .exceptions import (
    BusinessLogicError,
    LibraryError,
    ResourceNotFoundError,
    ValidationError,
)


class LibraryService:
    """Сервіс керування книгами."""

    def __init__(self) -> None:
        """Створює порожній каталог книг.

        Returns:
            Нічого не повертає.

        Raises:
            Ніяких винятків не підносить.
        """
        self._books: dict[str, dict] = {}

    def add_book(self, isbn: str, title: str, year: int) -> None:
        """Додає книгу до каталогу.

        Args:
            isbn: ISBN книги, що складається з 13 цифр.
            title: Назва книги.
            year: Рік видання книги.

        Returns:
            Нічого не повертає.

        Raises:
            ValidationError: Якщо ISBN або рік мають некоректне значення.
            BusinessLogicError: Якщо книга з таким ISBN уже існує.
        """
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
                "Книга з таким ISBN вже існує",
                rule_name="unique_isbn",
                details={"isbn": isbn},
            )

        self._books[isbn] = {
            "title": title,
            "year": year,
        }

    def get_book(self, isbn: str) -> dict:
        """Повертає книгу за її ISBN.

        Args:
            isbn: ISBN книги, яку потрібно знайти.

        Returns:
            Словник із назвою та роком видання книги.

        Raises:
            ResourceNotFoundError: Якщо книги з таким ISBN немає в каталозі.
        """
        if isbn not in self._books:
            raise ResourceNotFoundError(
                "Книга відсутня в каталозі",
                resource_id=isbn,
                resource_type="Book",
            )

        return self._books[isbn]

    def load_from_file(self, path: str) -> None:
        """Завантажує книги з JSON-файлу.

        Args:
            path: Шлях до JSON-файлу з даними книг.

        Returns:
            Нічого не повертає.

        Raises:
            ResourceNotFoundError: Якщо файл не знайдено.
            ValidationError: Якщо файл містить некоректний JSON.
            LibraryError: Якщо дані книги не пройшли перевірку.
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
                print(f"[ЛОГ] Помилка імпорту ISBN {isbn}: {error}")
                raise