# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QListWidgetItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from enum import Enum
from typing import List

from datetime import date

from object.メニュー import メニュー, 食事種類型
from object.注文 import 注文

from window import 予約状況


class main(QWidget):
    def __init__(self, メニューリスト: List[メニュー], 注文: 注文):
        super(main, self).__init__()
        self.load_ui()
        self.メニューリスト = メニューリスト
        self.注文 = 注文
        self.ui.btnGoBack.clicked.connect(
            lambda: self.ui.close())
        self.ui.btnOpenConfirm.clicked.connect(
            lambda: self.open_confirm_window())
        self.plot_data()

    def plot_data(self):
        self.ui.labelToday.text = date.strftime(self.メニュー.提供日, '%m月%d日')

        self.ui.listMorning.clear()
        self.ui.listLunch.clear()
        
        朝食メニューリスト = filter(lambda メニュー: メニュー.種類 == 食事種類型.朝食, self.メニューリスト)
        昼食メニューリスト = filter(lambda メニュー: メニュー.種類 == 食事種類型.昼食, self.メニューリスト)

        icon_off_path = os.path.join(
            os.path.dirname(__file__), "icon", "check_off.svg")
        icon_on_path = os.path.join(
            os.path.dirname(__file__), "icon", "check_on.svg")

        for 朝食メニュー in 朝食メニューリスト:
            menuItem = QListWidgetItem(朝食メニュー.内容)
            menuItem.font().setPointSize(24)
            menuItem.icon().Off.addFile(icon_off_path)
            menuItem.icon().On.addFile(icon_on_path)
            self.ui.listMorning.addItem(menuItem)

        for 昼食メニュー in 昼食メニューリスト:
            menuItem = QListWidgetItem(昼食メニュー.内容)
            menuItem.font().setPointSize(24)
            menuItem.icon().Off.addFile(icon_off_path)
            menuItem.icon().On.addFile(icon_on_path)
            self.ui.listLunch.addItem(menuItem)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "食事予約.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def open_confirm_window(self):
        self.child_window = 予約状況()
        self.child_window.ui.show()
        self.child_window.ui.btnOpenReserve.setVisible(False)
