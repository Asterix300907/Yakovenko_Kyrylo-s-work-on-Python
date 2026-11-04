"""Власні класи виключень для системи бібліотеки."""


class LibraryError(Exception):
    """Базове виключення системи."""
    pass


class InvalidISBNError(LibraryError):
    """Некоректний ISBN."""
    pass


class InvalidEmailError(LibraryError):
    """Некоректна електронна пошта."""
    pass


class BookNotFoundError(LibraryError):
    """Книгу не знайдено."""
    pass


class BookAlreadyExistsError(LibraryError):
    """Книга вже є в базі."""
    pass


class ReaderLimitError(LibraryError):
    """Перевищено ліміт книг для читача."""
    pass