"""Семафори та Event для управління конкурентним доступом."""

import threading
import time
import random


class ConnectionPool:
    """Пул з'єднань з обмеженням через Semaphore."""

    def __init__(self, max_connections: int = 3):
        self._semaphore = threading.Semaphore(max_connections)
        self._lock = threading.Lock()
        self.max_connections = max_connections
        self.active_connections = 0
        self.total_served = 0
        self.peak_connections = 0

    def acquire_connection(self, client_name: str) -> None:
        """Отримання з'єднання (блокується, якщо пул вичерпано)."""
        print(f"[{client_name}] Запит на з'єднання...")
        # Семафор блокує, якщо вже max_connections активних
        self._semaphore.acquire()
        
        with self._lock:
            self.active_connections += 1
            if self.active_connections > self.peak_connections:
                self.peak_connections = self.active_connections
            print(f"  [{client_name}] З'єднання отримано "
                  f"(активних: {self.active_connections}/{self.max_connections})")

    def release_connection(self, client_name: str) -> None:
        """Повернення з'єднання до пулу."""
        with self._lock:
            self.active_connections -= 1
            self.total_served += 1
            print(f"  [{client_name}] З'єднання повернуто "
                  f"(залишилось активних: {self.active_connections})")
        # Звільняємо семафор — інший потік зможе отримати з'єднання
        self._semaphore.release()

    def get_stats(self) -> dict:
        """Повертає статистику використання пулу."""
        return {
            "max": self.max_connections,
            "active": self.active_connections,
            "total_served": self.total_served,
            "peak": self.peak_connections,
        }


def client_task(pool: ConnectionPool, client_name: str,
                ready_event: threading.Event) -> None:
    """Клієнт, що чекає сигналу готовності та використовує з'єднання."""
    ready_event.wait()  # чекаємо сигналу від "сервера"

    pool.acquire_connection(client_name)
    try:
        work_time = random.uniform(0.5, 2.0)
        print(f"  [{client_name}] Працює {work_time:.1f} сек "
              f"(активних: {pool.active_connections})")
        time.sleep(work_time)
    finally:
        pool.release_connection(client_name)


def main():
    pool = ConnectionPool(max_connections=3)
    ready_event = threading.Event()
    num_clients = 10

    # Створення та запуск 10 клієнтських потоків
    threads = []
    for i in range(num_clients):
        t = threading.Thread(
            target=client_task,
            args=(pool, f"Client-{i:02d}", ready_event),
        )
        threads.append(t)
        t.start()

    # Даємо всім потокам час стартувати, потім сигналізуємо готовність
    time.sleep(0.5)
    print(">>> Сервер готовий! Усі клієнти починають роботу.\n")
    ready_event.set()

    # Очікування завершення всіх потоків
    for t in threads:
        t.join()

    # Виведення статистики пулу
    stats = pool.get_stats()
    print(f"\n=== Статистика пулу ===")
    print(f"Макс. з'єднань: {stats['max']}")
    print(f"Обслуговано клієнтів: {stats['total_served']}")
    print(f"Пікове навантаження: {stats['peak']}")
    
    # Перевірка коректності обмеження
    if stats['peak'] <= stats['max']:
        print(f"✓ Обмеження дотримано: пік ({stats['peak']}) ≤ максимум ({stats['max']})")
    else:
        print(f"✗ ПОМИЛКА: пік ({stats['peak']}) перевищив максимум ({stats['max']})!")


if __name__ == "__main__":
    main()