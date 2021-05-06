from finder import control_method
from function import *
import time
from multiprocessing import Process, Queue, freeze_support

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.log_box = QTextEdit(self)
        self.log_box.setReadOnly(True)

        self.path_line_edit = QLineEdit(self)
        self.label1 = QLabel("video files directory")

        self.open_button = QPushButton("Open (O)", self)
        self.start_button = QPushButton("Start (F2)", self)

        self.start_button.setMinimumHeight(100)

        line_edit_button_layout = QGridLayout()
        line_edit_button_layout.addWidget(self.label1, 0, 0)
        line_edit_button_layout.addWidget(self.path_line_edit, 1, 0)
        line_edit_button_layout.addWidget(self.open_button, 1, 1)

        layout = QVBoxLayout()
        layout.addWidget(self.log_box)
        layout.addLayout(line_edit_button_layout)
        layout.addWidget(self.start_button)

        self.setLayout(layout)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Image Detection at Video'
        self.position = (50, 50, 600, 1000)
        self.cWidget = CentralWidget()
        self.setCentralWidget(self.cWidget)

        self.queue = Queue()
        self.finished_check_timer = QTimer()
        self.controller = None
        self.work_status = False
        self.work_start_time = None
        self.work_start_time_string = ""
        self.folder = None
        self.current_log = ""

        # Function Setting
        find_start = QAction("&Start (F2)", self)
        find_start.setShortcut('F2')
        find_start.setStatusTip('Find Start')
        find_start.triggered.connect(self.program_start)
        self.cWidget.start_button.setDefault(True)
        self.cWidget.start_button.clicked.connect(self.program_start)

        get_path = QAction("&Open (O)", self)
        get_path.setShortcut('O')
        get_path.setStatusTip('Open')
        get_path.triggered.connect(self.set_folder_path)
        self.cWidget.open_button.clicked.connect(self.set_folder_path)

        self.statusBar()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&Menu')
        file_menu.addAction(find_start)
        file_menu.addAction(get_path)

        # App Window setting
        self.setWindowTitle(self.title)
        self.setGeometry(
            self.position[0], self.position[1], self.position[2], self.position[3])

        self.show()

    def program_start(self):
        if not self.work_status:
            self.work_status = True
            self.work_start_time = time.localtime()
            self.work_start_time_string = time.strftime(
                "%Y%m%d-%H%M%S", self.work_start_time)
            self.get_folder_path()

            self.controller = Process(target=control_method, args=(
                self.queue, self.folder, ))
            self.controller.daemon = True
            self.controller.start()

            self.finished_check_timer.setInterval(1000)
            self.finished_check_timer.timeout.connect(self.check_log_update)
            self.finished_check_timer.start()

    def set_folder_path(self):
        path = QFileDialog.getExistingDirectory(self)
        if path:
            path = path + "/"
            self.cWidget.path_line_edit.setText(path)

    def get_folder_path(self):
        if self.cWidget.path_line_edit.text():
            self.folder = self.cWidget.path_line_edit.text()

    def check_log_update(self):
        if self.queue.qsize():
            result = self.queue.get()

            # timestamp, thread_number = result[0], result[1]
            timestamp = result[0]
            self.current_log += timestamp + "\n"

            folder_path = make_folder_tree(
                log_save_root, self.work_start_time,
                self.work_start_time_string)
            make_folder(folder_path)
            log_file_name = "{}.txt".format(
                self.work_start_time_string)

            log_path = folder_path + log_file_name

            self.cWidget.log_box.append(timestamp)
            text_save(log_path, self.current_log)

            if timestamp == "process finished.":
                self.initialize()

    def initialize(self):
        self.finished_check_timer.stop()
        self.controller.join()

        self.work_status = False
        self.work_start_time = None
        self.work_start_time_string = ""
        self.folder = None
        self.current_log = ""


if __name__ == '__main__':
    freeze_support()
    import sys
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
