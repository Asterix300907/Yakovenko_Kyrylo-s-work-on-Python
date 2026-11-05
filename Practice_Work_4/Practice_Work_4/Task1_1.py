"""Створення та керування потоками в Python."""

import threading
import time


def download_simulation(file_name: str, size_mb: float) -> dict:
    """Імітація завантаження файлу (I/O-bound задача)."""
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Початок завантаження '{file_name}' ({size_mb} MB)...")
    time.sleep(size_mb * 0.5)  # імітація: 0.5 с на 1 MB
    print(f"[{thread_name}] Завершено '{file_name}'")
    return {"file": file_name, "size": size_mb, "thread": thread_name}


class MonitorThread(threading.Thread):
    """Потік-монітор, що періодично виводить стан системи."""

    def __init__(self, interval: float = 1.0):
        super().__init__(name="Monitor", daemon=True)
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            print(f"[Monitor] Активних потоків: {threading.active_count()}")
            self._stop_event.wait(self.interval)

    def stop(self):
        self._stop_event.set()


def main():
    files = [
        ("data.csv", 2.5),
        ("report.pdf", 1.0),
        ("image.png", 0.5),
        ("archive.zip", 4.0),
        ("log.txt", 0.3),
    ]

    # Запуск демон-потоку моніторингу
    monitor = MonitorThread(interval=0.5)
    monitor.start()

    # Створення потоків для завантаження
    threads = []
    for file_name, size_mb in files:
        t = threading.Thread(
            target=download_simulation,
            args=(file_name, size_mb),
            name=f"Download-{file_name}",
        )
        threads.append(t)

    # Паралельне виконання
    print("\n=== Паралельне завантаження ===")
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed_parallel = time.perf_counter() - start

    # Зупинка монітора
    monitor.stop()
    monitor.join(timeout=1.0)

    print(f"\nУсі файли завантажено за {elapsed_parallel:.2f} сек")

    # Послідовне виконання для порівняння
    print("\n=== Послідовне завантаження ===")
    start = time.perf_counter()
    for file_name, size_mb in files:
        download_simulation(file_name, size_mb)
    elapsed_sequential = time.perf_counter() - start

    print(f"\nПослідовно: {elapsed_sequential:.2f} сек")
    print(f"Паралельно: {elapsed_parallel:.2f} сек")
    print(f"Прискорення: {elapsed_sequential / elapsed_parallel:.2f}x")


if __name__ == "__main__":
    main()