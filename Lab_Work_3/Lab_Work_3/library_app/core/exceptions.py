"""Класи винятків бібліотечної системи.

Модуль містить базовий клас помилки та спеціалізовані винятки
для перевірки даних, пошуку ресурсів і бізнес-правил.
"""

from typing import Optional


class LibraryError(Exception):
    """Базове виключення бібліотечної системи."""

    def __init__(self, message: str) -> None:
        """Створює базове виключення бібліотеки.

        Args:
            message: Текст повідомлення про помилку.

        Returns:
            Нічого не повертає.

        Raises:
            Ніяких винятків додатково не підносить.
        """
        super().__init__(message)
        self.message = message


class ValidationError(LibraryError):
    """Помилка перевірки вхідних даних."""

    def __init__(
        self,
        message: str,
        field_name: str,
        error_code: str = "VAL_001",
    ) -> None:
        """Створює помилку перевірки даних.

        Args:
            message: Опис помилки.
            field_name: Назва поля з некоректним значенням.
            error_code: Код помилки.

        Returns:
            Нічого не повертає.

        Raises:
            Ніяких винятків додатково не підносить.
        """
        super().__init__(message)
        self.field_name = field_name
        self.error_code = error_code

    def __str__(self) -> str:
        """Формує текстове представлення помилки.

        Returns:
            Повідомлення з кодом і назвою некоректного поля.

        Raises:
            Ніяких винятків не підносить.
        """
        return (
            f"[{self.error_code}] Поле '{self.field_name}': "
            f"{self.message}"
        )


class ResourceNotFoundError(LibraryError):
    """Помилка відсутності необхідного ресурсу."""

    def __init__(
        self,
        message: str,
        resource_id: str,
        resource_type: str = "Unknown",
    ) -> None:
        """Створює помилку відсутнього ресурсу.

        Args:
            message: Опис помилки.
            resource_id: Ідентифікатор відсутнього ресурсу.
            resource_type: Тип відсутнього ресурсу.

        Returns:
            Нічого не повертає.

        Raises:
            Ніяких винятків додатково не підносить.
        """
        super().__init__(message)
        self.resource_id = resource_id
        self.resource_type = resource_type

    def __str__(self) -> str:
        """Формує текстове представлення помилки.

        Returns:
            Повідомлення про відсутній ресурс.

        Raises:
            Ніяких винятків не підносить.
        """
        return (
            f"{self.resource_type} '{self.resource_id}' не знайдено: "
            f"{self.message}"
        )


class BusinessLogicError(LibraryError):
    """Помилка порушення бізнес-правила."""

    def __init__(
        self,
        message: str,
        rule_name: str,
        details: Optional[dict] = None,
    ) -> None:
        """Створює помилку бізнес-логіки.

        Args:
            message: Опис порушення правила.
            rule_name: Назва порушеного правила.
            details: Додаткові відомості про помилку.

        Returns:
            Нічого не повертає.

        Raises:
            Ніяких винятків додатково не підносить.
        """
        super().__init__(message)
        self.rule_name = rule_name
        self.details = details or {}

    def __str__(self) -> str:
        """Формує текстове представлення помилки.

        Returns:
            Повідомлення про порушене бізнес-правило.

        Raises:
            Ніяких винятків не підносить.
        """
        return f"Порушено правило '{self.rule_name}': {self.message}"