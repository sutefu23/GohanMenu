# This Python file uses the following encoding: utf-8
import os


from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from enum import Enum

import nfc
import binascii
import time

from util.sound import SOUND

from window import 食事受取, 食事予約, 予約状況


class 待受状態(Enum):
    食事予約 = "食事予約"
    予約状況 = "予約状況"
    食事受取 = "食事受取"


class Window(QWidget):
    def __init__(self, 待受状態):
        self.待受状態 = 待受状態
        super(Window, self).__init__()
        self.load_ui()
        self.ui.btnGoBack.clicked.connect(
            lambda: self.ui.close())

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "カード待受.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def show_window(self):
        if self.待受状態 == 待受状態.食事予約:
            self.child_window = 食事予約.Window()
        elif self.待受状態 == 待受状態.予約状況:
            self.child_window = 予約状況.Window()
        elif self.待受状態 == 待受状態.食事受取:
            self.child_window = 食事受取.Window()
        self.child_window.ui.show()

    def waiting_tag():
        TIME_wait = 3

        target_req_felica = nfc.clf.RemoteTarget("212F")
        while True:
            clf = nfc.ContactlessFrontend('usb')
            TIME_cycle = 1.0
            TIME_interval = 0.2
            target_res = clf.sense(target_req_felica, iterations=int(
            TIME_cycle//TIME_interval)+1, interval=TIME_interval)

            if not target_res is None:
                beep = SOUND()
                beep.onRead()

                tag = nfc.tag.activate(clf, target_res)

                #IDmを取り出す
                idm = binascii.hexlify(tag.idm)
                print('FeliCa detected. idm = ' + str(idm))

                print('sleep ' + str(TIME_wait) + ' seconds')
                time.sleep(TIME_wait)
                clf.close()
