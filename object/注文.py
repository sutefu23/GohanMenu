# This Python file uses the following encoding: utf-8
from enum import Enum
from datetime import date
from object import FileMakerDB
from object.メニュー import 食事種類型
from datetime import datetime

class 食事要求状態(Enum):
    未処理 = "未処理"
    受取待 = "受取待"
    受渡済 = "受渡済"
    追加発注 = "追加発注"

class 注文:
    社員番号: str
    メニューID: str
    状態: 食事要求状態
    タイムスタンプ: datetime
    recordId: str = ""
    def __init__(self, record: FileMakerDB.FileMakerRecord = None, 社員番号 = None, メニューID = None, 状態 = None):
        if record:
            self.社員番号 = record.string("社員番号")
            self.メニューID = record.string("メニューID")
            self.状態 = 食事要求状態(record.string("要求状態"))
            self.タイムスタンプ = record.datetime("修正情報タイムスタンプ")
            self.recordId =  record.recordId
            self.提供日 = record.day("DataAPI_食事メニュー::提供日")
            self.発注日 = record.day("DataAPI_食事メニュー::発注日")
            self.種類 = 食事種類型(record.string("DataAPI_食事メニュー::種類"))
            self.内容 = record.string("DataAPI_食事メニュー::内容")
        if 社員番号:
            self.社員番号 = 社員番号
        if メニューID:
            self.メニューID = メニューID
        if 状態:
            self.状態 = 状態

    # db上のレコードを削除する
    def delete(self):
        if not self.recordId:
            return
        FileMakerDB.system.delete(DBName, self.recordId)

    # db上のデータをオブジェクトのデータで上書きする
    # db上にデータが無ければ追加する
    def upload(self):
        data = { "社員番号": self.社員番号, "メニューID": self.メニューID, "要求状態": self.状態.name }
        db = FileMakerDB.system
        db.prepareToken()
        if self.recordId:
            db.update(DBName, self.recordId, data) # 更新
        else:
            self.recordId = db.insert(DBName, data)  # 追加
        db.logout

# アクセス用レイアウト名
DBName = "DataAPI_7" # systemn

#注文検索
def find(query):
    result = []
    db = FileMakerDB.system
    db.prepareToken()
    list = db.find(DBName, query)
    db.logout()
    for record in list:
        object = 注文(record)
        result.append(object)
    return result


def find提供日(提供日: date, 社員番号: str):
    daystr = FileMakerDB.makeDayString(提供日)
    query = [{"DataAPI_食事メニュー::提供日": "=="+daystr, "社員番号": "=="+社員番号}]
    return find(query)


def find提供日以降(開始日: date, 社員番号: str):
    daystr = FileMakerDB.makeDayString(開始日)
    query = [{"DataAPI_食事メニュー::提供日": f">={daystr}", "社員番号": "=="+社員番号}]
    return find(query)

def find発注日(発注日: date, 社員番号: str):
    daystr = FileMakerDB.makeDayString(発注日)
    query = [{"DataAPI_食事メニュー::発注日": "=="+daystr, "社員番号": "=="+社員番号}]
    return find(query)

def find発注日以降(開始日: date, 社員番号: str):
    daystr = FileMakerDB.makeDayString(開始日)
    query = [{"DataAPI_食事メニュー::発注日": f">={daystr}", "社員番号": "=="+社員番号}]
    return find(query)


def findメニューID(メニューID: str):
    query = [{"メニューID": "=="+メニューID}]
    return find(query)

#テスト
def test():
    db = FileMakerDB.system
    db.prepareToken()
    data = 注文(社員番号="023",メニューID="M000011",状態=食事要求状態.受取待)
    data.upload()    

def test2():
    提供日 = date(2020,11,1)
    find提供日(提供日, '023')

def test3():
    メニュー = findメニューID("M000011")
    print(f"{メニュー}")


def test4():
    メニュー = findメニューID("M000011")
    print(vars(メニュー[0]))

#test()
#test2()
#test3()
#test4()
