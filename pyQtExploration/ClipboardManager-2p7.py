# backported version of ClipboardManager.py
# original started 6/4/2024
# Ported by Copilot, Oct. 6, 2025 from Python 3.13 to 
# Python 2.7 / PyQt4 
# (https://github.com/copilot/c/106c7d44-9893-480f-9626-f46bfa2b135e)
# addl. history:
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

os.environ["XDG_SESSION_TYPE"] = "xcb"

from PyQt4.QtGui import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QAction,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QPalette,
    QColor,
)
from PyQt4.QtCore import Qt, QTimer

silent_command_line = False
if "--silent" in sys.argv:
    silent_command_line = True
elif "-s" in sys.argv:
    silent_command_line = True

if not silent_command_line:
    print "Starting Clipboard Manager..."
    print time.strftime("%X %x %Z")

class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None, search_function=None):
        QLineEdit.__init__(self, parent)
        self.search_function = search_function

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            if self.search_function:
                self.search_function()
            elif not silent_command_line:
                print "ERROR WARNING: No search function provided."
        else:
            QLineEdit.keyPressEvent(self, event)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.clipboard = QApplication.clipboard()
        self.clipboard_data = []  # tuples (timestamp, text)
        self.last_clipboard_text = None

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Timestamp', 'Clipboard Text', 'Copy', 'Remove'])
        header = self.table.horizontalHeader()
        header.setResizeMode(0, QHeaderView.ResizeToContents)
        header.setResizeMode(1, QHeaderView.Stretch)
        header.setResizeMode(2, QHeaderView.Fixed)
        header.setResizeMode(3, QHeaderView.Fixed)
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
        self.timer.start(1000)

        self.init_menu_bar()

        self.resize(425, 200)

    def check_clipboard(self):
        text = unicode(self.clipboard.text())
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
        # Use lambda default argument trick for late binding
        copy_button.clicked.connect(lambda _, t=text: self.copy_to_clipboard(t))
        self.table.setCellWidget(0, 2, copy_button)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda _, ts=timestamp, t=text: self.remove_from_list(ts, t))
        self.table.setCellWidget(0, 3, remove_button)

    def copy_to_clipboard(self, text):
        self.last_clipboard_text = text
        self.clipboard.setText(text)

    def remove_from_list(self, timestamp, text):
        try:
            self.clipboard_data.remove((timestamp, text))
        except ValueError:
            pass
        for i in xrange(self.table.rowCount()):
            if (unicode(self.table.item(i, 0).text()) == timestamp and
                unicode(self.table.item(i, 1).text()) == text):
                self.table.removeRow(i)
                break

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        save_action = QAction('Save', self)
        load_action = QAction('Load', self)
        clear_history_action = QAction('Clear Clipboard History', self)
        file_menu.addAction(clear_history_action)
        file_menu.addAction(load_action)
        file_menu.addAction(save_action)

        save_action.triggered.connect(self.save_clipboard_data)
        load_action.triggered.connect(self.load_clipboard_data)
        clear_history_action.triggered.connect(self.clear_clipboard_history)

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
        if reply == 0:
            self.clipboard_data = []
            self.table.setRowCount(0)
            if not silent_command_line:
                print "Clipboard history cleared."

    def save_clipboard_data(self):
        files = glob.glob('clipboard_data_*.json')
        if files:
            latest_file = max(files, key=os.path.getctime)
            try:
                latest_index = int(latest_file.split('_')[-1].split('.')[0])
                new_index = latest_index + 1
            except Exception:
                new_index = 1
        else:
            new_index = 1
        new_filename = 'clipboard_data_{}.json'.format(new_index)
        with open(new_filename, 'w') as file:
            file.write("ClipboardManager clipboard data version 0.2\n")
            json.dump(self.clipboard_data, file)
            if not silent_command_line:
                print "saved to '{}'".format(new_filename)

    def load_clipboard_data(self):
        try:
            files = glob.glob('clipboard_data_*.json')
            if files:
                def extract_index(f):
                    try:
                        return int(f.split('_')[-1].split('.')[0])
                    except Exception:
                        return 0
                latest_file = max(files, key=extract_index)
                with open(latest_file, 'r') as file:
                    first_line = file.readline()
                    if first_line.strip() == "ClipboardManager clipboard data version 0.2":
                        self.clipboard_data = json.load(file)
                    else:
                        file.seek(0)
                        v0p1_data = json.load(file)
                        now = time.strftime("%Y-%m-%d %H:%M:%S")
                        self.clipboard_data = [(now, text) for text in v0p1_data]
                    self.table.setRowCount(0)
                    for timestamp, text in self.clipboard_data:
                        self.add_item_to_datagrid(timestamp, text)
                    if not silent_command_line:
                        print "loaded from '{}'".format(latest_file)
            else:
                if not silent_command_line:
                    print "ERROR: No clipboard data files found."
        except IOError:
            if not silent_command_line:
                print "ERROR: Clipboard data file not found."
        except ValueError:
            if not silent_command_line:
                print "ERROR: Failed to decode JSON from clipboard data file."
        except Exception as e:
            if not silent_command_line:
                print "ERROR: load_clipboard_data failed with exception: {}".format(e)

    def search_clipboard(self):
        search_text = unicode(self.search_input.text()).lower()
        for i in xrange(self.table.rowCount()):
            item_text = unicode(self.table.item(i, 1).text()).lower()
            self.table.setRowHidden(i, search_text not in item_text)
        self.update_search_layout_color(bool(search_text))

    def clear_search(self):
        self.search_input.clear()
        for i in xrange(self.table.rowCount()):
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
        msg_box.setText("Are you sure you want to exit Clipboard Manager?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        msg_box.addButton(yes_button, QMessageBox.YesRole)
        msg_box.addButton(no_button, QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        reply = msg_box.exec_()
        if reply == 0:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
