import json
import os
from typing import Optional


# --- Власний контекстний менеджер ---
class LogFile:
    """Контекстний менеджер для запису лог-файлу.

    Замінює явну конструкцію try/finally: __exit__ гарантує
    закриття файлу навіть у разі виключення.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self._file = None

    def __enter__(self) -> "LogFile":
        self._file = open(self.path, "a", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._file is not None:
            self._file.close()
        return False

    def write(self, text: str) -> None:
        if self._file is not None:
            self._file.write(text + "\n")


# --- Сценарій 1: базовий try/except ---
def read_config(path: str) -> Optional[dict]:
    """Читає JSON-файл конфігурації.

    Перехоплює FileNotFoundError та json.JSONDecodeError.
    """
    print(f"\n[Сценарій 1] Читання '{path}'")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  Файл '{path}' не знайдено.")
    except json.JSONDecodeError as e:
        print(f"  Некоректний JSON у '{path}': {e}")
    return None


# --- Сценарій 2: повний try/except/else/finally ---
def divide_inputs(a_str: str, b_str: str) -> Optional[float]:
    """Ділить два числа, введені як рядки.

    else — виконується обчислення, якщо не було виключень.
    finally — виконується завжди.
    """
    print(f"\n[Сценарій 2] Ділення {a_str} / {b_str}")
    result = None
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        print("  Ввід не є числом.")
    except ZeroDivisionError:
        print("  Ділення на нуль.")
    else:
        if b == 0:
            print("  Ділення на нуль неможливе.")
        else:
            result = a / b
            print(f"  Результат: {result}")
    finally:
        print("  Операція ділення завершена.")
    return result


# --- Сценарій 3: кілька типів виключень одним блоком ---
def process_files(paths: list[str]) -> list[dict]:
    """Читає список JSON-файлів.

    Один блок except перехоплює FileNotFoundError,
    PermissionError та json.JSONDecodeError.
    """
    print("\n[Сценарій 3] Обробка списку файлів")
    results: list[dict] = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            results.append(data)
            print(f"  '{path}' — прочитано.")
        except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
            print(f"  '{path}' — пропущено ({type(e).__name__}).")
    return results


# --- Демонстрація контекстного менеджера ---
def demo_context_manager() -> None:
    """Демонстрація LogFile у блоці with."""
    print("\n[Контекстний менеджер] Запис у log.txt")
    log_path = "log.txt"
    try:
        with LogFile(log_path) as log:
            log.write("Початок роботи")
            log.write("Крок 1")
            raise RuntimeError("тестова помилка")
    except RuntimeError as e:
        print(f"  Перехоплено: {e}")
    finally:
        if os.path.exists(log_path):
            os.remove(log_path)
            print("  log.txt видалено.")


# --- Головний блок ---
def main() -> None:
    print("=" * 50)
    print("Лабораторна робота №3, Завдання 1")
    print("=" * 50)

    # Сценарій 1: успіх і помилка
    cfg = read_config("config.json")
    if cfg is None:
        # створимо файл і прочитаємо знову
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({"theme": "dark", "lang": "uk"}, f)
        cfg = read_config("config.json")
    if os.path.exists("config.json"):
        os.remove("config.json")

    # Сценарій 2: успіх і помилки
    divide_inputs("10", "3")
    divide_inputs("abc", "5")
    divide_inputs("10", "0")

    # Сценарій 3: суміш файлів
    with open("ok.json", "w", encoding="utf-8") as f:
        json.dump({"status": "ok"}, f)
    with open("bad.json", "w", encoding="utf-8") as f:
        f.write("{не json")
    process_files(["ok.json", "missing.json", "bad.json"])
    for name in ["ok.json", "bad.json"]:
        if os.path.exists(name):
            os.remove(name)

    # Контекстний менеджер
    demo_context_manager()

    print("\nРоботу завершено.")


if __name__ == "__main__":
    main()
