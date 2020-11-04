# This Python file uses the following encoding: utf-8
import os

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QFile, QTimer
from PyQt5 import uic
from enum import Enum
from queue import Queue
from threading import Thread

from util.read import waiting_tag
from util.sound import SOUND
from util.counter import Timer
from window import 食事受取, 食事予約
from object.社員 import 社員, find as 社員find
from object.IDカード import find as IDカードfind
import config

queue = Queue()

class 待受状態(Enum):
    食事予約 = "食事予約"
    食事受取 = "食事受取"

class Window(QWidget):
    child_window: QWidget = None
    prev_idm = 0
    def __init__(self, 待受状態):
        self.待受状態 = 待受状態
        super(Window, self).__init__()
        self.load_ui()
        reading_thread = Thread(target=waiting_tag, args=(queue,))
        reading_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_queue)
        self.timer.start(100)

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "カード待受.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file)
        ui_file.close()

    def show_window(self, 社員: 社員):            
        if self.待受状態 == 待受状態.食事予約:
            self.child_window = 食事予約.Window(社員)
        elif self.待受状態 == 待受状態.食事受取:
            self.child_window = 食事受取.Window(社員)
        
        if config.環境 == "開発":
            self.child_window.ui.show()
        else:
            self.child_window.ui.showFullScreen()
                

    def fetch_queue(self):
        if not queue.empty():
            idm = queue.get()
            IDカード = IDカードfind(idm)
            if IDカード is None:
                return
            社員 = 社員find(IDカード.社員番号)
            if self.child_window is not None:
                if self.child_window.社員 is not None and self.child_window.社員.社員番号 == 社員.社員番号:  # すでに開いた画面で同じ社員が表示中
                    print("同じ社員が表示")
                    return
                else:
                    self.child_window.quit()

            beep = SOUND()
            beep.onRead()
            self.show_window(社員)
