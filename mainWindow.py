import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QPushButton, \
    QHBoxLayout
import psycopg2


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Список материалов')

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Поиск по материалам...")
        self.search_edit.textChanged.connect(self.filter_table)

        hbox.addWidget(self.search_edit)
        sort_button = QPushButton("Сортировка", self)
        hbox.addWidget(sort_button)
        filter_button = QPushButton("Фильтрация", self)
        hbox.addWidget(filter_button)

        vbox.addLayout(hbox)
        self.table_widget = QTableWidget(self)
        vbox.addWidget(self.table_widget)
        self.setLayout(vbox)

        self.original_data = []
        self.load_data()

    def load_data(self):
        try:
            connection = psycopg2.connect(
                dbname='zachet123',
                user='postgres',
                password='artem',
                host='localhost',
                port='5432'
            )
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM materials")
            rows = cursor.fetchall()

            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(3)
            self.table_widget.setHorizontalHeaderLabels(['ID', 'Название', 'Количество'])

            self.original_data = rows.copy()

            for row_index, row_data in enumerate(rows):
                for column_index, item in enumerate(row_data):
                    self.table_widget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться к базе данных: {str(e)}")

        finally:
            if connection:
                cursor.close()
                connection.close()

    def filter_table(self, text):
        """поиск по введенному тексту"""
        if not hasattr(self, 'original_data'):
            return

        if not text.strip():
            self.restore_original_data()
            return

        current_rows = []
        for row in range(self.table_widget.rowCount()):
            row_items = [self.table_widget.item(row, col).text().lower()
                         for col in range(self.table_widget.columnCount())]
            current_rows.append(row_items)

        filtered_rows = []
        search_text = text.lower()
        for row in current_rows:
            if any(search_text in cell for cell in row):
                filtered_rows.append(row)

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(filtered_rows))

        for row_idx, row_data in enumerate(filtered_rows):
            for col_idx, item in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(item))

    def restore_original_data(self):
        """возращает исходные данные из бд"""
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.original_data))
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Название', 'Количество'])

        for row_idx, row_data in enumerate(self.original_data):
            for col_idx, item in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))


