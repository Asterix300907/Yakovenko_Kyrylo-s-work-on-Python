#ЗАВДАННЯ 1
class Vehicle:
    def __init__(self, brand: str, year: int):
        self.brand = brand
        self.year = year

    def get_fuel_type(self) -> str:
        return "Невідомо"

    def __str__(self) -> str:
        return f"{self.brand} ({self.year})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(brand='{self.brand}', year={self.year})"


class Car(Vehicle):
    def __init__(self, brand: str, year: int, doors: int):
        super().__init__(brand, year)
        self.doors = doors

    def get_fuel_type(self) -> str:
        return "Бензин або Дизель"


class Truck(Vehicle):
    def __init__(self, brand: str, year: int, payload_capacity: float):
        super().__init__(brand, year)
        self.payload_capacity = payload_capacity

    def get_fuel_type(self) -> str:
        return "Зазвичай Дизель"


class Motorcycle(Vehicle):
    def __init__(self, brand: str, year: int, has_sidecar: bool):
        super().__init__(brand, year)
        self.has_sidecar = has_sidecar

    def get_fuel_type(self) -> str:
        return "Бензин"


# Демонстрація
vehicles = [
    Car("Toyota", 2020, 4),
    Truck("Volvo", 2018, 15000.0),
    Motorcycle("Harley-Davidson", 2021, False)
]

for v in vehicles:
    print(f"{v} -> Паливо: {v.get_fuel_type()}")

print(f"\nCar є підкласом Vehicle: {issubclass(Car, Vehicle)}")
print(f"Об'єкт Truck є екземпляром Vehicle: {isinstance(vehicles[1], Vehicle)}")

#ЗАВДАННЯ 2
class TemperatureSensor:
    def __init__(self, sensor_id: str, initial_temp: float):
        self.sensor_id = sensor_id
        self._calibration_offset = 0.5  # Захищений атрибут
        self.__current_temp = 0.0       # Приватний атрибут
        self.temperature = initial_temp # Виклик setter для валідації

    @property
    def temperature(self) -> float:
        return self.__current_temp + self._calibration_offset

    @temperature.setter
    def temperature(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Температура має бути числовим значенням.")
        if value < -50.0 or value > 150.0:
            raise ValueError("Температура поза діапазоном роботи датчика (-50..150).")
        self.__current_temp = value

    @property
    def temperature_in_fahrenheit(self) -> float:
        return self.temperature * 9/5 + 32

# Демонстрація
sensor = TemperatureSensor("S-101", 25.0)
print(f"Поточна температура: {sensor.temperature}°C")
print(f"В Фаренгейтах: {sensor.temperature_in_fahrenheit}°F")

sensor._calibration_offset = 1.0  # Зміна захищеного атрибута
print(f"Після зміни калібрування: {sensor.temperature}°C")

try:
    sensor.temperature = "hot"
except TypeError as e:
    print(f"Помилка типу: {e}")

try:
    sensor.temperature = 200.0
except ValueError as e:
    print(f"Помилка значення: {e}")

try:
    print(sensor.__current_temp)
except AttributeError as e:
    print(f"Прямий доступ заборонено: {e}")

# Доступ через name mangling
print(f"Доступ через name mangling: {sensor._TemperatureSensor__current_temp}")

#ЗАВДАННЯ 3
import math

class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Вектор ({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        raise TypeError("Додавати можна лише вектори.")

    def __mul__(self, scalar: float) -> 'Vector2D':
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise TypeError("Множити можна лише на число.")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2D):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        return False

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

# Демонстрація
v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print(str(v1))          # __str__
print(repr(v2))         # __repr__
print(f"Сума: {v1 + v2}")       # __add__
print(f"Множення: {v1 * 2}")    # __mul__
print(f"Рівність: {v1 == Vector2D(3, 4)}") # __eq__
print(f"Довжина (модуль): {abs(v1)}")      # __abs__

#ЗАВДАННЯ 4
from abc import ABC, abstractmethod

# Абстрактний базовий клас (is-a)
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

    @abstractmethod
    def refund(self, amount: float) -> bool:
        pass

    @property
    @abstractmethod
    def commission_rate(self) -> float:
        pass

    # Конкретний метод
    def log_transaction(self, action: str, amount: float):
        print(f"[Лог] {action} на суму {amount} (комісія: {self.commission_rate*100}%)")


class CardPayment(PaymentProcessor):
    @property
    def commission_rate(self) -> float:
        return 0.02

    def pay(self, amount: float) -> bool:
        self.log_transaction("Оплата карткою", amount)
        return True

    def refund(self, amount: float) -> bool:
        self.log_transaction("Повернення на картку", amount)
        return True


class CryptoPayment(PaymentProcessor):
    @property
    def commission_rate(self) -> float:
        return 0.005

    def pay(self, amount: float) -> bool:
        self.log_transaction("Оплата криптою", amount)
        return True

    def refund(self, amount: float) -> bool:
        self.log_transaction("Повернення криптою", amount)
        return True


# Композиція (has-a)
class OrderItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items = []
        self._processor = None # Делегування

    def add_item(self, item: OrderItem):
        self.items.append(item)

    def set_payment_processor(self, processor: PaymentProcessor):
        self._processor = processor

    def checkout(self):
        if not self._processor:
            raise RuntimeError("Платіжний процесор не встановлено.")
        total = sum(item.price for item in self.items)
        print(f"Замовлення {self.order_id}. Сума: {total}")
        self._processor.pay(total) # Делегування

# Демонстрація
try:
    abstract_proc = PaymentProcessor()
except TypeError as e:
    print(f"Помилка інстанціювання ABC: {e}\n")

order = Order("ORD-001")
order.add_item(OrderItem("Ноутбук", 1000.0))
order.add_item(OrderItem("Миша", 25.0))

order.set_payment_processor(CryptoPayment())
order.checkout()

#ЗАВДАННЯ 5
# Інтерфейс стратегії
class ReportFormatter:
    def format(self, data: dict) -> str:
        raise NotImplementedError

# Конкретні стратегії
class PlainTextFormatter(ReportFormatter):
    def format(self, data: dict) -> str:
        return "\n".join(f"{k}: {v}" for k, v in data.items())

class HtmlFormatter(ReportFormatter):
    def format(self, data: dict) -> str:
        rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in data.items())
        return f"<table>{rows}</table>"

# Нова стратегія, додана без зміни існуючого коду
class JsonFormatter(ReportFormatter):
    def format(self, data: dict) -> str:
        items = ', '.join(f'"{k}": "{v}"' for k, v in data.items())
        return f"{{{items}}}"

# Контекст
class ReportGenerator:
    def __init__(self, formatter: ReportFormatter):
        self._formatter = formatter

    def set_formatter(self, formatter: ReportFormatter):
        self._formatter = formatter

    def generate(self, data: dict) -> str:
        return self._formatter.format(data)

# Клієнтський код
report_data = {"Name": "Alice", "Role": "Admin", "Status": "Active"}

generator = ReportGenerator(PlainTextFormatter())
print("Plain Text:\n" + generator.generate(report_data) + "\n")

generator.set_formatter(HtmlFormatter())
print("HTML:\n" + generator.generate(report_data) + "\n")

# Демонстрація розширюваності
generator.set_formatter(JsonFormatter())
print("JSON:\n" + generator.generate(report_data))
