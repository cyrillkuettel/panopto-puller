import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QDir


class DialogApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        self.btn_cookies = QPushButton('Get Text File')
        self.btn_cookies.clicked.connect(self.get_text_file)

        self.labelImage = QLabel()
        self.textEditor = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.labelImage)
        layout.addWidget(self.btn_cookies)
        layout.addWidget(self.textEditor)
        self.setLayout(layout)

    def get_text_file(self):

        filters = ["Text Files (*.txt)"]
        # filters = []
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setWindowTitle("Open cookies.txt...")
        dialog.setNameFilters(filters)

        if dialog.exec():
            file_name = dialog.selectedFiles()

            if file_name[0].endswith('.txt'):
                with open(file_name[0], 'r') as f:
                    data = f.read()
                    self.textEditor.setPlainText(data)
                    f.close()
            else:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = DialogApp()
    demo.show()

    sys.exit(app.exec())
