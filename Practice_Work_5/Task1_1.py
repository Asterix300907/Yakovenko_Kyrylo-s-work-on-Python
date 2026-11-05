"""Скрипт перевірки середовища розробки."""

import sys
import importlib


def check_python_version():
    """Перевіряє версію Python (потрібна >= 3.10)."""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if (version.major, version.minor) >= (3, 10):
        print("  Версія Python відповідає вимогам (>= 3.10) ✓")
    else:
        print(f" Попередження: потрібна Python >= 3.10, "
              f"у вас {version.major}.{version.minor}")
        print("  Деякі функції можуть працювати некоректно.")


def check_package(package_name: str) -> bool:
    """Перевіряє, чи встановлено пакет, і виводить його версію.

    Args:
        package_name: назва пакета для перевірки.

    Returns:
        True, якщо пакет встановлено.
    """
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'невідома')
        print(f"  {package_name}: {version} ")
        return True
    except ImportError:
        print(f"  {package_name}: НЕ ВСТАНОВЛЕНО ")
        return False


def main():
    print("=" * 50)
    print("Перевірка середовища розробки")
    print("=" * 50)

    check_python_version()

    print("\nВстановлені пакети:")
    packages = ['django', 'flask']
    results = {pkg: check_package(pkg) for pkg in packages}

    # Підсумок
    installed = sum(results.values())
    missing = len(results) - installed

    print(f"\n{'=' * 50}")
    print(f"Підсумок: встановлено {installed}/{len(results)} пакетів")
    
    if missing > 0:
        missing_packages = [pkg for pkg, ok in results.items() if not ok]
        print(f"Відсутні пакети: {', '.join(missing_packages)}")
        print("\nДля встановлення виконайте:")
        print(f"  pip install {' '.join(missing_packages)}")
    else:
        print("Усі необхідні пакети встановлено ")
    
    print("=" * 50)


if __name__ == "__main__":
    main()