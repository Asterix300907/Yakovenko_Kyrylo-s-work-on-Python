"""Паттерни проектування: Singleton, Observer, Strategy."""

import threading
from abc import ABC, abstractmethod


# ---------- Singleton для LibraryManager ----------
class SingletonMeta(type):
    """Потокобезпечний метаклас-одинак."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# ---------- Observer: сповіщення читачів ----------
class Subject:
    """Суб'єкт, за яким спостерігають."""

    def __init__(self):
        self._observers: list["Observer"] = []

    def attach(self, observer: "Observer"):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: "Observer"):
        self._observers.remove(observer)

    def notify(self, event: str, data=None):
        for obs in self._observers:
            obs.update(event, data)


class Observer(ABC):
    """Абстрактний спостерігач."""

    @abstractmethod
    def update(self, event: str, data=None):
        pass


class EmailNotifier(Observer):
    """Сповіщення через 'email' (імітація)."""

    def __init__(self, reader_name: str):
        self.reader_name = reader_name

    def update(self, event: str, data=None):
        print(f"  📧 Сповіщення для {self.reader_name}: {event} — {data}")


# ---------- Strategy: різні стратегії пошуку ----------
class SearchStrategy(ABC):
    """Абстрактна стратегія пошуку."""

    @abstractmethod
    def matches(self, book, query: str) -> bool:
        pass


class TitleSearch(SearchStrategy):
    def matches(self, book, query: str) -> bool:
        return query.lower() in book.title.lower()


class AuthorSearch(SearchStrategy):
    def matches(self, book, query: str) -> bool:
        return query.lower() in book.author.name.lower()


class YearSearch(SearchStrategy):
    def matches(self, book, query: str) -> bool:
        try:
            return book.year == int(query)
        except ValueError:
            return False