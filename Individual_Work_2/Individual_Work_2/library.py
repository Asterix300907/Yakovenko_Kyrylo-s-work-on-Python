"""Головний контролер бібліотеки."""

import logging
import threading

from exceptions import BookAlreadyExistsError, BookNotFoundError
from models import Book, Reader
from patterns import (
    AuthorSearch,
    EmailNotifier,
    SingletonMeta,
    Subject,
    TitleSearch,
    YearSearch,
)

logger = logging.getLogger("Library")


class LibraryManager(Subject, metaclass=SingletonMeta):
    """Потокобезпечний Singleton-менеджер бібліотеки."""

    def __init__(self):
        super().__init__()
        self._books = {}
        self._readers = {}
        self._lock = threading.RLock()

    def add_book(self, book: Book) -> None:
        with self._lock:
            if book.isbn in self._books:
                raise BookAlreadyExistsError(
                    f"Книга з ISBN {book.isbn} вже існує"
                )

            self._books[book.isbn] = book
            self.notify("Нова книга додана", book.title)

    def remove_book(self, isbn: str) -> None:
        with self._lock:
            if isbn not in self._books:
                raise BookNotFoundError(
                    f"Книга з ISBN {isbn} не знайдена"
                )

            self._books.pop(isbn)

    def find_books(self, query: str, strategy=None):
        strategy = strategy or TitleSearch()

        with self._lock:
            return [
                book
                for book in self._books.values()
                if strategy.matches(book, query)
            ]

    def register_reader(self, reader: Reader) -> None:
        with self._lock:
            if reader.email in self._readers:
                raise ValueError(
                    f"Читач з email {reader.email} вже зареєстрований"
                )

            self._readers[reader.email] = reader
            self.attach(EmailNotifier(reader.name))

    def borrow_book(self, reader_email: str, isbn: str) -> None:
        with self._lock:
            reader = self._readers.get(reader_email)
            book = self._books.get(isbn)

            if reader is None or book is None:
                raise BookNotFoundError("Читач або книга не знайдені")

            reader.borrow(book)
            self.notify("Книгу взято", f"{reader.name} → {book.title}")

    def return_book(self, reader_email: str, isbn: str) -> None:
        with self._lock:
            reader = self._readers.get(reader_email)
            book = self._books.get(isbn)

            if reader is None or book is None:
                raise BookNotFoundError("Читач або книга не знайдені")

            reader.return_book(book)
            self.notify("Книгу повернуто", f"{reader.name} ← {book.title}")

    def reset(self) -> None:
        with self._lock:
            self._books.clear()
            self._readers.clear()
            self._observers.clear()

    @property
    def stats(self) -> dict:
        with self._lock:
            return {
                "books_total": len(self._books),
                "books_available": sum(
                    book.is_available for book in self._books.values()
                ),
                "readers": len(self._readers),
            }