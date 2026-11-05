"""Лабораторна робота №4, Завдання 4.
Виконав: Яковенко Кирило, група БІКСб-12-540
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QSpinBox, QLineEdit, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QGroupBox, QSplitter, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt


# ============================================================
# КОМПОНЕНТ 1: Панель фільтрів
# ============================================================
class FilterPanel(QWidget):
    """Компонент введення фільтрів для каталогу товарів.

    Кастомні сигнали:
        filter_changed(str, int, str) — випромінюється при зміні будь-якого
            поля фільтра. Параметри: (категорія, мін_ціна, текст_пошуку).
        filters_cleared() — випромінюється при натисканні кнопки "Скинути".
    """

    # Сигнал зміни фільтрів: (категорія, мін_ціна, пошук)
    filter_changed = pyqtSignal(str, int, str)

    # Сигнал скидання фільтрів (без параметрів)
    filters_cleared = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Категорія
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Категорія:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Всі", "Електроніка", "Одяг", "Книги", "Їжа"])
        self.category_combo.setCurrentIndex(0)
        cat_layout.addWidget(self.category_combo)
        layout.addLayout(cat_layout)

        # Мінімальна ціна
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Мін. ціна (грн):"))
        self.min_price_spin = QSpinBox()
        self.min_price_spin.setRange(0, 10000)
        self.min_price_spin.setValue(0)
        self.min_price_spin.setSuffix(" грн")
        price_layout.addWidget(self.min_price_spin)
        layout.addLayout(price_layout)

        # Пошук за назвою
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Пошук:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть назву товару...")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Кнопка скидання
        self.reset_btn = QPushButton("Скинути фільтри")
        self.reset_btn.clicked.connect(self._on_reset)
        layout.addWidget(self.reset_btn)

        # З'єднання внутрішніх сигналів → випромінювання кастомного
        self.category_combo.currentTextChanged.connect(self._emit_filter)
        self.min_price_spin.valueChanged.connect(self._emit_filter)
        self.search_input.textChanged.connect(self._emit_filter)

    def _emit_filter(self):
        """Випромінює сигнал filter_changed з поточними значеннями."""
        category = self.category_combo.currentText()
        min_price = self.min_price_spin.value()
        search_text = self.search_input.text()
        self.filter_changed.emit(category, min_price, search_text)

    def _on_reset(self):
        """Скидає всі поля до початкових значень."""
        self.category_combo.setCurrentIndex(0)
        self.min_price_spin.setValue(0)
        self.search_input.clear()
        self.filters_cleared.emit()


# ============================================================
# КОМПОНЕНТ 2: Панель результатів
# ============================================================
class ResultsPanel(QWidget):
    """Компонент відображення відфільтрованих товарів.

    Кастомні сигнали:
        item_selected(str, int) — випромінюється при кліку на товар.
            Параметри: (назва, ціна).
        items_count_changed(int) — випромінюється при зміні кількості
            товарів у списку. Параметр: нова кількість.
    """

    # Сигнал вибору товару: (назва, ціна)
    item_selected = pyqtSignal(str, int)

    # Сигнал зміни кількості товарів: (кількість)
    items_count_changed = pyqtSignal(int)

    # Тестові дані каталогу
    CATALOG = [
        ("Ноутбук Dell", "Електроніка", 25000),
        ("Смартфон Samsung", "Електроніка", 15000),
        ("Навушники Sony", "Електроніка", 3500),
        ("Футболка Adidas", "Одяг", 800),
        ("Джинси Levi's", "Одяг", 2200),
        ("Куртка зимowa", "Одяг", 4500),
        ("Python для початківців", "Книги", 450),
        ("Clean Code", "Книги", 900),
        ("Яблуко", "Їжа", 50),
        ("Хліб", "Їжа", 30),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._populate_catalog()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Результати пошуку:"))

        self.list_widget = QListWidget()
        self.list_widget.setToolTip("Клацніть на товар для перегляду деталей")
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)

        self.count_label = QLabel("Знайдено: 0 товарів")
        layout.addWidget(self.count_label)

    def _populate_catalog(self):
        """Заповнює список початковими даними."""
        self.list_widget.clear()
        for name, category, price in self.CATALOG:
            item = QListWidgetItem(f"{name} — {price} грн [{category}]")
            item.setData(Qt.ItemDataRole.UserRole, (name, category, price))
            self.list_widget.addItem(item)
        self._update_count()

    def apply_filters(self, category: str, min_price: int, search_text: str):
        """Застосовує фільтри до каталогу (слот для signal filter_changed)."""
        self.list_widget.clear()
        search_lower = search_text.lower()

        for name, cat, price in self.CATALOG:
            # Перевірка категорії
            if category != "Всі" and cat != category:
                continue
            # Перевірка мінімальної ціни
            if price < min_price:
                continue
            # Перевірка пошуку за назвою
            if search_lower and search_lower not in name.lower():
                continue

            item = QListWidgetItem(f"{name} — {price} грн [{cat}]")
            item.setData(Qt.ItemDataRole.UserRole, (name, cat, price))
            self.list_widget.addItem(item)

        self._update_count()

    def _on_item_clicked(self, item: QListWidgetItem):
        """Обробник кліку на товар — випромінює item_selected."""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            name, category, price = data
            self.item_selected.emit(name, price)

    def _update_count(self):
        """Оновлює лічильник та випромінює items_count_changed."""
        count = self.list_widget.count()
        self.count_label.setText(f"Знайдено: {count} товарів")
        self.items_count_changed.emit(count)


# ============================================================
# ГОЛОВНЕ ВІКНО: з'єднує компоненти через сигнали
# ============================================================
class MainWindow(QMainWindow):
    """Головне вікно, що з'єднує FilterPanel та ResultsPanel через сигнали."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ЛБ №4, Завдання 4 — Кастомні сигнали | Яковенко БІКСб-12-540")
        self.setMinimumSize(700, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # === Створення компонентів ===
        self.filter_panel = FilterPanel()
        self.results_panel = ResultsPanel()

        # === З'ЄДНАННЯ СИГНАЛІВ МІЖ КОМПОНЕНТАМИ (зовні!) ===

        # FilterPanel.filter_changed → ResultsPanel.apply_filters
        self.filter_panel.filter_changed.connect(self.results_panel.apply_filters)

        # ResultsPanel.item_selected → MainWindow.show_item_info
        self.results_panel.item_selected.connect(self.show_item_info)

        # ResultsPanel.items_count_changed → MainWindow.update_status
        self.results_panel.items_count_changed.connect(self.update_status)

        # FilterPanel.filters_cleared → MainWindow.on_filters_cleared
        self.filter_panel.filters_cleared.connect(self.on_filters_cleared)

        # === Панель інформації про вибраний товар ===
        info_group = QGroupBox("Інформація про вибраний товар")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("Оберіть товар зі списку...")
        self.info_label.setStyleSheet("font-size: 14px; padding: 10px;")
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)

        # === Панель керування сигналами (демонстрація disconnect/blockSignals) ===
        control_group = QGroupBox("Керування сигналами")
        control_layout = QHBoxLayout()

        self.block_btn = QPushButton("Блокувати сигнали фільтрів")
        self.block_btn.setToolTip("Блокує signal filter_changed (blockSignals)")
        self.block_btn.clicked.connect(self.toggle_block_signals)
        control_layout.addWidget(self.block_btn)

        self.disconnect_btn = QPushButton("Від'єднати фільтри від результатів")
        self.disconnect_btn.setToolTip("Від'єднує signal→slot (disconnect)")
        self.disconnect_btn.clicked.connect(self.disconnect_filters)
        control_layout.addWidget(self.disconnect_btn)

        self.reconnect_btn = QPushButton("Під'єднати фільтри знову")
        self.reconnect_btn.setToolTip("Повторно з'єднує signal→slot")
        self.reconnect_btn.clicked.connect(self.reconnect_filters)
        self.reconnect_btn.setEnabled(False)
        control_layout.addWidget(self.reconnect_btn)

        control_group.setLayout(control_layout)

        # === Додавання компонентів у головний layout ===
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.filter_panel)
        splitter.addWidget(self.results_panel)

        main_layout.addWidget(splitter)
        main_layout.addWidget(info_group)
        main_layout.addWidget(control_group)

        # === Рядок стану ===
        self.statusBar().showMessage("Готовий до роботи")

    # === Слоти головного вікна ===

    def show_item_info(self, name: str, price: int):
        """Слот: показує інформацію про вибраний товар."""
        self.info_label.setText(f"🛒 <b>{name}</b> — ціна: {price} грн")
        self.statusBar().showMessage(f"Вибрано товар: {name}", 3000)

    def update_status(self, count: int):
        """Слот: оновлює рядок стану при зміні кількості товарів."""
        self.statusBar().showMessage(f"У списку: {count} товарів", 2000)

    def on_filters_cleared(self):
        """Слот: обробляє скидання фільтрів."""
        self.info_label.setText("Фільтри скинуто. Оберіть товар зі списку...")
        self.statusBar().showMessage("Фільтри скинуто", 2000)

    # === Демонстрація blockSignals ===

    def toggle_block_signals(self):
        """Блокує/розблоковує сигнали FilterPanel."""
        is_blocked = self.filter_panel.blockSignals(True)
        if not is_blocked:
            # Щойно заблокували
            self.block_btn.setText("Розблокувати сигнали фільтрів")
            self.block_btn.setStyleSheet("background-color: #ffcccc;")
            self.statusBar().showMessage("Сигнали фільтрів ЗАБЛОКОВАНІ — зміни не впливають на результати", 5000)
        else:
            # Розблокували
            self.filter_panel.blockSignals(False)
            self.block_btn.setText("Блокувати сигнали фільтрів")
            self.block_btn.setStyleSheet("")
            self.statusBar().showMessage("Сигнали фільтрів РОЗБЛОКОВАНІ", 3000)
            # Примусово оновлюємо результати поточними значеннями
            self.filter_panel._emit_filter()

    # === Демонстрація disconnect ===

    def disconnect_filters(self):
        """Від'єднує сигнал filter_changed від слота apply_filters."""
        try:
            self.filter_panel.filter_changed.disconnect(self.results_panel.apply_filters)
            self.disconnect_btn.setEnabled(False)
            self.reconnect_btn.setEnabled(True)
            self.statusBar().showMessage("Фільтри ВІД'ЄДНАНІ від результатів", 5000)
            QMessageBox.information(
                self, "Від'єднано",
                "Сигнал filter_changed більше не з'єднаний зі слотом apply_filters.\n"
                "Зміни у фільтрах не впливатимуть на список результатів."
            )
        except TypeError:
            # Вже від'єднано
            pass

    def reconnect_filters(self):
        """Повторно з'єднує сигнал filter_changed зі слотом apply_filters."""
        self.filter_panel.filter_changed.connect(self.results_panel.apply_filters)
        self.disconnect_btn.setEnabled(True)
        self.reconnect_btn.setEnabled(False)
        self.statusBar().showMessage("Фільтри ПІД'ЄДНАНІ до результатів", 3000)
        # Примусово оновлюємо
        self.filter_panel._emit_filter()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()