# This Python file uses the following encoding: utf-8
from enum import Enum
from datetime import date
from object import FileMakerDB

from pprint import pprint

class 食事種類型(Enum):
    朝食 = "朝食"
    昼食 = "昼食"

class メニュー :
    メニューID: str
    図番: str
    提供日: date
    発注日: date
    種類: 食事種類型 
    内容: str
    カロリー: str
    食塩: str
    def __init__(self, record):
        self.メニューID = record.fieldData["メニューID"]
        self.図番 = record.fieldData["図番"]
        self.提供日 = record.day("提供日")
        self.発注日 = record.day("発注日")
        self.種類 = 食事種類型(record.fieldData["種類"])
        self.内容 = record.fieldData["内容"]
        self.カロリー = record.fieldData["カロリー"]
        self.食塩 = record.fieldData["食塩"]

# アクセス用レイアウト名
DBName = "DataAPI_6" # systemn

# メニューの検索
def find(query):
    db = FileMakerDB.system
    db.prepareToken()
    list = db.find(DBName, query)
    result = []
    for record in list:
        object = メニュー(record)
        result.append(object)
    return result

# 指定されたメニューIDのメニュー
def findメニューID(メニューID: str):
    query = [{"メニューID": f"=={メニューID}"}]
    return find(query)

# 指定された提供日のメニュー
def find提供日(提供日: date):
    daystr = FileMakerDB.makeDayString(提供日)
    query = [{"提供日": daystr}]
    return find(query)

# 指定された日にちか、それ以降の提供日のメニュー
def find提供日以降(開始日: date):
    daystr = FileMakerDB.makeDayString(開始日)
    query = [{"提供日": f">={daystr}"}]
    return find(query)

# テスト
def test():
    result = findメニューID("M000011")
    pprint(vars(result[0]))
def test2():
    day = date(2020, 11, 4)
    result = find提供日以降(day)
    pprint(vars(result[0]))

#test()
#test2()
