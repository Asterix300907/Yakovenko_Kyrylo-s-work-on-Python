"""Система плагінів з автоматичною реєстрацією через метаклас."""

from abc import abstractmethod


class PluginMeta(type):
    """Метаклас для автоматичної реєстрації та валідації плагінів."""

    _registry: dict[str, type] = {}
    REQUIRED_ATTRS = ("name", "version")

    def __new__(mcs, cls_name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, cls_name, bases, namespace)

        # Валідуємо тільки підкласи (не сам BasePlugin)
        if bases:
            for attr in mcs.REQUIRED_ATTRS:
                if attr not in namespace:
                    raise TypeError(
                        f"Клас '{cls_name}' повинен мати атрибут '{attr}'"
                    )
            mcs._registry[namespace["name"]] = cls

        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        """Повертає копію реєстру плагінів."""
        return dict(mcs._registry)

    @classmethod
    def create_plugin(mcs, plugin_name: str):
        """Фабричний метод: створює екземпляр плагіна за його name."""
        if plugin_name not in mcs._registry:
            raise KeyError(f"Плагін '{plugin_name}' не зареєстровано")
        return mcs._registry[plugin_name]()


class BasePlugin(metaclass=PluginMeta):
    """Базовий клас плагіна."""

    @abstractmethod
    def execute(self, data: str) -> str:
        """Обробити вхідні дані."""


# --- Конкретні плагіни ---

class UpperPlugin(BasePlugin):
    name = "upper"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data.upper()


class ReversePlugin(BasePlugin):
    name = "reverse"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data[::-1]


class CensorPlugin(BasePlugin):
    name = "censor"
    version = "1.1"
    banned_words = ("біс", "чорт", "дідько")

    def execute(self, data: str) -> str:
        result = data
        for word in self.banned_words:
            result = result.replace(word, "***")
        return result


# --- Динамічне створення класу через type() ---

def _hash_execute(self, data: str) -> str:
    return str(hash(data))


HashPlugin = type(
    "HashPlugin",
    (BasePlugin,),
    {"name": "hash", "version": "2.0", "execute": _hash_execute},
)


def main():
    print("Зареєстровані плагіни:")
    for name, cls in PluginMeta.get_registry().items():
        print(f"  {name} (v{cls.version}): {cls.__name__}")

    print("\nВиконання плагінів на даних 'Привіт Світ':")
    test_data = "Привіт Світ"
    for name in PluginMeta.get_registry():
        plugin = PluginMeta.create_plugin(name)
        print(f"  {name}: {plugin.execute(test_data)}")

    print("\nДемонстрація валідації (клас без атрибута 'name'):")
    try:
        type("BadPlugin", (BasePlugin,), {"version": "1.0"})
    except TypeError as e:
        print(f"  Перехоплено: {e}")


if __name__ == "__main__":
    main()