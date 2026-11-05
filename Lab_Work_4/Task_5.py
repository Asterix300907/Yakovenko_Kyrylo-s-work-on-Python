"""Лабораторна робота №4, Завдання 5.
Виконав: Яковенко Кирило, група БІКСб-12-540
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem,
    QDialog, QLineEdit, QComboBox, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt


# ============================================================
# ГЛОБАЛЬНА СТИЛІЗАЦІЯ (QSS)
# ============================================================
APP_STYLESHEET = """
QMainWindow {
    background-color: #f4f6f9;
}

/* Глобальна стилізація міток */
QLabel {
    font-size: 14px;
    color: #2c3e50;
}

/* Стилізація конкретного віджета за objectName */
#title_label {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
    background-color: #2c3e50;
    padding: 15px;
    border-radius: 5px;
}

/* Глобальна стилізація кнопок */
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}

/* Псевдостан :hover */
QPushButton:hover {
    background-color: #2980b9;
}

/* Псевдостан :pressed */
QPushButton:pressed {
    background-color: #1f618d;
}

/* Псевдостан :disabled */
QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

/* Стилізація полів вводу та комбо-боксів */
QLineEdit, QComboBox {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px;
    background-color: white;
    font-size: 13px;
}

/* Псевдостан :focus для полів вводу */
QLineEdit:focus {
    border: 2px solid #3498db;
}

/* Стилізація списку */
QListWidget {
    background-color: white;
    border: 1px solid #bdc3c7;
    border-radius: 6px;
    font-size: 13px;
    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #ecf0f1;
}

QListWidget::item:selected {
    background-color: #3498db;
    color: white;
    border-radius: 4px;
}
"""


# ============================================================
# ВЛАСНЕ МОДАЛЬНЕ ДІАЛОГОВЕ ВІКНО
# ============================================================
class AddUserDialog(QDialog):
    """Власне модальне діалогове вікно для додавання співробітника."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додавання співробітника")
        self.setMinimumWidth(350)
        self.setModal(True)  # Робимо вікно модальним

        layout = QVBoxLayout(self)

        # Поле Ім'я
        layout.addWidget(QLabel("Ім'я та Прізвище:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Наприклад: Іван Петренко")
        layout.addWidget(self.name_input)

        # Поле Посада
        layout.addWidget(QLabel("Посада:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Розробник", "Дизайнер", "Менеджер", "Тестувальник", "HR"])
        layout.addWidget(self.role_combo)

        # Поле Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ivan@example.com")
        layout.addWidget(self.email_input)

        # Кнопки OK та Cancel
        buttons_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Додати")
        self.ok_btn.clicked.connect(self.accept)  # Повертає QDialog.DialogCode.Accepted
        self.cancel_btn = QPushButton("Скасувати")
        self.cancel_btn.setStyleSheet("background-color: #e74c3c;")  # Точкова inline-стилізація
        self.cancel_btn.clicked.connect(self.reject)  # Повертає QDialog.DialogCode.Rejected

        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)

    def get_user_data(self):
        """Повертає введені дані."""
        return {
            'name': self.name_input.text().strip(),
            'role': self.role_combo.currentText(),
            'email': self.email_input.text().strip()
        }


# ============================================================
# ГОЛОВНЕ ВІКНО
# ============================================================
class MainWindow(QMainWindow):
    """Головне вікно додатка 'Каталог співробітників'."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ЛБ №4, Завдання 5 — Діалоги та QSS | Яковенко БІКСб-12-540")
        self.setMinimumSize(600, 500)

        # Застосування глобальної стилізації
        self.setStyleSheet(APP_STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок (з objectName для специфічної стилізації)
        self.title_label = QLabel("📁 Каталог співробітників")
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Мітка статусу (змінюватиметься через QInputDialog)
        self.status_label = QLabel("Статус: Очікування дій користувача...")
        self.status_label.setStyleSheet("font-style: italic; color: #7f8c8d;")
        main_layout.addWidget(self.status_label)

        # Список співробітників
        self.user_list = QListWidget()
        self.user_list.setAlternatingRowColors(True)
        main_layout.addWidget(self.user_list)

        # Панель кнопок
        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ Додати співробітника")
        self.add_btn.clicked.connect(self.add_user)
        buttons_layout.addWidget(self.add_btn)

        self.theme_btn = QPushButton("🎨 Змінити статус")
        self.theme_btn.clicked.connect(self.change_status)
        buttons_layout.addWidget(self.theme_btn)

        self.clear_btn = QPushButton("🗑 Очистити список")
        self.clear_btn.clicked.connect(self.clear_list)
        buttons_layout.addWidget(self.clear_btn)

        main_layout.addLayout(buttons_layout)

    # --- Обробники кнопок (Діалоги) ---

    def add_user(self):
        """1. ВЛАСНЕ МОДАЛЬНЕ ДІАЛОГОВЕ ВІКНО (QDialog)."""
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_user_data()
            if not data['name'] or not data['email']:
                QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть Ім'я та Email!")
                return

            item_text = f"👤 {data['name']} | 💼 {data['role']} | ✉️ {data['email']}"
            item = QListWidgetItem(item_text)
            self.user_list.addItem(item)
            self.status_label.setText(f"Статус: Додано нового співробітника — {data['name']}")

    def change_status(self):
        """2. СТАНДАРТНИЙ ДІАЛОГ ВВОДУ (QInputDialog)."""
        statuses = ["Активна робота", "Перерва", "Нарада", "Відпустка", "Лікарняний"]
        current_status = self.status_label.text().replace("Статус: ", "")

        selected_status, ok = QInputDialog.getItem(
            self,
            "Зміна статусу",
            "Оберіть поточний статус системи:",
            statuses,
            0,  # індекс за замовчуванням
            False  # поле не редагується
        )

        if ok and selected_status:
            self.status_label.setText(f"Статус: {selected_status}")
            # Демонстрація точкової зміни стилю
            if selected_status == "Відпустка":
                self.status_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 16px;")
            elif selected_status == "Лікарняний":
                self.status_label.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 16px;")
            else:
                self.status_label.setStyleSheet("font-style: italic; color: #7f8c8d;")

    def clear_list(self):
        """3. СТАНДАРТНИЙ ДІАЛОГ ПІДТВЕРДЖЕННЯ (QMessageBox)."""
        if self.user_list.count() == 0:
            QMessageBox.information(self, "Інформація", "Список і так порожній!")
            return

        reply = QMessageBox.question(
            self,
            "Підтвердження видалення",
            f"Ви впевнені, що хочете видалити всі {self.user_list.count()} записів?\n"
            "Цю дію неможливо скасувати.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.user_list.clear()
            self.status_label.setText("Статус: Список успішно очищено")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()