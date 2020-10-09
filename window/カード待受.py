# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QWidget, QMessageBox
from PySide2.QtCore import QFile, QTimer
from PySide2.QtUiTools import QUiLoader
from enum import Enum
from queue import Queue
from threading import Thread

from util.read import waiting_tag

from window import 食事受取, 食事予約
from object.社員 import 社員, find as 社員find
from object.IDカード import find as IDカードfind

queue = Queue()

class 待受状態(Enum):
    食事予約 = "食事予約"
    食事受取 = "食事受取"

class Window(QWidget):
    def __init__(self, 待受状態):
        self.待受状態 = 待受状態
        super(Window, self).__init__()
        self.load_ui()
        reading_thread = Thread(target=waiting_tag, args=(queue,))
        reading_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_queue)
        self.timer.start(500)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "カード待受.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def show_window(self, 社員: 社員):
        if self.待受状態 == 待受状態.食事予約:
            self.child_window = 食事予約.Window(社員)
        elif self.待受状態 == 待受状態.食事受取:
            self.child_window = 食事受取.Window(社員)
        self.child_window.ui.show()

    def fetch_queue(self):
        if not queue.empty():
            idm = queue.get()
            IDカード = IDカードfind(idm)
            社員 = 社員find(IDカード.社員番号)
            if 社員 is None:
                QMessageBox.warning(
                    None, "NOT FOUND", u"社員が見つかりません。", QMessageBox.OK)
            else:
                self.show_window(社員)
