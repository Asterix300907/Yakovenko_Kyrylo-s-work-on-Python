import itertools
from typing import Optional


def arithmetic_progression(start: float, step: float):
    current = start
    while True:
        yield current
        current += step


def geometric_progression(start: float, ratio: float, limit: float = float("inf")):
  
    current = start
    while current <= limit:
        yield current
        current *= ratio


def fibonacci(n: Optional[int] = None):
    """Генератор чисел Фібоначчі.
    
    Args:
        n: кількість чисел (None — нескінченна послідовність).
    """
    a, b = 0, 1
    count = 0
    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1


def collatz_sequence(n: int):
    """Генератор послідовності Коллатца (3n+1 задача)."""
    yield n
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        yield n


def flatten(nested):
    """Рекурсивний генератор для розгортання вкладених списків."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def main():
    # Арифметична прогресія: перші 10 елементів
    ap = arithmetic_progression(2, 3)
    first_10 = list(itertools.islice(ap, 10))
    print(f"Арифметична прогресія (2, 3): {first_10}")
 

    # Геометрична прогресія до 1000
    gp = list(geometric_progression(1, 2, limit=1000))
    print(f"Геометрична прогресія (1, 2): {gp}")
 

    # Фібоначчі: перші 15 чисел
    fib_15 = list(fibonacci(15))
    print(f"Фібоначчі (15): {fib_15}")

    # Послідовність Коллатца
    coll = list(collatz_sequence(27))
    print(f"Коллатц (27): довжина={len(coll)}, макс={max(coll)}")

    # Розгортання вкладених списків
    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    flat = list(flatten(nested))
    print(f"Розгортання: {flat}")


    # Знайти перше число Фібоначчі > 10000
    for fib_num in fibonacci(None):
        if fib_num > 10000:
            print(f"Перше число Фібоначчі > 10000: {fib_num}")
            break


if __name__ == "__main__":
    main()