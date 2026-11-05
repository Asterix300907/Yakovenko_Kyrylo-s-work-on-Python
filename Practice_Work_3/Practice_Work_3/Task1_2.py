"""Типізовані дескриптори та __init_subclass__ для системи конфігурації."""


class ValidatedField:
    """Дескриптор із валідацією типу та діапазону значень."""

    def __init__(self, expected_type: type, min_value=None, max_value=None):
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"'{self.name}' має бути {self.expected_type.__name__}, "
                f"отримано {type(value).__name__}"
            )
        if self.min_value is not None and value < self.min_value:
            raise ValueError(
                f"'{self.name}' має бути >= {self.min_value}, отримано {value}"
            )
        if self.max_value is not None and value > self.max_value:
            raise ValueError(
                f"'{self.name}' має бути <= {self.max_value}, отримано {value}"
            )
        setattr(obj, self.private_name, value)


class ConfigSection:
    """Базовий клас секції конфігурації з автоматичною реєстрацією."""

    _sections: dict[str, type] = {}

    def __init_subclass__(cls, section_name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if section_name:
            ConfigSection._sections[section_name] = cls

    @classmethod
    def get_section(cls, name: str):
        """Повертає клас секції за іменем."""
        if name not in cls._sections:
            raise KeyError(f"Секція '{name}' не зареєстрована")
        return cls._sections[name]

    @classmethod
    def list_sections(cls) -> list[str]:
        """Повертає список усіх зареєстрованих секцій."""
        return list(cls._sections.keys())


class DatabaseConfig(ConfigSection, section_name="database"):
    host = ValidatedField(str)
    port = ValidatedField(int, min_value=1, max_value=65535)
    max_connections = ValidatedField(int, min_value=1, max_value=1000)

    def __init__(self, host: str, port: int, max_connections: int):
        self.host = host
        self.port = port
        self.max_connections = max_connections

    def __repr__(self):
        return (
            f"DatabaseConfig(host={self.host!r}, port={self.port}, "
            f"max_connections={self.max_connections})"
        )


class LoggingConfig(ConfigSection, section_name="logging"):
    level = ValidatedField(str)
    max_file_size_mb = ValidatedField(int, min_value=1, max_value=1024)

    def __init__(self, level: str, max_file_size_mb: int):
        self.level = level
        self.max_file_size_mb = max_file_size_mb

    def __repr__(self):
        return (
            f"LoggingConfig(level={self.level!r}, "
            f"max_file_size_mb={self.max_file_size_mb})"
        )


def main():
    print("Зареєстровані секції:", ConfigSection.list_sections())

    print("\nСтворення DatabaseConfig з коректними значеннями:")
    db = DatabaseConfig(host="localhost", port=5432, max_connections=100)
    print(f"  {db}")

    print("\nВалідація типу (TypeError):")
    try:
        db.port = "not_a_number"
    except TypeError as e:
        print(f"  Перехоплено: {e}")

    print("\nВалідація діапазону (ValueError):")
    try:
        db.port = 70000
    except ValueError as e:
        print(f"  Перехоплено: {e}")

    print("\nСтворення LoggingConfig:")
    log = LoggingConfig(level="INFO", max_file_size_mb=50)
    print(f"  {log}")

    print("\nОтримання секції за іменем:")
    cls = ConfigSection.get_section("database")
    print(f"  Клас: {cls.__name__}")


if __name__ == "__main__":
    main()