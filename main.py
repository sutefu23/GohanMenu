# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

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
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "main.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def show_window(self, 待受状態: カード待受.待受状態):
        self.child_window = カード待受.Window(待受状態)
        self.child_window.ui.show()


if __name__ == "__main__":
    app = QApplication([])
    widget = GohanMenu()
    widget.show()
    sys.exit(app.exec_())

