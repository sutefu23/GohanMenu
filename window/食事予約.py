# This Python file uses the following encoding: utf-8
import os

from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QFile
from PyQt5 import uic
from PyQt5.QtGui import QFont
from typing import List, Union

from datetime import date, time, timedelta, datetime
from enum import Enum
from object.メニュー import メニュー, 食事種類型, find提供日 as findメニュー提供日
from object.注文 import 注文, 食事要求状態, find提供日 as find注文提供日, find発注日 as find注文発注日, findメニューID as find注文メニューID
from object.社員 import 社員
from object.提供パターン import findTime as find提供時刻
from object import FileMakerDB
from window import 予約状況

import config


class checkStatus(Enum):
    On = "On"
    Off = "Off"

class Window(QWidget):
    メニューリスト: List[メニュー] = None
    注文リスト: List[注文] = None
    child_window: QWidget = None
    def __init__(self, 社員: 社員, 提供日: date = None):
        super(Window, self).__init__()
        self.load_ui()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.社員 = 社員
        self.提供日 = 提供日
        self.ui.btnGoBack.clicked.connect(
            lambda: self.quit())
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
        disableStyle = ":disabled { color: gray; }"

        self.ui.listMorning.setStyleSheet(disableStyle)
        self.ui.listLunch.setStyleSheet(disableStyle)

        self.plot_data()

    def quit(self):
        self.社員 = None
        self.ui.close()
        if self.child_window is not None:
            self.child_window.quit()

    def order(self, item: QListWidgetItem):
        #発注締切時刻以降は翌日より前のメニューを変更できない
        today = config.デバッグ日付 if config.環境 == "開発" else date.today()

        if config.発注締切時刻 <= datetime.now().time() and self.提供日 <= today + timedelta(days=1):
            QMessageBox.warning(
                None, "NOT PERMITTED", u"予約変更期限を過ぎています")
            return

        クリックメニュー名 = item.data(Qt.UserRole)  # hidden data
        if クリックメニュー名 is None:
            return

        クリックメニュー = self.getMenuByMenuName(クリックメニュー名)

        db = FileMakerDB.system
        db.prepareToken()

        isNewOrder = not self.isAlreadyOrder(クリックメニュー)

        if isNewOrder and self.isOrderLimit(クリックメニュー):  # 注文制限確認
            QMessageBox.warning(
                    None, "ORDER LIMIT", u"既に最大発注数をオーバーしています")
            return
        #一旦クリア
        for Order in self.注文リスト:
            if Order.種類 == クリックメニュー.種類:
                Order.delete()

        if isNewOrder:
            data = 注文(社員番号=self.社員.社員番号,
                      メニューID=クリックメニュー.メニューID, 状態=食事要求状態.未処理)
            if config.環境 == "開発":
                print('発注:', クリックメニュー名)
            data.upload()

        db.logout()
        self.plot_data()


    def plot_data(self):
        today = date.today() if config.環境 == "本番" else config.デバッグ日付

        if self.提供日 is None: #デフォルトでは今日発注のものを表示
            self.注文リスト = find注文発注日(today, self.社員.社員番号)
            if len(self.注文リスト) > 0:
                self.提供日 = self.注文リスト[0].提供日
            else: #今日注文したものがない場合は翌日提供日のメニューを出すのがデフォルト
                self.提供日 = today + timedelta(days=1)
        else:
            self.注文リスト = find注文提供日(self.提供日, self.社員.社員番号)

        #締切時間表示
        if self.提供日 == today + timedelta(days=1):
            self.ui.labelDeadLine.setVisible(True)            
            self.ui.labelDeadLine.setText(
                f"発注締切時刻: {time.strftime(config.発注締切時刻, '%H時%M分')}")
        else:
            self.ui.labelDeadLine.setVisible(False)

        self.メニューリスト = findメニュー提供日(self.提供日)

        self.ui.labelToday.setText(date.strftime(self.提供日, '%m月%d日(%a)'))
        self.ui.labelStaffName.setText(self.社員.社員名称)

        self.ui.listMorning.clear()
        self.ui.listLunch.clear()

        for 食事種類 in 食事種類型: #朝、昼でそれぞれメニューを抽出してループ処理
            抽出メニューリスト = list(filter(lambda メニュー: メニュー.種類 == 食事種類, self.メニューリスト))

            #提供時刻表示
            targetLabel = self.ui.labelMorningTime if 食事種類 == 食事種類型.朝食 else self.ui.labelLunchTime
            if len(抽出メニューリスト) > 0:
                (開始時刻, _) = find提供時刻(self.社員, 抽出メニューリスト[0])
                targetLabel.setText(time.strftime(開始時刻, '%H:%M'))
            else:
                targetLabel.setText("")

            for メニュー in 抽出メニューリスト:
                menuItem = QListWidgetItem(メニュー.内容)
                menuItem.setFont(QFont(QFont().defaultFamily(), 48))
                注文検索結果 = list(filter(lambda 注文: 注文.メニューID == メニュー.メニューID, self.注文リスト))
                if len(注文検索結果) > 0: #注文あり
                    self.setStatus(menuItem, checkStatus.On)
                else: #注文なし
                    self.setStatus(menuItem, checkStatus.Off)

                #カロリー、食塩などの情報行
                最大提供数 = "無制限" if self.isUnlimit(メニュー) else メニュー.最大提供数
                extraInfoItem = QListWidgetItem(
                    f"カロリー:{メニュー.カロリー}kcal　食塩:{メニュー.食塩}g　注文数:{self.getCurrentOrderAmount(メニュー)}　最大提供数:{最大提供数}　　　")
                extraInfoItem.setFont(QFont(QFont().defaultFamily(), 20))
                extraInfoItem.setTextAlignment(Qt.AlignRight)
                extraInfoItem.setFlags(Qt.ItemIsEnabled)

                blankItem = QListWidgetItem("")
                blankItem.setFont(QFont(QFont().defaultFamily(), 14))
                blankItem.setFlags(menuItem.flags() ^ Qt.ItemIsSelectable)


                #注文可能数を超えてないか確認
                if self.isOrderLimit(メニュー) and not self.isAlreadyOrder(メニュー):
                    menuItem.setFlags(menuItem.flags() ^ Qt.ItemIsEnabled)
                    extraInfoItem.setFlags(extraInfoItem.flags() ^ Qt.ItemIsEnabled)
                else:
                    menuItem.setData(Qt.UserRole, メニュー.内容)  # hidden data

                targetList = self.ui.listMorning if 食事種類 == 食事種類型.朝食 else self.ui.listLunch
                targetList.addItem(menuItem)
                targetList.addItem(extraInfoItem)
                targetList.addItem(blankItem)


    def isAlreadyOrder(self, メニュー: メニュー):  # データがすでに発注されたデータか否か
        発注検索結果 = list(
            filter(lambda 注文: 注文.内容 == メニュー.内容, self.注文リスト))  
        return len(発注検索結果) > 0

    def getMenuByMenuName(self, メニュー名): #メニュー内容からメニューオブジェクトを取得
        メニュー検索結果 = list(
                    filter(lambda メニュー: メニュー.内容 == メニュー名, self.メニューリスト))
        if len(メニュー検索結果) == 0:
            return
        return メニュー検索結果[0]

    def isUnlimit(self, メニュー:メニュー):
        return メニュー.最大提供数 == 999

    def isOrderLimit(self, メニュー:メニュー):
        if self.isUnlimit(メニュー):
            return False
        return self.getCurrentOrderAmount(メニュー) >= メニュー.最大提供数

    def getCurrentOrderAmount(self, メニュー: メニュー):
        注文メニュー群 = find注文メニューID(メニュー.メニューID)
        return len(注文メニュー群)


    def setStatus(self, item: QTableWidgetItem, status: checkStatus):
        if status == checkStatus.On:
            item.setText("✅" + item.text())
        else:
            item.setText("　" + item.text())

    def move_next(self):
        self.提供日 = self.提供日 + timedelta(days=1)
        self.plot_data()


    def move_prev(self):
        self.提供日 = self.提供日 - timedelta(days=1)
        self.plot_data()


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "食事予約.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file)
        ui_file.close()


    def open_confirm_window(self):
        self.child_window = 予約状況.Window(self.社員, self)
        if config.環境 == "開発":
            self.child_window.ui.show()
        else:
            self.child_window.ui.showFullScreen()
