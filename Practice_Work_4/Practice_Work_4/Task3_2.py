"""Producer-Consumer з queue.Queue та демонстрація дедлоку."""

import threading
import queue
import time
import random


class Task:
    """Завдання для обробки."""

    def __init__(self, task_id: int, data: str, priority: int = 0):
        self.task_id = task_id
        self.data = data
        self.priority = priority
        self.created_at = time.time()

    def __repr__(self):
        return f"Task(id={self.task_id}, data='{self.data}')"


def producer(task_queue: queue.Queue, num_tasks: int,
             producer_id: int) -> None:
    """Виробник: генерує завдання та поміщає їх у чергу."""
    for i in range(num_tasks):
        task = Task(
            task_id=producer_id * 100 + i,
            data=f"Дані від виробника {producer_id}, пакет {i}",
            priority=random.randint(1, 5),
        )
        task_queue.put(task)  # блокується, якщо черга повна (maxsize)
        print(f"  [Виробник-{producer_id}] Створено: {task}")
        time.sleep(random.uniform(0.1, 0.3))

    # Сигнал завершення для споживачів
    task_queue.put(None)


def consumer(task_queue: queue.Queue, consumer_id: int,
             results: list, results_lock: threading.Lock) -> None:
    """Споживач: обробляє завдання з черги."""
    while True:
        try:
            task = task_queue.get(timeout=2)
        except queue.Empty:
            print(f"  [Споживач-{consumer_id}] Черга порожня, завершення")
            break

        if task is None:
            # Передати сигнал завершення наступному споживачу
            task_queue.put(None)
            task_queue.task_done()
            break

        # Імітація обробки задачі
        work_time = random.uniform(0.2, 0.5)
        time.sleep(work_time)

        result = {
            "task_id": task.task_id,
            "consumer_id": consumer_id,
            "work_time": work_time,
            "processed_at": time.time(),
        }

        with results_lock:
            results.append(result)

        print(f"  [Споживач-{consumer_id}] Оброблено: {task} за {work_time:.2f}с")
        task_queue.task_done()


def producer_consumer_demo():
    """Демонстрація паттерну Producer-Consumer."""
    task_queue = queue.Queue(maxsize=5)  # обмеження розміру черги
    results = []
    results_lock = threading.Lock()
    num_producers = 2
    num_consumers = 3
    tasks_per_producer = 5

    print(f"Запуск: {num_producers} виробників, {num_consumers} споживачів")
    print(f"Завдань на виробника: {tasks_per_producer}\n")

    # Створення потоків виробників
    producer_threads = []
    for i in range(num_producers):
        t = threading.Thread(target=producer, args=(task_queue, tasks_per_producer, i))
        producer_threads.append(t)
        t.start()

    # Створення потоків споживачів
    consumer_threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer, args=(task_queue, i, results, results_lock))
        consumer_threads.append(t)
        t.start()

    # Очікування завершення виробників
    for t in producer_threads:
        t.join()

    # Очікування завершення споживачів
    for t in consumer_threads:
        t.join()

    # Виведення результатів
    print(f"\n=== Результати ===")
    print(f"Всього оброблено задач: {len(results)}")
    if results:
        avg_time = sum(r["work_time"] for r in results) / len(results)
        print(f"Середній час обробки: {avg_time:.3f} сек")
        print(f"Очікувано задач: {num_producers * tasks_per_producer}")


def deadlock_demo():
    """Демонстрація та виявлення потенційного дедлоку."""
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    deadlock_detected = threading.Event()

    def worker_1():
        """Захоплює lock_a, потім lock_b."""
        lock_a.acquire()
        print("[Worker-1] Захопив Lock A")
        time.sleep(0.1)
        acquired = lock_b.acquire(timeout=2)
        if not acquired:
            print("[Worker-1] ДЕДЛОК: не вдалося захопити Lock B!")
            deadlock_detected.set()
            lock_a.release()
            return
        print("[Worker-1] Захопив Lock B")
        lock_b.release()
        lock_a.release()

    def worker_2():
        """Захоплює lock_b, потім lock_a — зворотний порядок!"""
        lock_b.acquire()
        print("[Worker-2] Захопив Lock B")
        time.sleep(0.1)
        acquired = lock_a.acquire(timeout=2)
        if not acquired:
            print("[Worker-2] ДЕДЛОК: не вдалося захопити Lock A!")
            deadlock_detected.set()
            lock_b.release()
            return
        print("[Worker-2] Захопив Lock A")
        lock_a.release()
        lock_b.release()

    def safe_worker_1():
        """Безпечна версія: завжди захоплює A → B."""
        lock_a.acquire()
        print("[Safe-Worker-1] Захопив Lock A")
        time.sleep(0.1)
        lock_b.acquire()
        print("[Safe-Worker-1] Захопив Lock B")
        # Імітація роботи
        time.sleep(0.2)
        lock_b.release()
        lock_a.release()
        print("[Safe-Worker-1] Завершив роботу")

    def safe_worker_2():
        """Безпечна версія: той самий порядок A → B."""
        lock_a.acquire()
        print("[Safe-Worker-2] Захопив Lock A")
        time.sleep(0.1)
        lock_b.acquire()
        print("[Safe-Worker-2] Захопив Lock B")
        # Імітація роботи
        time.sleep(0.2)
        lock_b.release()
        lock_a.release()
        print("[Safe-Worker-2] Завершив роботу")

    # === Демонстрація дедлоку ===
    print("=== Спроба з потенційним дедлоком ===")
    t1 = threading.Thread(target=worker_1)
    t2 = threading.Thread(target=worker_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    if deadlock_detected.is_set():
        print(">>> Дедлок виявлено! Використовуємо timeout для запобігання зависанню.\n")
    else:
        print(">>> Дедлок не виник цього разу (залежить від планувальника).\n")

    # === Безпечна версія ===
    print("=== Безпечна версія (однаковий порядок замків) ===")
    t1 = threading.Thread(target=safe_worker_1)
    t2 = threading.Thread(target=safe_worker_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(">>> Безпечна версія завершилася без дедлоків!\n")


def main():
    print("=" * 60)
    print("=== Паттерн Producer-Consumer ===")
    print("=" * 60)
    producer_consumer_demo()

    print(f"\n{'=' * 60}")
    print("=== Демонстрація дедлоку ===")
    print("=" * 60)
    deadlock_demo()


if __name__ == "__main__":
    main()