# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from enum import Enum

class 待受状態(Enum):
    食事予約 = "食事予約"
    予約状況 = "予約状況"
    食事受取 = "食事受取"


class WaitReading(QWidget):
    def __init__(self):
        super(WaitReading, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "Waiting.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
