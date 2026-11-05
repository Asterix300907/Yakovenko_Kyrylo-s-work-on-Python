"""Декоратори класів."""

import functools
import time


def auto_repr(cls):
    """Декоратор класу: додає __repr__ на основі параметрів __init__."""
    init = cls.__init__
    param_names = init.__code__.co_varnames[1:init.__code__.co_argcount]

    def __repr__(self):
        args = ", ".join(f"{name}={getattr(self, name)!r}" for name in param_names)
        return f"{cls.__name__}({args})"

    cls.__repr__ = __repr__
    return cls


def frozen(cls):
    """Декоратор класу: забороняє зміну атрибутів після __init__."""
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError(
                f"Не можна змінити атрибут '{name}' після ініціалізації"
            )
        object.__setattr__(self, name, value)

    cls.__init__ = new_init
    cls.__setattr__ = __setattr__
    return cls


def log_methods(cls):
    """Декоратор класу: логує виклики всіх публічних методів."""
    for name, attr in list(vars(cls).items()):
        if name.startswith("_") or not callable(attr):
            continue

        @functools.wraps(attr)
        def wrapper(self, *args, _name=name, _method=attr, **kwargs):
            args_repr = ", ".join(repr(a) for a in args)
            print(f"  [LOG] {cls.__name__}.{_name}({args_repr})")
            start = time.perf_counter()
            try:
                result = _method(self, *args, **kwargs)
                elapsed = time.perf_counter() - start
                print(f"  [LOG] → {result} ({elapsed:.4f}с)")
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                print(f"  [LOG] → {type(e).__name__}: {e} ({elapsed:.4f}с)")
                raise

        setattr(cls, name, wrapper)
    return cls


# --- Застосування декораторів ---

@auto_repr
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@frozen
class ImmutableConfig:
    def __init__(self, host: str, port: int, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug


@log_methods
class MathService:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Ділення на нуль")
        return a / b


def main():
    print("=== 1. Декоратор @auto_repr ===")
    p = Point(3.0, 4.0)
    print(f"repr: {repr(p)}")
    print(f"distance_to(Point(0, 0)): {p.distance_to(Point(0.0, 0.0))}")

    print("\n=== 2. Декоратор @frozen ===")
    cfg = ImmutableConfig("localhost", 8080, debug=True)
    print(f"Config: {cfg.host}:{cfg.port} (debug={cfg.debug})")
    try:
        cfg.host = "remote"
    except AttributeError as e:
        print(f"Очікувана помилка: {e}")

    print("\n=== 3. Декоратор @log_methods ===")
    svc = MathService()
    svc.add(10, 20)
    svc.multiply(3, 7)
    try:
        svc.divide(10, 0)
    except ValueError:
        print("  ValueError перехоплено зовнішнім блоком")


if __name__ == "__main__":
    main()