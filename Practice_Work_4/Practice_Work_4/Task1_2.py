"""Паралельне обчислення з multiprocessing."""

import multiprocessing
import time
import os


def is_prime(n: int) -> bool:
    """Перевірка числа на простоту."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def sum_primes_in_range(start: int, end: int) -> tuple[int, int, int]:
    """Обчислює суму та кількість простих чисел у діапазоні [start, end).

    Returns:
        Кортеж (сума простих, кількість простих, PID процесу).
    """
    pid = os.getpid()
    total_sum = 0
    count = 0
    
    for n in range(start, end):
        if is_prime(n):
            total_sum += n
            count += 1
            
    return total_sum, count, pid


def main():
    total_range = 1_000_000
    num_workers = 4

    # Розбити діапазон [2, total_range) на num_workers частин
    chunk_size = total_range // num_workers
    ranges = []
    for i in range(num_workers):
        start = i * chunk_size if i > 0 else 2
        end = (i + 1) * chunk_size
        ranges.append((start, end))

    # === Послідовне виконання ===
    start_time = time.perf_counter()
    
    seq_total_sum = 0
    seq_total_count = 0
    for start, end in ranges:
        s, c, _ = sum_primes_in_range(start, end)
        seq_total_sum += s
        seq_total_count += c
        
    seq_time = time.perf_counter() - start_time

    # === Паралельне виконання з multiprocessing.Pool ===
    start_time = time.perf_counter()
    
    par_total_sum = 0
    par_total_count = 0
    pids_used = set()
    
    # Використовуємо контекстний менеджер для автоматичного закриття пулу
    with multiprocessing.Pool(processes=num_workers) as pool:
        # starmap автоматично розпаковує кортежі (start, end) як аргументи
        results = pool.starmap(sum_primes_in_range, ranges)
        
    for s, c, pid in results:
        par_total_sum += s
        par_total_count += c
        pids_used.add(pid)
        
    par_time = time.perf_counter() - start_time

    # === Виведення результатів ===
    print(f"Загальна сума простих чисел: {seq_total_sum}")
    print(f"Кількість знайдених простих чисел: {seq_total_count}")
    print(f"Перевірка цілісності даних: {'OK' if seq_total_sum == par_total_sum else 'ПОМИЛКА'}\n")
    
    print(f"PID головного процесу: {os.getpid()}")
    print(f"PID робочих процесів: {list(pids_used)}")
    
    print(f"\nПослідовно: {seq_time:.3f} сек")
    print(f"Паралельно ({num_workers} процеси): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


if __name__ == "__main__":
    # Цей блок обов'язковий для коректної роботи multiprocessing у Windows
    main()