#!/usr/bin python
# -*- coding: utf-8 -*-
import nfc
import binascii
import time
from queue import Queue
from util import sound


def waiting_tag(queue: Queue):

    # タッチされてから次の待ち受けを開始するまで無効化する秒
    TIME_wait = 3

    # NFC接続リクエストのための準備
    # target_req_felica = nfc.clf.RemoteTarget("212F")

    target_req_nfc = nfc.clf.RemoteTarget("106A")
    print("Waiting for Tag...")
    try:
        while True:
            # USBに接続されたNFCリーダに接続
            clf = nfc.ContactlessFrontend('usb:054c:06c3')
            # 待ち受けの1サイクル秒
            TIME_cycle = 1.0
            # 待ち受けの反応インターバル秒
            TIME_interval = 0.2
            # target_res = clf.sense(target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
            target_res = clf.sense(target_req_nfc, iterations=int(TIME_cycle//TIME_interval)+1, interval=TIME_interval)
            if not target_res is None:
                beep = sound.SOUND()
                beep.onRead()

                tag = nfc.tag.activate(clf, target_res)

                #IDmを取り出す
                # idm = binascii.hexlify(tag.idm)
                idm = str(tag.identifier).encode().hex().upper()
                queue.put(idm)

                print('FeliCa detected. idm = ' + str(idm))
                print('sleep ' + str(TIME_wait) + ' seconds')
                time.sleep(TIME_wait)

            clf.close()
        #end while
    except PermissionError as e:
            print(e)



