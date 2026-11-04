"""Метаклас для логування створення об'єктів."""

import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("LibraryMeta")


class LoggingMeta(type):
    """Метаклас, що логує створення кожного екземпляра класу."""

    _instance_count = {}  # лічильник створених об'єктів по класах

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        cls._instance_count[cls.__name__] = cls._instance_count.get(cls.__name__, 0) + 1
        logger.info(
            "Створено об'єкт: %s #%d (%s)",
            cls.__name__,
            cls._instance_count[cls.__name__],
            instance,
        )
        return instance