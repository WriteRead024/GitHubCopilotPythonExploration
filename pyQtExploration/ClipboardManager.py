# started 6/4/2024
# file menu improvements 12/3/2024
# timestamp column 6/30/2025
# Rich W.
# with
# GitHub Copilot
# MSL.l


import sys
import os
import json
import glob
import time
# silences a console warning
os.environ["XDG_SESSION_TYPE"] = "xcb"
# os.environ["QT_QPA_PLATFORM"] = "wayland"

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QWidget,
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
        self.clipboard_data = []  # tuples formatted (timestamp, text)
        self.last_clipboard_text = None

        self.table = QTableWidget(0, 4)  # setup datagrid columns
        self.table.setHorizontalHeaderLabels(['Timestamp', 'Clipboard Text', 'Copy', 'Remove'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Timestamp
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Clipboard Text
        header.setSectionResizeMode(2, QHeaderView.Fixed)             # Copy
        header.setSectionResizeMode(3, QHeaderView.Fixed)             # Remove
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
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
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.clipboard_data.append((timestamp, text))
            self.add_item_to_datagrid(timestamp, text)

    def add_item_to_datagrid(self, timestamp, text):
        self.table.insertRow(0)
        timestamp_item = QTableWidgetItem(timestamp)
        timestamp_item.setFlags(timestamp_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(0, 0, timestamp_item)

        text_item = QTableWidgetItem(text)
        text_item.setFlags(text_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(0, 1, text_item)

        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(text))
        self.table.setCellWidget(0, 2, copy_button)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_from_list(timestamp, text))
        self.table.setCellWidget(0, 3, remove_button)

    def copy_to_clipboard(self, text):
        self.last_clipboard_text = text
        self.clipboard.setText(text)

    def remove_from_list(self, timestamp, text):
        try:
            self.clipboard_data.remove((timestamp, text))
        except ValueError:
            pass
        for i in range(self.table.rowCount()):
            if (self.table.item(i, 0).text() == timestamp and
                self.table.item(i, 1).text() == text):
                self.table.removeRow(i)
                break

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        save_action = QAction('Save', self)
        load_action = QAction('Load', self)
        clear_history_action = QAction('Clear Clipboard History', self)  # New action
        file_menu.addAction(clear_history_action)  # Add to menu
        file_menu.addAction(load_action)
        file_menu.addAction(save_action)

        save_action.triggered.connect(self.save_clipboard_data)
        load_action.triggered.connect(self.load_clipboard_data)
        clear_history_action.triggered.connect(self.clear_clipboard_history)  # Connect action

    def clear_clipboard_history(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Clear")
        msg_box.setText("Are you sure you want to clear the clipboard history?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        msg_box.addButton(yes_button, QMessageBox.YesRole)
        msg_box.addButton(no_button, QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        reply = msg_box.exec_()
        if reply == 0:  # Yes button is the first added
            self.clipboard_data.clear()
            self.table.setRowCount(0)
            if not silent_command_line:
                print("Clipboard history cleared.")

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
            file.write("ClipboardManager clipboard data version 0.2\n")
            json.dump(self.clipboard_data, file)

    def load_clipboard_data(self):
        try:
            files = glob.glob('clipboard_data_*.json')
            if files:
                latest_file = max(files, key=lambda f: int(f.split('_')[-1].split('.')[0]))
                with open(latest_file, 'r') as file:
                    first_line = file.readline()
                    if first_line.strip() == "ClipboardManager clipboard data version 0.2":
                        # Version 0.2: expects list of (timestamp, text) tuples
                        self.clipboard_data = json.load(file)
                    else:
                        # Version 0.1: expects list of strings, add current timestamp
                        # CODE COMMENT: Version 0.1 compatibility - add current timestamp to each entry
                        file.seek(0)  # rewind to start
                        v0p1_data = json.load(file)
                        now = time.strftime("%Y-%m-%d %H:%M:%S")
                        self.clipboard_data = [(now, text) for text in v0p1_data]
                    self.table.setRowCount(0)
                    for timestamp, text in self.clipboard_data:
                        self.add_item_to_datagrid(timestamp, text)
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
            item_text = self.table.item(i, 1).text().lower()  # Now column 1 is Clipboard Text
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

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Exit")
        msg_box.setText("Are you sure you want to exit?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        msg_box.addButton(yes_button, QMessageBox.YesRole)
        msg_box.addButton(no_button, QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        reply = msg_box.exec_()
        if reply == 0:  # Yes button is the first added
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
