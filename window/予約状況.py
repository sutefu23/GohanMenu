# This Python file uses the following encoding: utf-8
import os
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5 import uic
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from datetime import date, datetime, timedelta
from typing import List
from window import 食事予約
from object.注文 import 注文, 食事種類型, find提供日以降 as find注文提供日以降
from object.社員 import 社員

from pprint import pprint
import locale
import config

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

表示フォーマット = '%m/%d(%a)'
class Window(QWidget):
    注文リスト: List[注文]
    予約画面: 食事予約
    def __init__(self,  社員: 社員, 予約画面: 食事予約):
        super(Window, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.load_ui()
        self.予約画面 = 予約画面
        self.社員 = 社員
        self.ui.btnGoBack.clicked.connect(
            self.quit)
        self.ui.btnOpenReserve.clicked.connect(
            lambda: self.ui.close())
        self.ui.tableWidget.itemClicked.connect(self.reserve)
        self.plot_data()

    def quit(self):
        self.ui.close()
        if self.parent() is not None: 
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

        if(datetime.now().time() <= config.朝食期限時刻):
            現在食事種類 = 食事種類型.朝食
        else:
            現在食事種類 = 食事種類型.昼食

        row = 0
        for d in range(表示日数):
            for 食事種類 in 食事種類型:  # 朝、昼でそれぞれメニューを抽出してループ処理
                表示日付 = 表示開始日 + timedelta(days=d)

                if 食事種類 == 食事種類型.朝食:
                    提供日列 = QTableWidgetItem(表示日付.strftime(表示フォーマット))
                else:
                    提供日列 = QTableWidgetItem("")
                提供日列.setFont(QFont(QFont().defaultFamily(), 48))
                提供日列.setData(Qt.UserRole,表示日付)
                self.ui.tableWidget.setItem(row, 0, 提供日列)  # 提供日
                
                種類列 = QTableWidgetItem(食事種類.value)
                種類列.setFont(QFont(QFont().defaultFamily(), 48))
                種類列.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(row, 1, 種類列)  # 朝夕

                注文検索結果 = list(filter(lambda 注文: 注文.提供日 ==
                                     表示日付 and 注文.種類 == 食事種類, self.注文リスト))
                if len(注文検索結果) > 0:  # 注文あり
                    メニュー名列 = QTableWidgetItem(注文検索結果[0].内容)
                    today = date.today()
                    if config.環境 == "開発":
                        today = config.デバッグ日付
                    if today == 表示日付:  # 今日の提供時間に該当しているものだと色を付ける
                        if 現在食事種類 == 食事種類:
                            メニュー名列.setForeground(QBrush(QColor(0, 0, 255)))
                        else:
                            メニュー名列.setForeground(QBrush(QColor(255, 0, 0)))
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

