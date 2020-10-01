# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from enum import Enum

from object.社員 import 社員
from object.メニュー import メニュー

class main(QWidget):
    def __init__(self, 社員: 社員, メニュー: メニュー):
        super(main, self).__init__()
        self.load_ui()
        self.社員 = 社員
        self.メニュー = メニュー
        self.ui.btnGoBack.clicked.connect(
            lambda: self.ui.close())
        self.ui.btnReceive.clicked.connect(
            lambda: self.receive())

    def receive():
        pass

    def plot_data(self):
        self.ui.labelName.text = self.社員.社員名称
        self.ui.labelMenu.text = self.メニュー.内容

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "食事受取.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
