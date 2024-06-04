# started 6/4/2024
# Rich W.
# with
# GitHub Copilot


import sys
import os
# silences a console warning
os.environ["XDG_SESSION_TYPE"] = "xcb"

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

    def check_clipboard(self):
        text = self.clipboard.text()
        if text and text != self.last_clipboard_text:
            self.last_clipboard_text = text
            self.clipboard_data.append(text)
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


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
