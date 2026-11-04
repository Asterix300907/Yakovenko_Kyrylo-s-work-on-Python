"""Декоратори для валідації даних."""

import inspect
import re
from functools import wraps

from exceptions import InvalidEmailError, InvalidISBNError


def _get_argument(func, args, kwargs, name):
    """Отримує аргумент функції незалежно від способу його передачі."""
    bound = inspect.signature(func).bind_partial(*args, **kwargs)
    return bound.arguments.get(name)


def validate_isbn(func):
    """Перевіряє ISBN-13."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        isbn = _get_argument(func, args, kwargs, "isbn")

        if isbn is None:
            raise InvalidISBNError("ISBN не вказано")

        isbn = str(isbn)

        if not re.fullmatch(r"\d{13}", isbn):
            raise InvalidISBNError(f"Некоректний ISBN-13: {isbn}")

        return func(*args, **kwargs)

    return wrapper


def validate_email(func):
    """Перевіряє формат email."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        email = _get_argument(func, args, kwargs, "email")

        if email is None:
            raise InvalidEmailError("Email не вказано")

        email = str(email)

        if not re.fullmatch(r"[\w.-]+@[\w.-]+\.\w+", email):
            raise InvalidEmailError(f"Некоректний email: {email}")

        return func(*args, **kwargs)

    return wrapper


def validate_positive(func):
    """Перевіряє, що числові аргументи додатні."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = inspect.signature(func).bind_partial(*args, **kwargs)

        for name, value in bound.arguments.items():
            if name == "self":
                continue

            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(
                    f"Аргумент '{name}' має бути додатним: {value}"
                )

        return func(*args, **kwargs)

    return wrapper