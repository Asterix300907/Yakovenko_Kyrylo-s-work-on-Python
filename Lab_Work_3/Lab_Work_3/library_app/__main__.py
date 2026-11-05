import library_app.utils.demo as demo
from library_app import *

if __name__ == "__main__":
    print("Запуск пакета library_app через python -m library_app")

    exported_names = [
        name
        for name in (
            "LibraryService",
            "LibraryError",
            "ValidationError",
            "ResourceNotFoundError",
            "BusinessLogicError",
            "run_demo",
        )
        if name in globals()
    ]

    print("Імена, отримані через from library_app import *:")
    print(exported_names)

    demo.run_demo()