# This Python file uses the following encoding: utf-8

import FileMakerDB

# IDカードテーブル
class IDカード:
    社員番号: str
    カードID: str
    recordId: str
    def __init__(self, record):
        self.社員番号 = record.fieldData["社員番号"]
        self.カードID = record.fieldData["カードID"]
        self.recordId = record.recordId

# アクセス用レイアウト名
DBName = "DataAPI_8" # systemn

# カードIDに対応するIDカードオブジェクトを返す
def find(カードID):
    query = [{"カードID": カードID}] 
    db = FileMakerDB.system
    db.prepareToken()
    list = db.find(DBName, query)
    if not list:
        return
    return IDカード(list[0])

# 動作テスト
def test(): # オブジェクトを返すテスト
    cardID = "aabbccdd"
    result = find(cardID)
    print(result.社員番号) 
    print(result.recordId) 
def test2(): # オブジェクトが存在しない場合のテスト
    cardID = "存在しないカードIDです"
    result = find(cardID)
    print(result)
    if not result:
        print("ok")
#test()
#test2()
