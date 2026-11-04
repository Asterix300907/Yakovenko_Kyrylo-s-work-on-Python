"""
СР №1: Консольна програма — базові конструкції, структури даних,
ітератори та генератори.
Виконав: Яковенко Кирило, група БІКСб1-25-40
"""

import math
from typing import Iterator, Generator, Optional


# ============================================================
# ЧАСТИНА 1. Базові оператори та математичні обчислення
# ============================================================

def factorial(n: int) -> int:
    """Обчислення факторіала через цикл (ітеративно)."""
    if n < 0:
        raise ValueError("Факторіал визначений лише для невід'ємних чисел")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """Обчислення факторіала через рекурсію (для порівняння)."""
    if n < 0:
        raise ValueError("Факторіал визначений лише для невід'ємних чисел")
    return 1 if n <= 1 else n * factorial_recursive(n - 1)


# ============================================================
# ЧАСТИНА 2. Робота з геометричними фігурами (словник + кортежі)
# ============================================================

# Словник формул: ключ — назва фігури, значення — кортеж (параметри, функція площі)
SHAPES = {
    "Коло":      ("радіус",         lambda r: math.pi * r ** 2),
    "Квадрат":   ("сторона",        lambda a: a ** 2),
    "Прямокутник": ("довжина, ширина", lambda a, b: a * b),
    "Трикутник": ("основа, висота", lambda a, h: 0.5 * a * h),
    "Трапеція":  ("a, b, висота",   lambda a, b, h: 0.5 * (a + b) * h),
}


def calculate_shape_area() -> None:
    """Інтерактивне обчислення площі геометричної фігури."""
    print("\n=== Доступні фігури ===")
    for idx, name in enumerate(SHAPES.keys(), 1):
        print(f"  {idx}. {name}")

    choice = input("Оберіть номер фігури: ").strip()
    if not choice.isdigit() or int(choice) not in range(1, len(SHAPES) + 1):
        print(" Невірний вибір.")
        return

    name = list(SHAPES.keys())[int(choice) - 1]
    params_desc, area_func = SHAPES[name]
    print(f"Фігура: {name} (параметри: {params_desc})")

    try:
        values = [float(x) for x in input("Введіть параметри через пробіл: ").split()]
        area = area_func(*values)
        print(f" Площа {name.lower()} = {area:.4f}")
    except (ValueError, TypeError) as e:
        print(f" Помилка вводу: {e}")


# ============================================================
# ЧАСТИНА 3. Структури даних: список, кортеж, словник
# ============================================================

def demonstrate_data_structures() -> None:
    """Демонстрація роботи зі списками, кортежами та словниками."""
    print("\n=== Робота зі структурами даних ===")

    # СПИСОК — мутує, впорядкований
    students = ["Олена", "Іван", "Марія", "Петро", "Анна"]
    print(f"\n[Список] Студенти: {students}")
    students.append("Кирило")
    students.sort()
    print(f"  Після додавання та сортування: {students}")

    # КОРТЕЖ — незмінюваний, використовується як ключ словника
    grades = (95, 78, 92, 85, 88, 90)
    print(f"\n[Кортеж] Оцінки: {grades}")
    print(f"  Середнє: {sum(grades) / len(grades):.2f}")
    print(f"  Максимум: {max(grades)}, Мінімум: {min(grades)}")

    # СЛОВНИК — пари ключ-значення
    student_grades = dict(zip(students[:5], grades[:5]))
    print(f"\n[Словник] Студент → оцінка: {student_grades}")

    # Фільтрація через dict comprehension
    excellent = {k: v for k, v in student_grades.items() if v >= 90}
    print(f"  Відмінники (≥90): {excellent}")


# ============================================================
# ЧАСТИНА 4. Власний ітератор
# ============================================================

class PrimeIterator:
    """Ітератор, що генерує прості числа до заданої межі."""

    def __init__(self, limit: int):
        self._limit = limit
        self._current = 2  # перше просте число

    def __iter__(self) -> "PrimeIterator":
        return self

    def __next__(self) -> int:
        while self._current <= self._limit:
            candidate = self._current
            self._current += 1
            if self._is_prime(candidate):
                return candidate
        raise StopIteration

    @staticmethod
    def _is_prime(n: int) -> bool:
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


def demonstrate_iterator() -> None:
    """Демонстрація власного ітератора простих чисел."""
    print("\n=== Власний ітератор: прості числа до 50 ===")
    primes = PrimeIterator(50)
    prime_list = list(primes)
    print(f"  Прості числа: {prime_list}")
    print(f"  Кількість: {len(prime_list)}")
    print(f"  Сума: {sum(prime_list)}")


# ============================================================
# ЧАСТИНА 5. Генератори
# ============================================================

def fibonacci_generator(n: Optional[int] = None) -> Generator[int, None, None]:
    """Генератор чисел Фібоначчі (нескінченний, якщо n=None)."""
    a, b = 0, 1
    count = 0
    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1


def collatz_generator(start: int) -> Generator[int, None, None]:
    """Генератор послідовності Коллатца (3n+1)."""
    n = start
    yield n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        yield n


def demonstrate_generators() -> None:
    """Демонстрація генераторів."""
    print("\n=== Генератори ===")

    # Фібоначчі: перші 12 чисел
    fib = list(fibonacci_generator(12))
    print(f"  Фібоначчі (12): {fib}")

    # Перше число Фібоначчі > 1000 (ліниве обчислення)
    for f in fibonacci_generator():
        if f > 1000:
            print(f"  Перше Фібоначчі > 1000: {f}")
            break

    # Послідовність Коллатца для n=27
    coll = list(collatz_generator(27))
    print(f"  Коллатц(27): довжина={len(coll)}, максимум={max(coll)}")

    # Generator expression — сума квадратів парних чисел
    even_sq_sum = sum(x ** 2 for x in range(1, 51) if x % 2 == 0)
    print(f"  Сума квадратів парних (1..50): {even_sq_sum}")


# ============================================================
# ЧАСТИНА 6. Умовні конструкції та цикли (додатковий приклад)
# ============================================================

def number_analysis() -> None:
    """Аналіз числа: парність, простота, сума цифр, дільники."""
    print("\n=== Аналіз числа ===")
    try:
        n = int(input("Введіть ціле число: "))
    except ValueError:
        print(" Потрібно ціле число.")
        return

    # Умовні конструкції
    parity = "парне" if n % 2 == 0 else "непарне"
    sign = "додатне" if n > 0 else ("від'ємне" if n < 0 else "нуль")
    print(f"  Число {n}: {sign}, {parity}")

    # Цикл — сума цифр
    digit_sum = sum(int(d) for d in str(abs(n)))
    print(f"  Сума цифр: {digit_sum}")

    # Цикл — дільники
    divisors = [i for i in range(1, abs(n) + 1) if n % i == 0] if n != 0 else []
    print(f"  Дільники: {divisors}")

    # Перевірка на простоту
    is_prime = PrimeIterator._is_prime(abs(n))
    print(f"  Просте: {'так' if is_prime else 'ні'}")


# ============================================================
# ГОЛОВНЕ МЕНЮ
# ============================================================

MENU = {
    "1": ("Факторіал числа", lambda: _run_factorial()),
    "2": ("Площа геометричної фігури", calculate_shape_area),
    "3": ("Структури даних (список/кортеж/словник)", demonstrate_data_structures),
    "4": ("Ітератор простих чисел", demonstrate_iterator),
    "5": ("Генератори (Фібоначчі, Коллатц)", demonstrate_generators),
    "6": ("Аналіз числа", number_analysis),
    "0": ("Вихід", None),
}


def _run_factorial() -> None:
    """Допоміжна функція для запуску обчислення факторіала."""
    try:
        n = int(input("Введіть невід'ємне ціле число: "))
        print(f"  Ітеративно: {n}! = {factorial(n)}")
        print(f"  Рекурсивно: {n}! = {factorial_recursive(n)}")
    except ValueError as e:
        print(f"❌ {e}")


def main() -> None:
    """Головне меню програми."""
    print("=" * 60)
    print("  СР №1: Базові конструкції, структури даних,")
    print("         ітератори та генератори у Python")
    print("=" * 60)

    while True:
        print("\n--- Меню ---")
        for key, (desc, _) in MENU.items():
            print(f"  [{key}] {desc}")

        choice = input("\nВаш вибір: ").strip()
        if choice not in MENU:
            print("❌ Невірний вибір. Спробуйте ще раз.")
            continue
        if choice == "0":
            print("👋 До побачення!")
            break
        func = MENU[choice][1]
        if func:
            func()


if __name__ == "__main__":
    main()
