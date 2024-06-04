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

        self.table = QTableWidget(0, 1)
        self.table.setHorizontalHeaderLabels(['Clipboard Text'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.copy_button = QPushButton("Copy to Clipboard")
        self.remove_button = QPushButton("Remove from List")

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.remove_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.remove_button.clicked.connect(self.remove_from_list)

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
            # Make the grid row item not editable
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(0, 0, item)

    def copy_to_clipboard(self):
        row = self.table.currentRow()
        if row != -1:
            self.last_clipboard_text = self.clipboard_data[row]
            self.clipboard.setText(self.last_clipboard_text)

    def remove_from_list(self):
        row = self.table.currentRow()
        if row != -1:
            self.table.removeRow(row)
            del self.clipboard_data[row]


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
