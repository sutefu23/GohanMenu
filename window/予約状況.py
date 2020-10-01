# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QWidget, QTableWidgetItem
from PySide2.QtCore import Qt, QFile
from PySide2.QtUiTools import QUiLoader
from typing import List
from enum import Enum

from window import 食事予約

from object.注文 import 注文


class Window(QWidget):
    def __init__(self, 注文リスト: List[注文]):
        super(Window, self).__init__()
        self.load_ui()
        self.注文リスト = 注文リスト
        self.ui.btnGoBack.clicked.connect(
            lambda: self.ui.close())
        self.ui.btnOpenReserve.clicked.connect(
            lambda: self.ui.open_reserve_window())

    def plot_data(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(len(self.注文リスト))

        row = 0
        for 注文 in self.注文リスト:
            提供日 = QTableWidgetItem("提供日")
            提供日.font().setPointSize(24)
            self.ui.tableWidget.setItem(row, 0, 提供日)  # 提供日

            食事種類 = QTableWidgetItem("食事種類")
            食事種類.font().setPointSize(24)
            食事種類.setTextAlignment(Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row, 1, 食事種類)  # 朝夕

            メニュー名 = QTableWidgetItem("メニュー名")
            メニュー名.font().setPointSize(24)
            self.ui.tableWidget.setItem(row, 1, メニュー名)  # メニュー名 or 予約なし

            row += 1
    
    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "予約状況.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def open_reserve_window(self):
        self.child_window = 食事予約.Window()
        self.child_window.ui.show()
        self.child_window.ui.btnOpenConfirm.setVisible(False)
