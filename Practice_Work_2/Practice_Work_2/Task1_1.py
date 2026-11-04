
class CyclicRange:


    def __init__(self, start: int, stop: int, step: int = 1, repeats: int = 1):
        self._start = start
        self._stop = stop
        self._step = step
        self._repeats = repeats
        self._current = start
        self._cycle = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        # 1. Якщо всі цикли завершені — raise StopIteration
        if self._cycle >= self._repeats:
            raise StopIteration

        # 2. Зберегти поточне значення
        value = self._current

        # 3. Оновити _current на крок
        self._current += self._step

        # 4. Якщо _current досяг _stop — скинути на _start, збільшити лічильник циклів
        # (Підтримуємо як позитивний, так і негативний крок)
        if (self._step > 0 and self._current >= self._stop) or \
           (self._step < 0 and self._current <= self._stop):
            self._current = self._start
            self._cycle += 1

        # 5. Повернути збережене значення
        return value


def main():
    # Базове використання
    print("CyclicRange(1, 4, repeats=3):")
    for num in CyclicRange(1, 4, repeats=3):
        print(num, end=" ")
    print()

    # З кроком
    print("\nCyclicRange(0, 10, step=3, repeats=2):")
    for num in CyclicRange(0, 10, step=3, repeats=2):
        print(num, end=" ")
    print()

    # Перетворення на список
    result = list(CyclicRange(5, 8, repeats=2))
    print(f"\nЯк список: {result}")

    # Обчислення суми елементів через sum()
    total = sum(CyclicRange(1, 5, repeats=2))
    print(f"Сума CyclicRange(1, 5, repeats=2): {total}")


if __name__ == "__main__":
    main()
