"""Паттерни Observer, Strategy та архітектурний шаблон MVC."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, List


# --- Observer ---

class EventEmitter:
    """Базовий клас для підтримки системи подій (Observer)."""

    def __init__(self):
        self._listeners: dict[str, List[Callable]] = {}

    def on(self, event: str, callback: Callable) -> None:
        """Підписатися на подію."""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable) -> None:
        """Відписатися від події."""
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs) -> None:
        """Сповістити всіх слухачів про подію."""
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


# --- Strategy ---

class SortStrategy(ABC):
    """Абстрактна стратегія сортування завдань."""

    @abstractmethod
    def sort(self, tasks: List["Task"]) -> List["Task"]:
        pass


class SortByPriority(SortStrategy):
    """Сортування за пріоритетом (1 - найвищий, 5 - найнижчий)."""

    def sort(self, tasks: List["Task"]) -> List["Task"]:
        return sorted(tasks, key=lambda t: t.priority)


class SortByDeadline(SortStrategy):
    """Сортування за терміном виконання (найближчий першим)."""

    def sort(self, tasks: List["Task"]) -> List["Task"]:
        return sorted(tasks, key=lambda t: t.deadline)


class SortByCreationDate(SortStrategy):
    """Сортування за датою створення (найновіші першими)."""

    def sort(self, tasks: List["Task"]) -> List["Task"]:
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


# --- Model ---

@dataclass
class Task:
    title: str
    priority: int  # 1 (найвищий) – 5 (найнижчий)
    deadline: datetime
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class TaskModel(EventEmitter):
    """Model: дані та бізнес-логіка завдань."""

    def __init__(self):
        super().__init__()
        self._tasks: List[Task] = []

    def add_task(self, title: str, priority: int, deadline: datetime) -> None:
        task = Task(title=title, priority=priority, deadline=deadline)
        self._tasks.append(task)
        self.emit("task_added", task)

    def complete_task(self, index: int) -> None:
        task = self._tasks[index]
        task.completed = True
        self.emit("task_completed", task)

    def remove_task(self, index: int) -> None:
        task = self._tasks.pop(index)
        self.emit("task_removed", task)

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        if include_completed:
            return self._tasks[:]
        return [t for t in self._tasks if not t.completed]

    def get_statistics(self) -> dict:
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.completed)
        return {
            "total": total,
            "completed": completed,
            "active": total - completed
        }


# --- View ---

class TaskView:
    """View: відображення даних у консолі."""

    def show_tasks(self, tasks: List[Task], title: str = "Завдання") -> None:
        print(f"\n--- {title} ---")
        print(f"{'№':<2} | {'Назва':<20} | {'Пріоритет':<10} | {'Дедлайн':<16} | {'Статус'}")
        print("-" * 65)
        for i, task in enumerate(tasks):
            status = "[x]" if task.completed else "[ ]"
            deadline_str = task.deadline.strftime("%d.%m %H:%M")
            print(f"{i:<2} | {task.title:<20} | {task.priority:<10} | {deadline_str:<16} | {status}")
        print("-" * 65)

    def show_message(self, message: str) -> None:
        print(f"[INFO] {message}")

    def show_statistics(self, stats: dict) -> None:
        print(f"\n--- Статистика ---")
        print(f"Всього завдань: {stats['total']}")
        print(f"Виконано: {stats['completed']}")
        print(f"Активних: {stats['active']}")


# --- Controller ---

class TaskController:
    """Controller: координація Model та View з підтримкою Strategy."""

    def __init__(self, model: TaskModel, view: TaskView):
        self._model = model
        self._view = view
        self._sort_strategy: SortStrategy = SortByPriority()

        # Підписка на події моделі (Observer)
        self._model.on("task_added", lambda t: self._view.show_message(f"Додано завдання: '{t.title}'"))
        self._model.on("task_completed", lambda t: self._view.show_message(f"Виконано завдання: '{t.title}'"))
        self._model.on("task_removed", lambda t: self._view.show_message(f"Видалено завдання: '{t.title}'"))

    def set_sort_strategy(self, strategy: SortStrategy) -> None:
        """Змінити стратегію сортування (Strategy)."""
        self._sort_strategy = strategy

    def add_task(self, title: str, priority: int, deadline: datetime) -> None:
        self._model.add_task(title, priority, deadline)

    def complete_task(self, index: int) -> None:
        self._model.complete_task(index)

    def show_all(self) -> None:
        tasks = self._model.get_tasks()
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks)

    def show_active(self) -> None:
        tasks = self._model.get_tasks(include_completed=False)
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks, title="Активні завдання")

    def show_stats(self) -> None:
        self._view.show_statistics(self._model.get_statistics())


def main():
    now = datetime.now()
    
    model = TaskModel()
    view = TaskView()
    ctrl = TaskController(model, view)

    print("=== Додавання завдань ===")
    ctrl.add_task("Здати Лабораторну 3", 1, now + timedelta(days=1))
    ctrl.add_task("Купити продукти", 3, now + timedelta(hours=5))
    ctrl.add_task("Прочитати розділ книги", 4, now + timedelta(days=3))
    ctrl.add_task("Відповісти на email", 2, now + timedelta(hours=2))

    print("\n=== Завдання (сортування за пріоритетом за замовчуванням) ===")
    ctrl.show_all()

    print("\n=== Зміна стратегії сортування на SortByDeadline ===")
    ctrl.set_sort_strategy(SortByDeadline())
    ctrl.show_all()

    print("\n=== Виконання завдання (індекс 1: 'Купити продукти') ===")
    ctrl.complete_task(1)

    print("\n=== Тільки активні завдання ===")
    ctrl.show_active()

    print("\n=== Статистика ===")
    ctrl.show_stats()


if __name__ == "__main__":
    main()