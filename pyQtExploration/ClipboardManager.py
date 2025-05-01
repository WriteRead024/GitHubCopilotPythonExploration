# started 6/4/2024
# file menu improvements 12/3/2024
# Rich W.
# with
# GitHub Copilot
# MSL.l


import sys
import os
import json
import glob
# silences a console warning
os.environ["XDG_SESSION_TYPE"] = "xcb"
# os.environ["QT_QPA_PLATFORM"] = "wayland"

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QMenuBar,
    QAction,
    QLineEdit,
    QHBoxLayout,
)
from PyQt5.Qt import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QPalette, QColor


silent_command_line = False
if "--silent" in sys.argv: silent_command_line = True
elif "-s" in sys.argv: silent_command_line = True


if not silent_command_line:
    print("Starting Clipboard Manager...")
    import time
    print(time.strftime("%X %x %Z"))


class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None, search_function=None):
        super(SearchLineEdit, self).__init__(parent)
        self.search_function = search_function

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.search_function:
                self.search_function()
            elif not silent_command_line:
                print("ERROR WARNING: No search function provided.")
        else:
            super(SearchLineEdit, self).keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.clipboard = QApplication.clipboard()
        self.clipboard_data = []
        self.last_clipboard_text = None

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(['Clipboard Text', 'Copy', 'Remove'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.search_input = SearchLineEdit(search_function=self.search_clipboard)
        self.search_input.setPlaceholderText("Search clipboard...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_clipboard)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_search)

        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addLayout(self.search_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.default_search_layout_color = self.palette().color(QPalette.Window)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)  # Check every second

        self.init_menu_bar()

        self.resize(425, 200)

    def check_clipboard(self):
        text = self.clipboard.text()
        if text and text != self.last_clipboard_text:
            self.last_clipboard_text = text
            self.clipboard_data.append(text)
            self.add_item_to_datagrid(text)

    def add_item_to_datagrid(self, text):
        self.table.insertRow(0)
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item not editable
        self.table.setItem(0, 0, item)

        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(text))
        self.table.setCellWidget(0, 1, copy_button)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_from_list(text))
        self.table.setCellWidget(0, 2, remove_button)

    def copy_to_clipboard(self, text):
        self.last_clipboard_text = text
        self.clipboard.setText(text)

    def remove_from_list(self, text):
        self.clipboard_data.remove(text)
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).text() == text:
                self.table.removeRow(i)
                break

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        save_action = QAction('Save', self)
        load_action = QAction('Load', self)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)        

        save_action.triggered.connect(self.save_clipboard_data)
        load_action.triggered.connect(self.load_clipboard_data)

    def save_clipboard_data(self):
        files = glob.glob('clipboard_data_*.json')
        if files:
            latest_file = max(files, key=os.path.getctime)
            latest_index = int(latest_file.split('_')[-1].split('.')[0])
            new_index = latest_index + 1
        else:
            new_index = 1
        new_filename = f'clipboard_data_{new_index}.json'
        with open(new_filename, 'w') as file:
            json.dump(self.clipboard_data, file)

    def load_clipboard_data(self):
        try:
            files = glob.glob('clipboard_data_*.json')
            if files:
                latest_file = max(files, key=lambda f: int(f.split('_')[-1].split('.')[0]))
                with open(latest_file, 'r') as file:
                    self.clipboard_data = json.load(file)
                    self.table.setRowCount(0)
                    for text in self.clipboard_data:
                        self.add_item_to_datagrid(text)
            else:
                if not silent_command_line:
                    print("ERROR: No clipboard data files found.")
        except FileNotFoundError:
            if not silent_command_line:
                print("ERROR: Clipboard data file not found.")
        except json.JSONDecodeError:
            if not silent_command_line:
                print("ERROR: Failed to decode JSON from clipboard data file.")
        except Exception as e:
            if not silent_command_line:
                print(f"ERROR: load_clipboard_data failed with exception: {e}")

    def search_clipboard(self):
        search_text = self.search_input.text().lower()
        for i in range(self.table.rowCount()):
            item_text = self.table.item(i, 0).text().lower()
            self.table.setRowHidden(i, search_text not in item_text)
        self.update_search_layout_color(bool(search_text))

    def clear_search(self):
        self.search_input.clear()
        for i in range(self.table.rowCount()):
            self.table.setRowHidden(i, False)
        self.update_search_layout_color(False)

    def update_search_layout_color(self, is_filtered):
        color = QColor(173, 216, 230) if is_filtered else self.default_search_layout_color
        palette = self.search_input.palette()
        palette.setColor(QPalette.Base, color)
        self.search_input.setPalette(palette)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
