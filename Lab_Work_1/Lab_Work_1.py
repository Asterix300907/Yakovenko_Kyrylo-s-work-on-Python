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
