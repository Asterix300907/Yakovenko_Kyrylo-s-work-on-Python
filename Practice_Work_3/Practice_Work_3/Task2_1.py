"""Декоратори функцій з параметрами."""

import functools
import time


def cache(max_size: int = 128):
    """Декоратор кешування результатів функції (спрощений LRU-кеш)."""

    def decorator(func):
        _cache = {}
        _call_order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in _cache:
                # Перемістити ключ в кінець (LRU)
                _call_order.remove(args)
                _call_order.append(args)
                print(f"  [cache hit] {func.__name__}{args}")
                return _cache[args]

            result = func(*args)
            _cache[args] = result
            _call_order.append(args)
            print(f"  [cache miss] {func.__name__}{args} = {result}")

            # Видалити найстаріший запис, якщо кеш переповнений
            if len(_cache) > max_size:
                oldest = _call_order.pop(0)
                del _cache[oldest]

            return result

        wrapper.cache_info = lambda: {"size": len(_cache), "max_size": max_size}
        wrapper.cache_clear = lambda: (_cache.clear(), _call_order.clear())
        return wrapper

    return decorator


def rate_limit(max_calls: int, period: float = 60.0):
    """Декоратор обмеження частоти викликів функції."""

    def decorator(func):
        call_times = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Видалити записи, старші за period
            call_times[:] = [t for t in call_times if now - t < period]

            if len(call_times) >= max_calls:
                raise RuntimeError(
                    f"Перевищено ліміт: {max_calls} викликів за {period} с"
                )

            call_times.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log(level: str = "INFO"):
    """Декоратор логування виклику функції з рівнем."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = ", ".join(
                [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
            )
            print(f"  [{level}] Виклик {func.__name__}({args_repr})")

            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                elapsed = time.perf_counter() - start
                print(f"  [ERROR] {func.__name__} → {type(e).__name__}: {e} ({elapsed:.4f}с)")
                raise

            elapsed = time.perf_counter() - start
            print(f"  [{level}] {func.__name__} → {result} (час: {elapsed:.4f}с)")
            return result

        return wrapper

    return decorator


# --- Застосування декораторів ---

@cache(max_size=64)
def fibonacci(n: int) -> int:
    """Обчислює n-е число Фібоначчі рекурсивно."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@rate_limit(max_calls=5, period=10.0)
def send_notification(message: str) -> str:
    """Імітує відправку сповіщення."""
    return f"Надіслано: {message}"


@log(level="DEBUG")
def divide(a: float, b: float) -> float:
    """Ділення з можливим ZeroDivisionError."""
    return a / b


def main():
    print("=== 1. Декоратор cache (fibonacci) ===")
    result = fibonacci(30)
    print(f"fibonacci(30) = {result}")
    print(f"Статистика кешу: {fibonacci.cache_info()}")

    print("\nПовторний виклик fibonacci(30) — має бути cache hit:")
    fibonacci(30)
    print(f"Статистика кешу: {fibonacci.cache_info()}")

    print("\n=== 2. Декоратор rate_limit ===")
    for i in range(1, 7):
        try:
            msg = send_notification(f"Тестове повідомлення #{i}")
            print(f"  Виклик #{i}: {msg}")
        except RuntimeError as e:
            print(f"  Виклик #{i}: {e}")

    print("\n=== 3. Декоратор log ===")
    divide(10, 3)
    print()
    try:
        divide(10, 0)
    except ZeroDivisionError:
        print("  ZeroDivisionError перехоплено зовнішнім блоком")


if __name__ == "__main__":
    main()