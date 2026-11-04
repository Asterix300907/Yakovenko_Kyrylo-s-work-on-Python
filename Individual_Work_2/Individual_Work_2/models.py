"""Моделі даних."""

from decorators import validate_email, validate_isbn, validate_positive
from metaclasses import LoggingMeta


class Author(metaclass=LoggingMeta):
    def __init__(self, name: str, country: str = ""):
        if not name.strip():
            raise ValueError("Ім'я автора не може бути порожнім")

        self.name = name
        self.country = country

    def __repr__(self):
        return f"Author({self.name!r})"


class Book(metaclass=LoggingMeta):
    @validate_isbn
    def __init__(self, title: str, author: Author, isbn: str, year: int):
        if not title.strip():
            raise ValueError("Назва книги не може бути порожньою")

        if not isinstance(author, Author):
            raise TypeError("author має бути об'єктом Author")

        if year <= 0:
            raise ValueError("Рік має бути додатним")

        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_available = True

    def __repr__(self):
        return f"Book({self.title!r}, {self.author.name!r})"


class Reader(metaclass=LoggingMeta):
    MAX_BOOKS = 5

    @validate_email
    def __init__(self, name: str, email: str, age: int = 18):
        if not name.strip():
            raise ValueError("Ім'я читача не може бути порожнім")

        if age <= 0:
            raise ValueError("Вік має бути додатним")

        self.name = name
        self.email = email
        self.age = age
        self.borrowed_books = []

    def borrow(self, book: Book) -> None:
        if len(self.borrowed_books) >= self.MAX_BOOKS:
            from exceptions import ReaderLimitError

            raise ReaderLimitError(
                f"{self.name} вже має {self.MAX_BOOKS} книг"
            )

        if not book.is_available:
            raise ValueError(f"Книга '{book.title}' вже взята")

        book.is_available = False
        self.borrowed_books.append(book)

    def return_book(self, book: Book) -> None:
        if book not in self.borrowed_books:
            raise ValueError(
                f"{self.name} не брав книгу '{book.title}'"
            )

        book.is_available = True
        self.borrowed_books.remove(book)

    def __repr__(self):
        return f"Reader({self.name!r}, email={self.email!r})"