
# started 6/4/2024
# Rich W.
# with
# GitHub Copilot

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
from PyQt5.Qt import QTimer, QClipboard
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.clipboard = QApplication.clipboard()
        self.clipboard_data = []
        self.last_clipboard_text = None

        self.table = QTableWidget(0, 1)
        self.copy_button = QPushButton('Copy to Clipboard')
        self.remove_button = QPushButton('Remove from List')

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
            self.table.setItem(0, 0, QTableWidgetItem(text))

    def copy_to_clipboard(self):
        row = self.table.currentRow()
        if row != -1:
            
            self.clipboard.setText(self.clipboard_data[row])

    def remove_from_list(self):
        row = self.table.currentRow()
        if row != -1:
            self.table.removeRow(row)
            del self.clipboard_data[row]

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())