"""Генератор requirements.txt з перевіркою залежностей."""

import json
import subprocess
import sys
import os


def get_installed_packages() -> list[dict]:
    """Повертає список встановлених пакетів з версіями.

    Returns:
        Список словників {'name': ..., 'version': ...}.
    """
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=json'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Помилка pip: {result.stderr}")
        return []
    
    packages = json.loads(result.stdout)
    return packages


def generate_requirements(packages: list[dict], filename: str = 'requirements.txt'):
    """Записує пакети у файл requirements.txt.

    Args:
        packages: список словників з ключами 'name' та 'version'.
        filename: ім'я файлу для запису.
    """
    # Фільтруємо системні пакети
    skip = {'pip', 'setuptools', 'wheel', 'distribute'}
    filtered = [p for p in packages if p['name'].lower() not in skip]

    with open(filename, 'w', encoding='utf-8') as f:
        for pkg in filtered:
            f.write(f"{pkg['name']}=={pkg['version']}\n")


def verify_requirements(filename: str = 'requirements.txt') -> bool:
    """Перевіряє, чи всі пакети з requirements.txt встановлені.

    Args:
        filename: шлях до файлу requirements.txt.

    Returns:
        True, якщо всі залежності задоволені.
    """
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не знайдено!")
        return False

    # Отримуємо список встановлених пакетів
    installed = get_installed_packages()
    installed_names = {p['name'].lower() for p in installed}

    all_ok = True
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '==' in line:
                name, version = line.split('==', 1)
            else:
                name = line
                version = None

            if name.lower() not in installed_names:
                print(f"  ✗ {name} — НЕ ВСТАНОВЛЕНО")
                all_ok = False
            elif version:
                # Перевіряємо точну версію
                for pkg in installed:
                    if pkg['name'].lower() == name.lower():
                        if pkg['version'] != version:
                            print(f"  ⚠ {name}: очікувалось {version}, "
                                  f"встановлено {pkg['version']}")
                        break

    return all_ok


def main():
    print("=" * 50)
    print("Генератор та перевірка requirements.txt")
    print("=" * 50)

    packages = get_installed_packages()
    print(f"\nЗнайдено {len(packages)} встановлених пакетів\n")

    for pkg in packages[:10]:
        print(f"  {pkg['name']}=={pkg['version']}")
    if len(packages) > 10:
        print(f"  ... та ще {len(packages) - 10}")

    generate_requirements(packages)
    print(f"\nФайл requirements.txt створено")

    ok = verify_requirements()
    print(f"\nПеревірка залежностей: {'✓ Усе OK' if ok else '✗ Є розбіжності'}")
    print("=" * 50)


if __name__ == "__main__":
    main()