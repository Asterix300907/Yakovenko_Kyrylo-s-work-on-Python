"""Паттерни Singleton та Factory Method."""

import json
from abc import ABC, abstractmethod
from datetime import datetime


class SingletonMeta(type):
    """Метаклас для реалізації патерну Singleton."""

    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        # Перевіряємо, чи існує вже екземпляр для цього класу
        if cls not in cls._instances:
            # Якщо ні — створюємо через super().__call__() та зберігаємо
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # Повертаємо збережений екземпляр
        return cls._instances[cls]


class LogFormatter(ABC):
    """Абстрактний базовий клас форматера логів."""

    @abstractmethod
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        """Форматувати повідомлення логу."""
        pass


class PlainFormatter(LogFormatter):
    """Простий текстовий формат: [РІВЕНЬ] ЧАС - Повідомлення"""

    def format(self, level: str, message: str, timestamp: datetime) -> str:
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{level}] {time_str} - {message}"


class JSONFormatter(LogFormatter):
    """JSON-формат: {"level": "...", "time": "...", "message": "..."}"""

    def format(self, level: str, message: str, timestamp: datetime) -> str:
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        log_dict = {
            "level": level,
            "time": time_str,
            "message": message
        }
        return json.dumps(log_dict, ensure_ascii=False)


class ColorFormatter(LogFormatter):
    """Кольоровий формат для терміналу (ANSI-коди)."""

    COLORS = {
        "DEBUG": "\033[90m",      # Сірий
        "INFO": "\033[92m",       # Зелений
        "WARNING": "\033[93m",    # Жовтий
        "ERROR": "\033[91m",      # Червоний
    }
    RESET = "\033[0m"

    def format(self, level: str, message: str, timestamp: datetime) -> str:
        color = self.COLORS.get(level, self.RESET)
        time_str = timestamp.strftime("%H:%M:%S")
        return f"{color}[{level}] {time_str} - {message}{self.RESET}"


class FormatterFactory:
    """Фабрика форматерів із підтримкою реєстрації нових типів."""

    _formatters: dict[str, type[LogFormatter]] = {
        "plain": PlainFormatter,
        "json": JSONFormatter,
        "color": ColorFormatter,
    }

    @classmethod
    def register(cls, name: str, formatter_cls: type[LogFormatter]):
        """Зареєструвати новий тип форматера."""
        cls._formatters[name] = formatter_cls

    @classmethod
    def create(cls, name: str) -> LogFormatter:
        """Створити форматер за іменем. Викинути ValueError, якщо невідомий."""
        if name not in cls._formatters:
            raise ValueError(f"Невідомий форматер '{name}'. Доступні: {cls.available()}")
        return cls._formatters[name]()

    @classmethod
    def available(cls) -> list[str]:
        """Повернути список доступних форматерів."""
        return list(cls._formatters.keys())


class Logger(metaclass=SingletonMeta):
    """Логер із підтримкою рівнів та змінних форматерів."""

    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def __init__(self, formatter_name: str = "plain", min_level: str = "DEBUG"):
        # Для Singleton важливо не перезаписувати історію при повторному виклику __init__
        if not hasattr(self, "_initialized"):
            self._log_history: list[str] = []
            self._initialized = True
        
        # Оновлюємо налаштування (це дозволяє змінити їх через другий "екземпляр")
        self._formatter = FormatterFactory.create(formatter_name)
        self._min_level = min_level

    def set_formatter(self, name: str):
        """Змінити форматер через FormatterFactory."""
        self._formatter = FormatterFactory.create(name)

    def log(self, level: str, message: str):
        """Перевірити рівень, форматувати та вивести повідомлення."""
        if self.LEVELS.get(level, -1) >= self.LEVELS.get(self._min_level, 0):
            timestamp = datetime.now()
            formatted_msg = self._formatter.format(level, message, timestamp)
            print(formatted_msg)
            self._log_history.append(formatted_msg)

    def debug(self, msg: str):
        self.log("DEBUG", msg)

    def info(self, msg: str):
        self.log("INFO", msg)

    def warning(self, msg: str):
        self.log("WARNING", msg)

    def error(self, msg: str):
        self.log("ERROR", msg)

    def get_history(self) -> list[str]:
        return self._log_history[:]


def main():
    print("=== 1. Доведення Singleton ===")
    logger1 = Logger("plain", "DEBUG")
    logger2 = Logger("json", "INFO")
    print(f"logger1 is logger2: {logger1 is logger2}")  # Має бути True
    print(f"Поточний мінімальний рівень (встановлений logger2): {logger1._min_level}\n")

    print("=== 2. Логування з різними рівнями ===")
    logger1.info("Система запущена")
    logger1.warning("Мало пам'яті")
    logger1.error("Помилка з'єднання")
    # DEBUG не виведеться, бо min_level зараз "INFO" (встановлено через logger2)

    print("\n=== 3. Зміна форматера ===")
    logger1.set_formatter("color")
    logger1.set_formatter("json")  # Змінюємо на JSON для демонстрації
    logger1.debug("Діагностика (не виведеться через рівень INFO)")
    logger1.info("Нове повідомлення в JSON")

    print("\n=== 4. Статистика ===")
    print(f"Доступні форматери: {FormatterFactory.available()}")
    print(f"Кількість записів в історії: {len(logger1.get_history())}")


if __name__ == "__main__":
    main()