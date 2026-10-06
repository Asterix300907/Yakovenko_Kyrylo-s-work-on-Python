# ЗАВДАННЯ 1.1
#Обчислення математичних виразів.
"""
import math

def main():
    a = float(input("Введіть a: "))
    b = float(input("Введіть b: "))
    c = float(input("Введіть c: "))

    sum_squares = a**2 + b**2 + c**2
    average = (a + b + c) / 3
    discriminant = b**2 - 4 * a * c
    hypotenuse = math.sqrt(a**2 + b**2)
    is_triangle = (a + b > c) and (a + c > b) and (b + c > a)

    print(f"1. Сума квадратів: {sum_squares:.2f}")
    print(f"2. Середнє арифметичне: {average:.2f}")
    print(f"3. Дискримінант: {discriminant:.2f}")
    print(f"4. Гіпотенуза (a, b): {hypotenuse:.2f}")
    print(f"5. Чи утворюють трикутник: {is_triangle}")

if __name__ == "__main__":
    main()
    """

# ЗАВДАННЯ 1.2
#Конвертор типів та форматоване виведення.
"""
def main():
    raw_input = input("Введіть число: ")
    
    try:
        val_int = int(raw_input)
        val_float = float(raw_input)
        print(f"int: {val_int} (тип: {type(val_int)})")
        print(f"float: {val_float} (тип: {type(val_float)})")
        print(f"Перевірка isinstance: {isinstance(val_float, float)}")
    except ValueError:
        print("Введене значення не є числом, перетворення в int/float неможливе.")
    
    val_bool = bool(raw_input)
    print(f"bool: {val_bool} (тип: {type(val_bool)})")

    name = input("Введіть ім'я: ")
    age = input("Введіть вік: ")
    print(f"Ім'я: {name} | Вік: {age}")

    my_range = list(range(1, 10, 2))
    print(f"Список з range: {my_range}")
    print(f"Довжина списку: {len(my_range)}")
    print(f"ID об'єкта списку: {id(my_range)}")

if __name__ == "__main__":
    main()
    """

    # ЗАВДАННЯ 2.1
    #Класифікація оцінок за шкалою ЄКТС.
"""
def classify_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 82:
        return "B"
    elif score >= 74:
        return "C"
    elif score >= 64:
        return "D"
    elif score >= 60:
        return "E"
    elif score >= 35:
        return "FX"
    else:
        return "F"

def main():
    raw = input("Введіть оцінку (0-100): ")
    try:
        score = int(raw)
        if score < 0 or score > 100:
            print("Помилка: оцінка має бути від 0 до 100")
        else:
            grade = classify_grade(score)
            print(f"Оцінка {score} -> ЄКТС: {grade}")
            passed = grade not in ("FX", "F")
            print(f"Результат: {'Зараховано' if passed else 'Не зараховано'}")
    except ValueError:
        print("Помилка: введено не ціле число.")

if __name__ == "__main__":
    main()

 """
 #ЗАВДАННЯ 2.2
 # Визначення типу трикутника та обчислення площі.
"""
import math

def triangle_type(a: float, b: float, c: float) -> str:
    if not ((a + b > c) and (a + c > b) and (b + c > a)):
        return "не є трикутником"
    
    if a == b == c:
        return "рівносторонній"
    
    if (abs(a**2 + b**2 - c**2) < 1e-9 or 
        abs(a**2 + c**2 - b**2) < 1e-9 or 
        abs(b**2 + c**2 - a**2) < 1e-9):
        return "прямокутний"
    
    if a == b or a == c or b == c:
        return "рівнобедрений"
    
    return "різносторонній"

def triangle_area(a: float, b: float, c: float) -> float:
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))

def main():
    a = float(input("Сторона a: "))
    b = float(input("Сторона b: "))
    c = float(input("Сторона c: "))
    
    t_type = triangle_type(a, b, c)
    print(f"Тип трикутника: {t_type}")
    
    if t_type != "не є трикутником":
        area = triangle_area(a, b, c)
        print(f"Площа трикутника: {area:.2f}")

if __name__ == "__main__":
    main()
"""

#ЗАВДАННЯ 3.1
#Використання циклу for для обчислень.
"""
def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def harmonic_sum(n: int) -> float:
    total = 0.0
    for i in range(1, n + 1):
        total += 1 / i
    return total

def multiplication_table(n: int) -> None:
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print(f"{i * j:4}", end="")
        print()

def main():
    n = int(input("Введіть число n: "))
    print(f"{n}! = {factorial(n)}")
    print(f"Гармонічна сума H({n}) = {harmonic_sum(n):.6f}")
    print(f"\nТаблиця множення {n}x{n}:")
    multiplication_table(n)

if __name__ == "__main__":
    main()
"""
#ЗАВДАННЯ 3.2
#Інтерактивний калькулятор на основі циклу while.
def calculator():
    print("=== Калькулятор ===")
    print("Введіть вираз у форматі: число оператор число")
    print("Введіть 'quit' для виходу, 'history' для історії")
    
    history = []
    
    while True:
        user_input = input("\n> ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        if user_input.lower() == 'history':
            if not history:
                print("Історія порожня.")
            else:
                for entry in history:
                    print(entry)
            continue
            
        parts = user_input.split()
        if len(parts) != 3:
            print("Некоректний формат. Використовуйте: число оператор число")
            continue
            
        try:
            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])
        except ValueError:
            print("Помилка: перший та третій аргументи мають бути числами.")
            continue
            
        if op == '+': res = num1 + num2
        elif op == '-': res = num1 - num2
        elif op == '*': res = num1 * num2
        elif op == '/':
            if num2 == 0:
                print("Помилка: ділення на нуль!")
                continue
            res = num1 / num2
        elif op == '//':
            if num2 == 0:
                print("Помилка: ділення на нуль!")
                continue
            res = num1 // num2
        elif op == '%':
            if num2 == 0:
                print("Помилка: ділення на нуль!")
                continue
            res = num1 % num2
        elif op == '**': res = num1 ** num2
        else:
            print("Невідомий оператор.")
            continue
            
        result_str = f"{num1} {op} {num2} = {res}"
        print(result_str)
        history.append(result_str)

if __name__ == "__main__":
    calculator()
