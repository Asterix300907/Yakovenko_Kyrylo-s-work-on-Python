"""Порівняння ThreadPoolExecutor та ProcessPoolExecutor."""

from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    as_completed,
)
import time
import math
import hashlib


def io_bound_task(url: str) -> dict:
    """Імітація I/O-bound задачі (завантаження сторінки)."""
    time.sleep(0.5)
    return {"url": url, "status": 200, "size": len(url) * 42}


def cpu_bound_task(n: int) -> dict:
    """CPU-bound задача: обчислення хеш-суми великого діапазону."""
    hasher = hashlib.sha256()
    for i in range(n):
        hasher.update(str(i).encode())
    return {"n": n, "hash": hasher.hexdigest()[:16]}


def risky_task(value: int) -> float:
    """Задача, що може згенерувати виключення."""
    if value == 0:
        raise ZeroDivisionError("Ділення на нуль!")
    if value < 0:
        raise ValueError(f"Від'ємне значення: {value}")
    return 1000.0 / value


def benchmark_io_bound():
    """Порівняння послідовного та ThreadPoolExecutor для I/O-bound."""
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]

    # Послідовне виконання
    start_seq = time.perf_counter()
    seq_results = [io_bound_task(url) for url in urls]
    seq_time = time.perf_counter() - start_seq

    # Паралельне виконання (ThreadPoolExecutor + map)
    start_par = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        par_results = list(executor.map(io_bound_task, urls))
    par_time = time.perf_counter() - start_par

    print(f"Кількість задач: {len(urls)}")
    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Паралельно (ThreadPoolExecutor): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


def benchmark_cpu_bound():
    """Порівняння послідовного та ProcessPoolExecutor для CPU-bound."""
    tasks = [500_000] * 8

    # Послідовне виконання
    start_seq = time.perf_counter()
    seq_results = [cpu_bound_task(n) for n in tasks]
    seq_time = time.perf_counter() - start_seq

    # Паралельне виконання (ProcessPoolExecutor + map)
    start_par = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        par_results = list(executor.map(cpu_bound_task, tasks))
    par_time = time.perf_counter() - start_par

    print(f"Кількість задач: {len(tasks)}")
    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Паралельно (ProcessPoolExecutor): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


def handle_exceptions():
    """Демонстрація обробки виключень у concurrent.futures."""
    values = [10, 5, 0, -3, 8, 2]

    print("Обробка результатів у міру їх готовності (as_completed):")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_task, v): v for v in values}

        for future in as_completed(futures):
            val = futures[future]
            try:
                result = future.result()
                print(f"  Значення {val:2d}: Успіх, результат = {result:.2f}")
            except Exception as e:
                # Перехоплюємо ВСІ винятки
                exc_type = type(e).__name__
                print(f"  Значення {val:2d}: {exc_type} ➔ {e}")

    print("\nУсі винятки оброблено, програма продовжує роботу.")


def main():
    print("=" * 60)
    print("=== I/O-bound: ThreadPoolExecutor ===")
    print("=" * 60)
    benchmark_io_bound()

    print(f"\n{'=' * 60}")
    print("=== CPU-bound: ProcessPoolExecutor ===")
    print("=" * 60)
    benchmark_cpu_bound()

    print(f"\n{'=' * 60}")
    print("=== Обробка виключень у пулах ===")
    print("=" * 60)
    handle_exceptions()


if __name__ == "__main__":
    main()