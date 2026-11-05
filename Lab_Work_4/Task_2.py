"""Лабораторна робота №4, Завдання 2.
Виконав: Яковенко Кирило, група БІКСб-12-540
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QPushButton, QLineEdit, QSpinBox,
    QComboBox, QCheckBox, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt


# Звичайна функція (не метод класу) — слот для сигналу
def on_category_changed_external(category_index, status_label):
    """Обробник зміни категорії (зовнішня функція, не метод класу)."""
    categories = ["Студент", "Викладач", "Адміністратор", "Гість"]
    if 0 <= category_index < len(categories):
        status_label.setText(f"Обрано категорію: {categories[category_index]}")


def validate_form(name, age, category, agreed):
    """Валідація форми. Виділена в окрему функцію.

    Returns:
        (is_valid: bool, message: str)
    """
    if not name.strip():
        return False, "Поле 'Ім'я' не може бути порожнім!"
    if len(name.strip()) < 2:
        return False, "Ім'я має містити щонайменше 2 символи!"
    if age < 16 or age > 100:
        return False, "Вік має бути в діапазоні від 16 до 100!"
    if category == "Гість":
        return False, "Гості не можуть зареєструватися!"
    if not agreed:
        return False, "Ви повинні погодитися з умовами використання!"
    return True, ""


class MainWindow(QMainWindow):
    """Головне вікно з інтерактивною формою."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ЛБ №4, Завдання 2 — Сигнали та слоти | Яковенко БІКСб-12-540")
        self.setMinimumSize(550, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # === Група 1: Форма вводу ===
        form_group = QGroupBox("Реєстрація користувача")
        form_layout = QFormLayout()

        # Поле імені (текст)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ваше ім'я")
        self.name_input.setToolTip("Мінімум 2 символи")
        form_layout.addRow("Ім'я:", self.name_input)

        # Лічильник символів (оновлюється через сигнал textChanged)
        self.char_count_label = QLabel("Символів: 0")
        self.char_count_label.setStyleSheet("color: gray; font-size: 11px;")
        form_layout.addRow("", self.char_count_label)

        # Поле віку (число)
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(16, 100)
        self.age_spinbox.setValue(18)
        self.age_spinbox.setSuffix(" років")
        form_layout.addRow("Вік:", self.age_spinbox)

        # Мітка віку (оновлюється через сигнал valueChanged)
        self.age_status_label = QLabel("Вік: 18 років")
        form_layout.addRow("", self.age_status_label)

        # Вибір категорії (список)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Студент", "Викладач", "Адміністратор", "Гість"])
        self.category_combo.setCurrentIndex(0)
        form_layout.addRow("Категорія:", self.category_combo)

        # Чекбокс згоди
        self.agree_check = QCheckBox("Я погоджуюсь з умовами використання")
        self.agree_check.setToolTip("Обов'язково для реєстрації")
        form_layout.addRow("", self.agree_check)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # === Група 2: Статус та кнопки ===
        status_group = QGroupBox("Статус та дії")
        status_layout = QVBoxLayout()

        # Мітка статусу (оновлюється через зовнішню функцію)
        self.status_label = QLabel("Готовий до реєстрації")
        self.status_label.setStyleSheet("font-weight: bold; color: blue;")
        status_layout.addWidget(self.status_label)

        # Мітка результату валідації
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        status_layout.addWidget(self.result_label)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.submit_btn = QPushButton("Підтвердити")
        self.submit_btn.setEnabled(False)  # Деактивована, поки не поставлено чекбокс
        self.submit_btn.setToolTip("Натисніть для валідації та реєстрації")
        buttons_layout.addWidget(self.submit_btn)

        self.reset_btn = QPushButton("Скинути")
        self.reset_btn.setToolTip("Повернути форму до початкового стану")
        buttons_layout.addWidget(self.reset_btn)

        status_layout.addLayout(buttons_layout)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        # === З'ЄДНАННЯ СИГНАЛ-СЛОТ ===

        # 1. Вбудований сигнал + лямбда-вираз: оновлення лічильника символів
        self.name_input.textChanged.connect(
            lambda text: self.char_count_label.setText(f"Символів: {len(text)}")
        )

        # 2. Вбудований сигнал + метод класу: зміна властивості іншого віджета (мітки віку)
        self.age_spinbox.valueChanged.connect(self.on_age_changed)

        # 3. Вбудований сигнал + звичайна функція (не метод класу): оновлення статусу
        self.category_combo.currentIndexChanged.connect(
            lambda idx: on_category_changed_external(idx, self.status_label)
        )

        # 4. Вбудований сигнал + метод класу: активація/деактивація кнопки
        self.agree_check.stateChanged.connect(self.on_agree_changed)

        # 5. Кнопка підтвердження → валідація
        self.submit_btn.clicked.connect(self.on_submit)

        # 6. Кнопка скидання → reset
        self.reset_btn.clicked.connect(self.on_reset)

    def on_age_changed(self, value):
        """Слот: оновлює мітку віку при зміні значення QSpinBox."""
        self.age_status_label.setText(f"Вік: {value} років")

    def on_agree_changed(self, state):
        """Слот: активує/деактивує кнопку підтвердження залежно від стану чекбокса."""
        self.submit_btn.setEnabled(state == Qt.CheckState.Checked.value)

    def on_submit(self):
        """Слот: валідація форми та вивід результату."""
        name = self.name_input.text()
        age = self.age_spinbox.value()
        category = self.category_combo.currentText()
        agreed = self.agree_check.isChecked()

        is_valid, message = validate_form(name, age, category, agreed)

        if is_valid:
            self.result_label.setText(
                f"✅ Реєстрація успішна!\n"
                f"Ім'я: {name}, Вік: {age}, Категорія: {category}"
            )
            self.result_label.setStyleSheet("color: green;")
            self.status_label.setText("Користувача зареєстровано!")
            QMessageBox.information(
                self, "Успіх",
                f"Користувача '{name}' успішно зареєстровано як '{category}'!"
            )
        else:
            self.result_label.setText(f"❌ Помилка: {message}")
            self.result_label.setStyleSheet("color: red;")
            self.status_label.setText("Помилка валідації!")
            QMessageBox.warning(self, "Помилка валідації", message)

    def on_reset(self):
        """Слот: повертає форму до початкового стану."""
        self.name_input.clear()
        self.age_spinbox.setValue(18)
        self.category_combo.setCurrentIndex(0)
        self.agree_check.setChecked(False)
        self.submit_btn.setEnabled(False)
        self.result_label.setText("")
        self.status_label.setText("Готовий до реєстрації")
        self.char_count_label.setText("Символів: 0")
        self.age_status_label.setText("Вік: 18 років")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()