"""Порівняльний аналіз структури Django та Flask проектів."""

import os


# Файли та папки, які треба ігнорувати
SKIP_NAMES = {
    '__pycache__', '.pyc', 'venv', 'venv2', 'env',
    '.git', '.vs', 'db.sqlite3', '*.pyc',
    '.idea', '.vscode', 'node_modules',
}


def should_skip(name: str) -> bool:
    """Перевіряє, чи треба пропустити файл/папку."""
    if name in SKIP_NAMES:
        return True
    if name.endswith('.pyc'):
        return True
    if name.endswith('.sqlite3'):
        return True
    return False


def scan_directory(path: str, prefix: str = '') -> list[str]:
    """Рекурсивно сканує каталог та повертає дерево файлів.

    Args:
        path: шлях до каталогу.
        prefix: відступ для форматування дерева.

    Returns:
        Список рядків зі структурою каталогу.
    """
    tree = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return tree

    # Фільтруємо
    entries = [e for e in entries if not should_skip(e)]

    for i, name in enumerate(entries):
        full_path = os.path.join(path, name)
        is_last = (i == len(entries) - 1)
        connector = '└── ' if is_last else '├── '
        tree.append(f"{prefix}{connector}{name}")

        if os.path.isdir(full_path):
            extension = '    ' if is_last else '│   '
            subtree = scan_directory(full_path, prefix + extension)
            tree.extend(subtree)

    return tree


def analyze_project(path: str) -> dict:
    """Аналізує проект та збирає статистику.

    Args:
        path: кореневий каталог проекту.

    Returns:
        Словник зі статистикою.
    """
    stats = {
        'py_files': 0,
        'html_files': 0,
        'css_files': 0,
        'total_size': 0,
        'directories': 0,
        'all_files': 0,
    }

    for root, dirs, files in os.walk(path):
        # Видаляємо службові папки з обходу
        dirs[:] = [d for d in dirs if not should_skip(d)]

        for file in files:
            if should_skip(file):
                continue

            full_path = os.path.join(root, file)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0

            stats['total_size'] += size
            stats['all_files'] += 1

            if file.endswith('.py'):
                stats['py_files'] += 1
            elif file.endswith('.html'):
                stats['html_files'] += 1
            elif file.endswith('.css'):
                stats['css_files'] += 1

        stats['directories'] += 1

    return stats


def format_size(size_bytes: int) -> str:
    """Форматує розмір у зручному вигляді."""
    if size_bytes < 1024:
        return f"{size_bytes} Б"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} КБ"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} МБ"


def compare_projects(django_path: str, flask_path: str):
    """Порівнює два проекти та виводить таблицю відмінностей."""
    print("=" * 60)
    print("ПОРІВНЯННЯ СТРУКТУРИ ПРОЕКТІВ")
    print("=" * 60)

    # Django
    print(f"\n--- Django ({django_path}) ---")
    django_tree = scan_directory(django_path)
    for line in django_tree:
        print(line)
    django_stats = analyze_project(django_path)

    # Flask
    print(f"\n--- Flask ({flask_path}) ---")
    flask_tree = scan_directory(flask_path)
    for line in flask_tree:
        print(line)
    flask_stats = analyze_project(flask_path)

    # Порівняльна таблиця
    print("\n" + "=" * 60)
    print("ПОРІВНЯЛЬНА ТАБЛИЦЯ")
    print("=" * 60)
    print(f"{'Характеристика':<25} | {'Django':<10} | {'Flask':<10}")
    print("-" * 25 + "-+-" + "-" * 10 + "-+-" + "-" * 10)
    print(f"{'Файли .py':<25} | {django_stats['py_files']:<10} | {flask_stats['py_files']:<10}")
    print(f"{'Файли .html':<25} | {django_stats['html_files']:<10} | {flask_stats['html_files']:<10}")
    print(f"{'Файли .css':<25} | {django_stats['css_files']:<10} | {flask_stats['css_files']:<10}")
    print(f"{'Всього файлів':<25} | {django_stats['all_files']:<10} | {flask_stats['all_files']:<10}")
    print(f"{'Каталоги':<25} | {django_stats['directories']:<10} | {flask_stats['directories']:<10}")
    print(f"{'Розмір':<25} | {format_size(django_stats['total_size']):<10} | {format_size(flask_stats['total_size']):<10}")
    print("=" * 60)


def main():
    django_path = 'mysite'
    flask_path = 'myflaskapp'

    for path in [django_path, flask_path]:
        if not os.path.isdir(path):
            print(f"Каталог '{path}' не знайдено. Спершу виконайте попередні завдання.")
            return

    compare_projects(django_path, flask_path)


if __name__ == "__main__":
    main()