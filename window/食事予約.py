# This Python file uses the following encoding: utf-8
import os

from PySide2.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QIcon, QColor, QBrush
from typing import List

from datetime import date, timedelta, datetime

from object.メニュー import メニュー, 食事種類型, find提供日 as findメニュー提供日
from object.注文 import 注文, 食事要求状態, find提供日 as find注文提供日
from object.社員 import 社員
from object import FileMakerDB
from window import 予約状況

import config

IconOn = QIcon("icon/check_on.svg")
IconOff = QIcon("icon/check_off.svg")

class Window(QWidget):
    メニューリスト: List[メニュー] = None
    注文リスト: List[注文] = None

    def __init__(self, 社員: 社員, 提供日=date.today() + timedelta(days=1)):
        super(Window, self).__init__()
        self.load_ui()
        
        self.社員 = 社員
        self.提供日 = 提供日 #デフォルトでは今日の翌日
        if config.環境 == "開発":
            if self.提供日 == date.today() + timedelta(days=1):
               self.提供日 = config.デバッグ日付 + timedelta(days=1)

        self.ui.btnGoBack.clicked.connect(
            lambda: self.ui.close())
        self.ui.btnOpenConfirm.clicked.connect(
            lambda: self.open_confirm_window())
        self.ui.btnPrevDay.clicked.connect(
            lambda : self.move_prev()
        )
        self.ui.btnNextDay.clicked.connect(
            lambda: self.move_next()
        )
        self.ui.listMorning.itemClicked.connect(self.order)
        self.ui.listLunch.itemClicked.connect(self.order)

        self.plot_data()


    def order(self, item: QListWidgetItem):
        #発注締切時刻以降は翌日より前のメニューを変更できない
        today = config.デバッグ日付 if config.環境 == "開発" else date.today()

        if config.発注締切時刻 <= datetime.now().time() and self.提供日 <=  today + timedelta(days=1):
            QMessageBox.warning(
                None, "NOT FOUND", u"社員が見つかりません。", QMessageBox.OK)
            return

        クリックメニュー名 = item.text()
        メニュー検索結果 = list(
            filter(lambda メニュー: メニュー.内容 == クリックメニュー名, self.メニューリスト))
        クリックメニュー = メニュー検索結果[0]


        db = FileMakerDB.system
        db.prepareToken()


        発注検索結果 = list(
            filter(lambda 注文: 注文.内容 == クリックメニュー名, self.注文リスト)) #クリックされたデータはすでに発注されたデータである
        新規注文 = len(発注検索結果) == 0

        #一旦クリア
        for Order in self.注文リスト:
            if Order.種類 == クリックメニュー.種類:
                Order.delete()

        if 新規注文:
            data = 注文(社員番号=self.社員.社員番号,
                      メニューID=クリックメニュー.メニューID, 状態=食事要求状態.未処理)
            if config.環境 == "開発":
                print('発注:', クリックメニュー名)
            data.upload()
 
        db.logout()
        self.plot_data()


    def plot_data(self):
        self.メニューリスト = findメニュー提供日(self.提供日)
        self.注文リスト = find注文提供日(self.提供日, self.社員.社員番号)
        if config.環境 == "開発":
            print("提供日:", self.提供日, "社員番号:", self.社員.社員番号)
            if len(self.注文リスト) > 0 :
                print(vars(self.注文リスト[0]))

        self.ui.labelToday.setText(date.strftime(self.提供日, '%m月%d日'))
        self.ui.labelStaffName.setText(self.社員.社員名称)

        self.ui.listMorning.clear()
        self.ui.listLunch.clear()

        if(datetime.now().time() <= config.朝食期限時刻):
            現在食事種類 = 食事種類型.朝食
        else:
            現在食事種類 = 食事種類型.昼食

        for 食事種類 in 食事種類型: #朝、昼でそれぞれメニューを抽出してループ処理
            メニューリスト = list(filter(lambda メニュー: メニュー.種類 == 食事種類, self.メニューリスト))
            for メニュー in メニューリスト:
                menuItem = QListWidgetItem(メニュー.内容)
                menuItem.setFont(QFont(QFont().defaultFamily(), 24))

                注文検索結果 = list(filter(lambda 注文: 注文.メニューID == メニュー.メニューID, self.注文リスト))

                if len(注文検索結果) > 0: #注文あり
                    menuItem.setIcon(IconOn)

                    today = date.today()
                    if config.環境 == "開発":
                        today = config.デバッグ日付
                    if today == self.提供日:  # 今日の提供時間に該当しているものだと色を付ける
                        if 現在食事種類 == 食事種類:
                            menuItem.setForeground(QBrush(QColor(0, 0, 255)))
                        else:
                            menuItem.setForeground(QBrush(QColor(255, 0, 0)))

                else: #注文なし
                    menuItem.setIcon(IconOff)

                if 食事種類 == 食事種類型.朝食:
                    self.ui.listMorning.addItem(menuItem)
                elif 食事種類 == 食事種類型.昼食:
                    self.ui.listLunch.addItem(menuItem)

    
    def move_next(self):
        self.提供日 = self.提供日 + timedelta(days=1)
        self.plot_data()


    def move_prev(self):
        self.提供日 = self.提供日 - timedelta(days=1)
        self.plot_data()


    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "食事予約.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def open_confirm_window(self):
        self.child_window = 予約状況.Window(self.社員)
        self.child_window.ui.show()
        self.child_window.ui.btnOpenReserve.setVisible(False)
