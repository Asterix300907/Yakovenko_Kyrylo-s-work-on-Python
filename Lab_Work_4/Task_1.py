"""Лабораторна робота №4, Завдання 1.
Виконав: Яковенко Кирило, група БІКСб-12-540
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QPushButton, QLineEdit, QTextEdit,
    QComboBox, QCheckBox, QRadioButton, QSlider, QSpinBox,
    QProgressBar, QGroupBox
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Головне вікно додатка з базовими віджетами."""

    def __init__(self):
        super().__init__()

        # Налаштування вікна
        self.setWindowTitle("ЛБ №4 — PyQt6 Додаток | Яковенко БІКСб-12-540")
        self.setMinimumSize(600, 500)

        # Головний віджет і layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # === Група 1: Ввід даних (QFormLayout) ===
        form_group = QGroupBox("Форма вводу даних")
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ваше ім'я")
        self.name_input.setToolTip("Поле для вводу імені користувача")
        form_layout.addRow("Ім'я:", self.name_input)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Студент", "Викладач", "Адміністратор"])
        self.category_combo.setCurrentIndex(0)
        self.category_combo.setToolTip("Оберіть категорію користувача")
        form_layout.addRow("Категорія:", self.category_combo)

        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(16, 100)
        self.age_spinbox.setValue(20)
        self.age_spinbox.setSuffix(" років")
        form_layout.addRow("Вік:", self.age_spinbox)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # === Група 2: Налаштування (QHBoxLayout) ===
        options_group = QGroupBox("Налаштування")
        options_layout = QHBoxLayout()

        self.dark_mode_check = QCheckBox("Темна тема")
        self.dark_mode_check.setToolTip("Увімкнути темну тему інтерфейсу")
        options_layout.addWidget(self.dark_mode_check)

        self.notifications_check = QCheckBox("Сповіщення")
        self.notifications_check.setChecked(True)
        self.notifications_check.setToolTip("Отримувати сповіщення")
        options_layout.addWidget(self.notifications_check)

        self.male_radio = QRadioButton("Чоловіча")
        self.male_radio.setChecked(True)
        options_layout.addWidget(self.male_radio)

        self.female_radio = QRadioButton("Жіноча")
        options_layout.addWidget(self.female_radio)

        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # === Група 3: Прогрес та слайдер (QVBoxLayout) ===
        progress_group = QGroupBox("Прогрес виконання")
        progress_layout = QVBoxLayout()

        self.progress_label = QLabel("Рівень завантаження: 0%")
        progress_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setToolTip("Перемістіть для зміни прогресу")
        progress_layout.addWidget(self.slider)

        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)

        # === Група 4: Текстовий вивід та кнопки (QHBoxLayout) ===
        output_group = QGroupBox("Вивід інформації")
        output_layout = QVBoxLayout()

        self.info_text = QTextEdit()
        self.info_text.setPlaceholderText("Тут з'явиться інформація...")
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(100)
        output_layout.addWidget(self.info_text)

        buttons_layout = QHBoxLayout()

        self.show_btn = QPushButton("Показати інформацію")
        self.show_btn.setToolTip("Натисніть для виводу даних")
        buttons_layout.addWidget(self.show_btn)

        self.clear_btn = QPushButton("Очистити")
        self.clear_btn.setToolTip("Очистити текстове поле")
        buttons_layout.addWidget(self.clear_btn)

        self.exit_btn = QPushButton("Вихід")
        self.exit_btn.setToolTip("Закрити додаток")
        self.exit_btn.clicked.connect(self.close)
        buttons_layout.addWidget(self.exit_btn)

        output_layout.addLayout(buttons_layout)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()