# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QFile
from PyQt5 import uic

from window import カード待受
import config 

print("現在の環境は", config.環境, "環境です。")

class GohanMenu(QWidget):

    def __init__(self):
        super(GohanMenu, self).__init__()
        self.load_ui()
        self.ui.btnOpenReserve.clicked.connect(
            lambda: self.show_window(カード待受.待受状態.食事予約))
        self.ui.btnOpenReceive.clicked.connect(
            lambda: self.show_window(カード待受.待受状態.食事受取))


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "main.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file, self)
        ui_file.close()

    def show_window(self, 待受状態: カード待受.待受状態):
        self.child_window = カード待受.Window(待受状態)
        if config.環境 == "開発":
            self.child_window.ui.show()
        else:
            self.child_window.ui.showFullScreen()


if __name__ == "__main__":
    app = QApplication([])
    widget = GohanMenu()
    if config.環境 == "開発":
        widget.show()
    else:
        widget.showFullScreen()
    sys.exit(app.exec_())

