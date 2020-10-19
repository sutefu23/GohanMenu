# This Python file uses the following encoding: utf-8
from datetime import datetime
import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QFile
from PyQt5 import uic
from typing import List

import datetime

from object.メニュー import  食事種類型
from object.注文 import 注文, find提供日, 食事要求状態
from object import FileMakerDB

import config

class Window(QWidget):
    社員:社員 = None
    注文:注文 = None
    食事種類:食事種類型 = None
    def __init__(self, 社員: 社員):
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
        
        self.ui.btnGoBack.clicked.connect(
            lambda: self.ui.close())
        self.ui.btnReceive.clicked.connect(
            lambda: self.receive())
        self.plot_data()

        
    def plot_data(self):
        self.ui.labelName.setText(self.社員.社員名称)
        if self.注文 is None:
            self.ui.labelMenu.setText(u"予約がありません")
            self.ui.btnReceive.setVisible(False)
            print("注文なし")
        elif self.注文.状態 != 食事要求状態.未処理:
            self.ui.labelMenu.setText(u"受取済")
            self.ui.btnReceive.setVisible(False)
            print("受取済")
        else:
            self.ui.labelMenu.setText(self.注文.内容)


    def receive(self):
        db = FileMakerDB.system
        db.prepareToken()
        data = 注文(社員番号=self.社員.社員番号, メニューID=self.注文.メニューID, 状態=食事要求状態.受取待)
        data.upload()
        db.logout()
        self.ui.close()


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "食事受取.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file)
        ui_file.close()
