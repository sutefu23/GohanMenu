# This Python file uses the following encoding: utf-8
from object import FileMakerDB
from object.社員 import 社員
from object.メニュー import メニュー
from datetime import time 
from typing import List
# 提供パターンテーブル


class 提供パターン:
    提供パターン: int
    食事グループ: str
    開始時間: time
    終了時間: time
    def __init__(self, record):
        self.提供パターン = record.int("提供パターン")
        self.食事グループ = record.fieldData["食事グループ"]
        self.開始時間 = record.time("開始時間")
        self.終了時間= record.time("終了時間")

#テーブルデータ
マスタ: List[提供パターン] = None
# アクセス用レイアウト
DBName = "DataAPI_9"  # system


def findTime(社員: 社員, メニュー: メニュー):
    提供パターンリスト = fetch()
    for data in 提供パターンリスト:
        if data.食事グループ == 社員.IDカード.食事グループ and data.提供パターン == メニュー.提供パターン:
            return (data.開始時間, data.終了時間)

def fetch() -> List[提供パターン]:
    result = []
    if マスタ is None:
        db = FileMakerDB.system
        db.prepareToken()
        list = db.fetch(DBName)
        for record in list:
            object = 提供パターン(record)
            result.append(object)
    else:
        result = マスタ

    return result

# 動作テスト

def test():  # オブジェクトを返すテスト
    result = fetch()

#test()
#test2()
