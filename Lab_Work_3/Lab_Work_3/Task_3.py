from library_app.core import LibraryService
from library_app.utils import run_demo


def main() -> None:
    """Запускає демонстрацію бібліотечного сервісу.

    Returns:
        Нічого не повертає.

    Raises:
        Ніяких винятків не підносить.
    """
    print("=" * 60)
    print("Лабораторна робота №3")
    print("Документування та інтроспекція")
    print("=" * 60)

    print("\n--- Інтроспекція ---")
    print("Ім'я класу:", LibraryService.__name__)
    print("Документація класу:")
    print(LibraryService.__doc__)
    print("Анотації методу add_book:")
    print(LibraryService.add_book.__annotations__)

    help(LibraryService)

    run_demo()


if __name__ == "__main__":
    main()