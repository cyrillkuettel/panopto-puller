import os
import sys

import yt_dlp
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, QDir
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QProgressBar, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.label_url = None
        self.thread = QThread()
        self.thread.started.connect(self.download)

        self.createWindow()
        self.createWidgetsAndSetLayout()

    def createWindow(self):
        global app

        self.setWindowTitle('Panopto Downloader')
        self.setWindowIcon(QIcon('icons:flat.png'))

        width = int(app.primaryScreen().size().width() * 0.42)
        height = int(app.primaryScreen().size().height() * 0.089)
        self.setFixedSize(width, height)

        frame = self.frameGeometry()
        frame.moveCenter(app.primaryScreen().availableGeometry().center())
        self.move(frame.topLeft())

    def createWidgetsAndSetLayout(self):  # create widgets and set layout
        global application_path

        # v box init
        v_box = QVBoxLayout()

        # line 1
        label_url = QLabel('URL', self)
        self.le_url = QLineEdit()
        btn_cookies = QPushButton()
        btn_cookies.setIcon(QIcon('icons:cookies.ico'))
        btn_file_path = QPushButton()
        btn_file_path.setIcon(QIcon('icons:choose-file-icon-16.png'))

        btn_file_path.clicked.connect(self.chooseFilePath)
        self.le_file_path = QLineEdit(application_path)
        self.le_file_path.setMaximumWidth(200)

        self.btn_download = QPushButton('Download', self)
        self.btn_download.clicked.connect(self.onClickDownloadButton)

        h_box1 = QHBoxLayout()
        h_box1.addWidget(label_url)
        h_box1.addWidget(self.le_url)
        h_box1.addWidget(btn_cookies)
        h_box1.addWidget(self.le_file_path)
        h_box1.addWidget(btn_file_path)
        h_box1.addWidget(self.btn_download)

        v_box.addLayout(h_box1)

        # line 2
        h_box2 = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        h_box2.addWidget(self.progress_bar)
        v_box.addLayout(h_box2)
        v_box.addStretch()

        # line 3 (printing status information)
        h_box3 = QHBoxLayout()
        self.label_url = QLabel('', self)
        self.label_url.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_box3.addWidget(self.label_url)
        v_box.addLayout(h_box3)


        self.setLayout(v_box)

    def chooseFilePath(self):
        file_path = QFileDialog.getExistingDirectory()
        self.le_file_path.setText(file_path)

    def onClickDownloadButton(self):
        self.thread.start()

    def download(self):
        ydl_opts = {'outtmpl': self.le_file_path.text() + '/%(title)s.%(ext)s', 'progress_hooks': [self.pHook],
                    'quiet': True, 'no_warnings': True, 'nocheckcertificate': True, 'format': 'best'}

        try:
            print(f'download from {self.le_url.text()}')
            self.btn_download.setEnabled(False)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.le_url.text()])
        except yt_dlp.utils.DownloadError or Exception as e:
            self.progress_bar.setValue(0)
        finally:
            self.btn_download.setEnabled(True)
            self.thread.terminate()

    def pHook(self, d):
        if d['status'] == 'downloading':
            percentage = int(float(d['_percent_str'].strip()[:-1]))
            self.progress_bar.setValue(percentage)
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)
            print('download completed')


if __name__ == '__main__':
    try:
        os.chdir(os.path.dirname(__file__))
        QDir.addSearchPath('icons', 'icons/')

        if getattr(sys, 'frozen', False):  # for pyinstaller
            application_path = os.path.dirname(sys.executable)
            os.environ['QT_PLUGIN_PATH'] = os.path.dirname(__file__) + r'\plugins'
            os.environ['path'] += ';' + os.path.dirname(__file__) + r'\ffmpeg'
        else:
            application_path = os.path.dirname(__file__)

        app = QApplication([])
        window = Window()
        window.show()
        sys.exit(app.exec())
    except SystemExit as e:
        print(f'Exit with return code: {e}')