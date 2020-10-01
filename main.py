# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import Signal, Slot, QFile
from PySide2.QtUiTools import QUiLoader

from enum import Enum
from window.カード待受 import 待受状態


class GohanMenu(QWidget):
    def __init__(self):
        super(GohanMenu, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "main.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    @Slot(bool)
    def menu_clicked(clicked: bool, 待受状態: 待受状態):
        pass


if __name__ == "__main__":
    app = QApplication([])
    widget = GohanMenu()
    widget.show()
    sys.exit(app.exec_())

