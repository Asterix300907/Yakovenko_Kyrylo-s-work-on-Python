"""Лабораторна робота №4, Завдання 3.
Виконав: Яковенко Кирило, група БІКСб-12-540
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox,
    QToolBar, QStatusBar, QLabel
)
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Головне вікно текстового редактора на базі QMainWindow."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ЛБ №4, Завдання 3 — Текстовий редактор | Яковенко БІКСб-12-540")
        self.setMinimumSize(700, 500)

        self.current_file = None  # Поточний відкритий файл

        # === Центральний віджет ===
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Почніть вводити текст тут...")
        self.text_edit.setToolTip("Основна текстова область редактора")
        self.setCentralWidget(self.text_edit)

        # Сигнал для оновлення рядка стану при зміні тексту
        self.text_edit.textChanged.connect(self.update_status)

        # === Рядок стану (statusBar) ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.chars_label = QLabel("Символів: 0")
        self.words_label = QLabel("Слів: 0")
        self.lines_label = QLabel("Рядків: 0")
        self.file_label = QLabel("Файл: не відкрито")

        self.status_bar.addWidget(self.file_label)
        self.status_bar.addPermanentWidget(self.chars_label)
        self.status_bar.addPermanentWidget(self.words_label)
        self.status_bar.addPermanentWidget(self.lines_label)

        self.status_bar.showMessage("Готовий до роботи", 3000)

        # === Меню ===
        self._create_menus()

        # === Панель інструментів ===
        self._create_toolbar()

    def _create_menus(self):
        """Створює меню додатка."""
        menubar = self.menuBar()

        # --- Меню "Файл" ---
        file_menu = menubar.addMenu("&Файл")

        # Новий файл (Ctrl+N)
        new_action = QAction("&Новий", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setToolTip("Створити новий документ (Ctrl+N)")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # Відкрити файл (Ctrl+O)
        open_action = QAction("&Відкрити...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setToolTip("Відкрити файл з диску (Ctrl+O)")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Зберегти файл (Ctrl+S)
        save_action = QAction("&Зберегти", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setToolTip("Зберегти файл (Ctrl+S)")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # Вихід (Ctrl+Q)
        exit_action = QAction("В&ихід", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setToolTip("Закрити програму (Ctrl+Q)")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Меню "Редагування" ---
        edit_menu = menubar.addMenu("&Редагування")

        select_all_action = QAction("Виділити &все", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        clear_action = QAction("&Очистити", self)
        clear_action.setShortcut(QKeySequence("Ctrl+L"))
        clear_action.triggered.connect(self.text_edit.clear)
        edit_menu.addAction(clear_action)

        # --- Меню "Довідка" ---
        help_menu = menubar.addMenu("&Довідка")

        about_action = QAction("&Про програму", self)
        about_action.setToolTip("Інформація про програму")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        help_action = QAction("&Довідка", self)
        help_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def _create_toolbar(self):
        """Створює панель інструментів з кнопками швидкого доступу."""
        toolbar = QToolBar("Основна панель")
        toolbar.setMovable(False)  # Заборонити переміщення панелі
        self.addToolBar(toolbar)

        # Кнопка "Новий"
        new_btn = QAction("📄 Новий", self)
        new_btn.setToolTip("Створити новий документ")
        new_btn.triggered.connect(self.new_file)
        toolbar.addAction(new_btn)

        # Кнопка "Відкрити"
        open_btn = QAction("📂 Відкрити", self)
        open_btn.setToolTip("Відкрити файл з диску")
        open_btn.triggered.connect(self.open_file)
        toolbar.addAction(open_btn)

        # Кнопка "Зберегти"
        save_btn = QAction("💾 Зберегти", self)
        save_btn.setToolTip("Зберегти файл")
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)

        toolbar.addSeparator()

        # Кнопка "Очистити"
        clear_btn = QAction("🗑 Очистити", self)
        clear_btn.setToolTip("Очистити текстове поле")
        clear_btn.triggered.connect(self.text_edit.clear)
        toolbar.addAction(clear_btn)

        toolbar.addSeparator()

        # Кнопка "Про програму"
        about_btn = QAction("ℹ Про програму", self)
        about_btn.setToolTip("Інформація про програму")
        about_btn.triggered.connect(self.show_about)
        toolbar.addAction(about_btn)

    # === Обробники дій меню ===

    def new_file(self):
        """Створення нового документа."""
        if self.text_edit.toPlainText().strip():
            reply = QMessageBox.question(
                self, "Новий файл",
                "Зберегти зміни перед створенням нового файла?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        self.text_edit.clear()
        self.current_file = None
        self.file_label.setText("Файл: не відкрито")
        self.status_bar.showMessage("Створено новий документ", 3000)
        self.update_status()

    def open_file(self):
        """Відкриття файлу через QFileDialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Відкрити файл",
            "",
            "Текстові файли (*.txt);;Всі файли (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.current_file = file_path
                self.file_label.setText(f"Файл: {file_path}")
                self.status_bar.showMessage(f"Відкрито файл: {file_path}", 3000)
                self.update_status()
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити файл:\n{e}")

    def save_file(self):
        """Збереження файлу через QFileDialog."""
        if self.current_file:
            file_path = self.current_file
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Зберегти файл",
                "",
                "Текстові файли (*.txt);;Всі файли (*)"
            )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.current_file = file_path
                self.file_label.setText(f"Файл: {file_path}")
                self.status_bar.showMessage(f"Збережено: {file_path}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл:\n{e}")

    def show_about(self):
        """Показ діалогу QMessageBox.about."""
        QMessageBox.about(
            self,
            "Про програму",
            "<h3>Текстовий редактор</h3>"
            "<p>Лабораторна робота №4, Завдання 3</p>"
            "<p><b>Виконав:</b> Яковенко Кирило, група БІКСб-12-540</p>"
            "<p><b>Дисципліна:</b> Програмування</p>"
            "<p>Додаток демонструє роботу з QMainWindow, меню, "
            "панеллю інструментів та рядком стану в PyQt6.</p>"
        )

    def show_help(self):
        """Показ довідки."""
        QMessageBox.information(
            self, "Довідка",
            "<h3>Як користуватися редактором</h3>"
            "<ul>"
            "<li><b>Ctrl+N</b> — створити новий документ</li>"
            "<li><b>Ctrl+O</b> — відкрити файл</li>"
            "<li><b>Ctrl+S</b> — зберегти файл</li>"
            "<li><b>Ctrl+Q</b> — вийти з програми</li>"
            "<li><b>Ctrl+L</b> — очистити текст</li>"
            "</ul>"
        )

    def update_status(self):
        """Оновлення рядка стану: кількість символів, слів, рядків."""
        text = self.text_edit.toPlainText()
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        lines = text.count('\n') + 1 if text else 0

        self.chars_label.setText(f"Символів: {chars}")
        self.words_label.setText(f"Слів: {words}")
        self.lines_label.setText(f"Рядків: {lines}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()