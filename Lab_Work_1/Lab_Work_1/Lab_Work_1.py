#ЗАДАЧА 1
print("ЗАДАЧА 1")
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(f"Початковий список: {data}\n")

print(f"Елемент за додатним індексом [2]: {data[2]}")
print(f"Елемент за від'ємним індексом [-3]: {data[-3]}\n")

print(f"Зріз [1:5]: {data[1:5]}")
print(f"Зріз [:-2]: {data[:-2]}")
print(f"Зріз [::3]: {data[::3]}\n")

expected_len = len(data)

data.append(110)
print(f"Після append(110): {data}")
print(f"Довжина: {len(data)} (очікувалось {expected_len + 1})\n")

data.insert(0, 5)
print(f"Після insert(0, 5): {data}")
print(f"Довжина: {len(data)} (очікувалось {expected_len + 2})\n")

del data[-1]
print(f"Після del [-1]: {data}")
print(f"Довжина: {len(data)} (очікувалось {expected_len + 1})\n")

print(f"Фінальний список: {data}")




#ЗАДАЧА2
print("ЗАДАЧА 2")
products = [
    (1, "Ноутбук", 5, 25000.00),
    (2, "Мишка", 50, 350.50),
    (3, "Клавіатура", 30, 899.99),
]

student = ("Іванов", "ІПЗ-21", [85, 90, 78, 92])


def unpack_product(record):
    pid, name, qty, price = record
    return pid, name, qty, price


def total_inventory_value(items):
    return sum(qty * price for _, _, qty, price in items)


print("=== Розпакування одного запису ===")
pid, name, qty, price = unpack_product(products[0])
print(f"ID: {pid}, Назва: {name}, Кількість: {qty}, Ціна: {price}")

print(f"\n=== Загальна вартість складу ===")
total = total_inventory_value(products)
print(f"Сума: {total:.2f} грн")

print("\n=== Спроба змінити кортеж за індексом ===")
try:
    products[0][1] = "Телефон"
except TypeError as e:
    print(f"TypeError: {e}")

print("\n=== Мутабельне вкладення в кортеж ===")
print(f"Студент до зміни: {student}")
student[2].append(95)
student[2][0] = 88
print(f"Студент після зміни оцінок: {student}")


#ЗАДАЧА 3
print("ЗАДАЧА 3")
def read_input():
    lines = []
    print("Введіть текст (натисніть Enter двічі для завершення):")
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return " ".join(lines)

def normalize_and_tokenize(text):
    cleaned = "".join(ch for ch in text if ch.isalnum() or ch.isspace())
    return cleaned.lower().split()

def build_frequency_dict(words):
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def main():
    text = read_input()
    
    words = normalize_and_tokenize(text)
    freq = build_frequency_dict(words)
    
    print("\n--- За алфавітом (за ключем) ---")
    for k, v in sorted(freq.items()):
        print(f"{k}: {v}")
        
    print("\n--- За спаданням частоти ---")
    for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True):
        print(f"{k}: {v}")
        
    threshold = 2
    filtered = {k: v for k, v in freq.items() if v >= threshold}
    print(f"\n--- Слова з частотою >= {threshold} ---")
    for k, v in sorted(filtered.items()):
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()



#ЗАДАЧА 4
print("ЗАДАЧА 4")    
list_a = [10, 20, 20, 30, 40]
list_b = [30, 40, 40, 50, 60]
list_c = [10, 20]

set_a = set(list_a)
set_b = set(list_b)
set_c = set(list_c)

print(f"Унікальні A: {sorted(set_a)}")
print(f"Унікальні B: {sorted(set_b)}")
print(f"Унікальні C: {sorted(set_c)}\n")

print(f"Об'єднання (A | B): {sorted(set_a | set_b)}")
print(f"Перетин (A & B): {sorted(set_a & set_b)}")
print(f"Симетрична різниця (A ^ B): {sorted(set_a ^ set_b)}\n")

print(f"C <= A (підмножина): {set_c <= set_a}")
print(f"B <= A (підмножина): {set_b <= set_a}")

#ЗАДАЧА 5
print("ЗАДАЧА 5")
import time

def get_avg_time(func, *args, runs=5):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)

def search_in_list(data, target):
    return target in data

def search_in_set(data_set, target):
    return target in data_set

def search_in_dict(data_dict, target):
    return target in data_dict

def build_unique_list(data):
    unique = []
    for item in data:
        if item not in unique:
            unique.append(item)

def build_unique_set(data):
    unique = set()
    for item in data:
        unique.add(item)

sizes = [1000, 10000, 50000]
runs_count = 5

print(f"{'Розмір (n)':<10} | {'Пошук List (с)':<15} | {'Пошук Set (с)':<15} | {'Пошук Dict (с)':<15} | {'Унікальні List (с)':<18} | {'Унікальні Set (с)':<18}")
print("-" * 110)

for n in sizes:
    data_list = list(range(n))
    data_set = set(data_list)
    data_dict = {i: i for i in range(n)}
    target = n
    
    t_list_search = get_avg_time(search_in_list, data_list, target, runs=runs_count)
    t_set_search = get_avg_time(search_in_set, data_set, target, runs=runs_count)
    t_dict_search = get_avg_time(search_in_dict, data_dict, target, runs=runs_count)
    t_unique_list = get_avg_time(build_unique_list, data_list, runs=runs_count)
    t_unique_set = get_avg_time(build_unique_set, data_list, runs=runs_count)

    print(f"{n:<10} | {t_list_search:<15.6f} | {t_set_search:<15.6f} | {t_dict_search:<15.6f} | {t_unique_list:<18.6f} | {t_unique_set:<18.6f}")