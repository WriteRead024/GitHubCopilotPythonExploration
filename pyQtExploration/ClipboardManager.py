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
)
from PyQt5.Qt import QTimer
from PyQt5.QtCore import Qt



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

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
                print("ERROR: No clipboard data files found.")
        except FileNotFoundError:
            print("ERROR: Clipboard data file not found.")
        except json.JSONDecodeError:
            print("ERROR: Failed to decode JSON from clipboard data file.")
        except Exception as e:
            print(f"ERROR: load_clipboard_data failed with exception: {e}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
