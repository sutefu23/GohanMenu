# This Python file uses the following encoding: utf-8
from datetime import datetime
import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QFile, QTimer
from PyQt5 import uic
from typing import List

import datetime

from object.社員 import 社員 as 社員型
from object.メニュー import  食事種類型, findメニューID as find注文メニューID
from object.注文 import 注文 as 注文型, find提供日, 食事要求状態
from object import FileMakerDB
import config

TIMEOUT_MINUTE = 1

class Window(QWidget):
    社員: 社員型 = None
    注文: 注文型 = None
    食事種類:食事種類型 = None

    def __init__(self, 社員: 社員型):
        super(Window, self).__init__()
        self.load_ui()
        self.setAttribute(Qt.WA_DeleteOnClose)

        today = datetime.date.today()
        if config.環境 == "開発":
            today = config.デバッグ日付
        注文リスト = find提供日(today, 社員.社員番号)

        now = datetime.datetime.now().time()

        self.社員 = 社員
        
        if(now <= config.朝食期限時刻):
            self.食事種類 = 食事種類型.朝食
        else:
            self.食事種類 = 食事種類型.昼食

        注文検索結果 = list(filter(lambda 注文: 注文.種類 == self.食事種類, 注文リスト))
        if len(注文検索結果) > 0:
            self.注文 = 注文検索結果[0]
            if config.環境 == "開発":
                print(vars(self.注文))
        
        self.ui.btnGoBack.clicked.connect(self.quit)
        self.plot_data()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.quit)
        self.timer.start(TIMEOUT_MINUTE * 60 * 1000)

        
    def plot_data(self):
        self.ui.labelName.setText(self.社員.社員名称)
        self.ui.labelPayAmount.setVisible(False)

        if self.注文 is None:
             self.ui.labelMenu.setText(u"予約がありません")
             print("注文なし")
        elif self.注文.状態 == 食事要求状態.未処理:
            self.ui.labelMenu.setText(self.注文.内容)
            
            現金払い = not self.社員.アマダ社員番号.isdigit() #数字以外は現金払い
            if 現金払い:
                メニュー = find注文メニューID(self.注文.メニューID)
                if len(メニュー) > 0 :
                    self.ui.labelPayAmount.setVisible(True)
                    self.ui.labelPayAmount.setText(f"{メニュー[0].金額}円")
            if config.環境 == "本番":
                self.receive()
        else:
            self.ui.labelMenu.setText(u"受取済")
            print("受取済")


    def quit(self):
        self.社員 = None
        self.ui.close()
        
    def receive(self):
        db = FileMakerDB.system
        db.prepareToken()
        self.注文.状態 = 食事要求状態.受取待
        self.注文.upload()
        db.logout()


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "食事受取.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file)
        ui_file.close()
