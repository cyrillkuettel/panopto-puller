import logging
import sys
import os
import yt_dlp
from PyQt6.QtCore import *
from PyQt6.QtCore import QThread
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QProgressBar, QVBoxLayout, QHBoxLayout, QFileDialog
from src.models import Cookie
from src.Utils import get_new_value

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))  # PYTHONPATH needs to be inserted. This enables running this script
# from the command line, from any directoy.
logging.basicConfig(level=logging.DEBUG)
Log = logging.getLogger(__name__)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.le_file_path = None
        self.btn_download = None
        self.btn_file_path = None
        self.btn_cookies = None
        self.le_url = None
        self.progress_bar = None
        self.status_info_label = None  # Shows information about the curent state

        self.thread = QThread()
        self.thread.started.connect(self.start_download_with_cookie)
        self.cookie = None

        self.create_window()
        self.create_widgets_and_layout()
        self.setup_onclick_listeners()

    def create_window(self):
        global app
        self.setWindowTitle('Panopto Puller')
        self.setWindowIcon(QIcon('icons:flat.png'))

        try:
            width = int(app.primaryScreen().size().width() * 0.42)
            height = int(app.primaryScreen().size().height() * 0.089)
            self.setup_frame(app.primaryScreen().availableGeometry().center())
        except NameError:
            width = int(1920 * 0.42)
            height = int(1080 * 0.089)
            self.setup_frame(QPoint(996, 553))
        finally:
            self.setFixedSize(width, height)

    def setup_frame(self, point: QPoint):
        frame = self.frameGeometry()
        frame.moveCenter(point)
        self.move(frame.topLeft())

    def create_widgets_and_layout(self):
        global application_path
        try:
            application_path
        except NameError:
            application_path = os.path.dirname(__file__)

        v_box = QVBoxLayout()

        # line 1
        self.label_url = QLabel('URL', self)
        self.btn_cookies = QPushButton()
        self.btn_cookies.setIcon(QIcon('icons:cookies.ico'))
        self.btn_file_path = QPushButton()
        self.btn_file_path.setIcon(QIcon('icons:choose-file-icon-16.png'))
        self.btn_download = QPushButton('Download', self)
        self.le_file_path = QLineEdit(application_path)
        self.le_file_path.setMaximumWidth(200)
        self.le_url = QLineEdit()
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.label_url)
        h_box1.addWidget(self.le_url)
        h_box1.addWidget(self.btn_cookies)
        h_box1.addWidget(self.le_file_path)
        h_box1.addWidget(self.btn_file_path)
        h_box1.addWidget(self.btn_download)
        v_box.addLayout(h_box1)

        # line 2
        h_box2 = QHBoxLayout()
        self.progress_bar: QProgressBar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        h_box2.addWidget(self.progress_bar)
        v_box.addLayout(h_box2)
        v_box.addStretch()

        # line 3 (printing status information)
        h_box3 = QHBoxLayout()
        self.status_info_label = QLabel('', self)
        self.status_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_box3.addWidget(self.status_info_label)
        v_box.addLayout(h_box3)
        self.setLayout(v_box)

    def choose_download_destination(self):
        file_path = QFileDialog.getExistingDirectory()
        self.le_file_path.setText(file_path)

    def on_click_download_button(self):
        if self.check_valid_input():
            self.thread.start()

    def check_valid_input(self):
        if self.cookie is None:
            self.status_info_label.setText('No cookies file loaded')
            self.status_info_label.setStyleSheet('color: red')
            Log.error("Need to provide a cookie")
            return False
        if self.le_url.text() == '':
            Log.error("No URL provided")
            self.status_info_label.setText('No URL provided')
            return False
        return True

    def start_download_with_cookie(self):

        ydl_opts = {'outtmpl': self.le_file_path.text() + '/%(title)s.%(ext)s', 'progress_hooks': [self.pHook],
                    'quiet': True, 'no_warnings': True, 'nocheckcertificate': True, 'format': 'best',
                    'cookies': self.cookie.absolute_file_path}

        try:
            self.status_info_label.setText(f'download from {self.le_url.text()}')
            self.btn_download.setEnabled(False)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.le_url.text()])
        except yt_dlp.utils.DownloadError or Exception as e:
            self.status_info_label.setText(f'Error: {e}')
            self.progress_bar.setValue(0)
        finally:
            self.btn_download.setEnabled(True)
            self.thread.terminate()

    def pHook(self, d):  # yt-dlp callback
        if d['status'] == 'downloading':
            progressbar_val = get_new_value(d)
            self.progress_bar.setValue(progressbar_val)
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)
            print('download completed')

    def open_cookie_file(self):
        try:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            dialog.setWindowTitle("Open cookies.txt")
            dialog.setNameFilters(["Text Files (*.txt)"])

            if dialog.exec():
                selected_Files = dialog.selectedFiles()
                cookie_file = selected_Files[0]
                if cookie_file.lower().endswith('.txt'):
                    self.cookie = Cookie()
                    with open(cookie_file, 'r') as f:
                        data = f.read()
                        self.cookie.cookie_data = data
                        f.close()
                    self.cookie.absolute_file_path = cookie_file
                    self.status_info_label.setText(f'Cookies file loaded: {cookie_file}')
                    self.status_info_label.setStyleSheet('color: green')
                else:
                    Log.error('Failed to load file. Is it actually a text file?')
        except Exception as ex:
            Log.error('Failed to open cookie File.')
            Log.error(ex)

    # noinspection PyUnresolvedReferences
    def setup_onclick_listeners(self):
        self.btn_file_path.clicked.connect(self.choose_download_destination)
        self.btn_download.clicked.connect(self.on_click_download_button)
        self.btn_cookies.clicked.connect(self.open_cookie_file)


if __name__ == '__main__':
    global app
    try:
        os.chdir(os.path.dirname(__file__))
        QDir.addSearchPath('icons', '../icons/')

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
        Log.error(f'Exit with return code: {e}')
