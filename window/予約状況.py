# This Python file uses the following encoding: utf-8
import os
from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QScroller, QScrollerProperties

from datetime import date, timedelta, time
from typing import List
from window import 食事予約
from object.注文 import 注文, 食事種類型, find提供日以降 as find注文提供日以降
from object.メニュー import findメニューID
from object.社員 import 社員
from object.提供パターン import findTime as find提供時刻

import locale
import config

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

表示フォーマット = '%m/%d(%a)'
class Window(QWidget):
    注文リスト: List[注文]
    予約画面: 食事予約
    def __init__(self, 社員: 社員, 予約画面: 食事予約):
        super(Window, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.load_ui()
        self.予約画面 = 予約画面
        self.社員 = 社員
        self.ui.btnGoBack.clicked.connect(
            lambda: self.quit(withParent=False))
        self.ui.btnOpenReserve.clicked.connect(
            lambda: self.quit(withParent=True))
        self.ui.tableWidget.itemClicked.connect(self.reserve)
        self.plot_data()

        # タッチスクロール設定
        QScroller.grabGesture(self.ui.tableWidget, QScroller.LeftMouseButtonGesture)
        scroller = QScroller.scroller(self.ui.tableWidget)
        props = scroller.scrollerProperties()
        props.setScrollMetric(QScrollerProperties.MaximumVelocity, 0.5)
        scroller.setScrollerProperties(props)

    def quit(self, withParent:bool = True):
        if self.ui is not None:
            self.ui.close()
            self.ui = None
        if withParent and self.parent() is not None: 
            self.parent().ui.close()


    def reserve(self, item: QTableWidgetItem):
        if item.column() == 0 :
            if item.text() == "":
                return
            
            提供日 = item.data(Qt.UserRole)
            self.ui.close()
            self.予約画面.提供日 = 提供日
            self.予約画面.plot_data()


    def plot_data(self):
        self.ui.tableWidget.clear()

        表示開始日 = date.today()
        if config.環境 == "開発":
            表示開始日 = config.デバッグ日付

        self.注文リスト = find注文提供日以降(開始日=表示開始日,社員番号=self.社員.社員番号)
        
        if len(self.注文リスト) == 0:
            return
            
        max提供日メニューID = max(注文.メニューID for 注文 in self.注文リスト)

        注文検索結果 = list(
            filter(lambda 注文: 注文.メニューID == max提供日メニューID, self.注文リスト))
        max提供日 = 注文検索結果[0].提供日
    
        表示日数 = (max提供日 - 表示開始日).days + 1

        self.ui.tableWidget.setRowCount(表示日数 * len(食事種類型))

        row = 0
        for d in range(表示日数):
            for 食事種類 in 食事種類型:  # 朝、昼でそれぞれメニューを抽出してループ処理
                表示日付 = 表示開始日 + timedelta(days=d)

                if 食事種類 == 食事種類型.朝食:
                    提供日列 = QTableWidgetItem(表示日付.strftime(表示フォーマット))
                else:
                    提供日列 = QTableWidgetItem("")
                提供日列.setFont(QFont(QFont().defaultFamily(), 47))
                提供日列.setData(Qt.UserRole,表示日付)
                self.ui.tableWidget.setItem(row, 0, 提供日列)  # 提供日
                
                種類列 = QTableWidgetItem(食事種類.value)
                種類列.setFont(QFont(QFont().defaultFamily(), 48))
                self.ui.tableWidget.setItem(row, 1, 種類列)  # 朝夕

                注文検索結果 = list(filter(lambda 注文: 注文.提供日 ==
                                     表示日付 and 注文.種類 == 食事種類, self.注文リスト))
                
                if len(注文検索結果) > 0:  # 注文あり
                    メニュー名列 = QTableWidgetItem(注文検索結果[0].内容)
                    メニューデータ = findメニューID(注文検索結果[0].メニューID)
                    if len(メニューデータ) > 0 :
                        (開始時刻, _) = find提供時刻(self.社員, メニューデータ[0])
                        種類列.setText(種類列.text() + " " + time.strftime(開始時刻, '%H:%M'))

                else:
                    メニュー名列 = QTableWidgetItem(u"予約なし")

                メニュー名列.setFont(QFont(QFont().defaultFamily(), 48))
                self.ui.tableWidget.setItem(row, 2, メニュー名列)  # メニュー名 or 予約なし

                row += 1
        


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "予約状況.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file)
        ui_file.close()

