# This Python file uses the following encoding: utf-8

from object import FileMakerDB

# 社員テーブル
class 社員:
    社員番号: str
    社員名称: str
    社員_姓: str
    recordId: str
    def __init__(self, record):
        self.社員番号 = record.fieldData["社員番号"]
        self.社員名称 = record.fieldData["社員名称"]
        self.社員_姓 = record.fieldData["社員_姓"]

# アクセス用レイアウト
DBName = "DataAPI_8" # pm_osakaname

    # 社員番号に対応する社員オブジェクトを返す
def find(社員番号):
    query = [{"社員番号": 社員番号}] 
    db = FileMakerDB.pm_osakaname
    db.prepareToken()
    list = db.find(DBName, query)
    if not list:
        return
    return 社員(list[0])

# 動作テスト
def test(): # オブジェクトを返すテスト
    社員番号 = "023"
    result = find(社員番号)
    print(result.社員番号) 
    print(result.社員名称) 
def test2(): # オブジェクトが存在しない場合のテスト
    社員番号 = "存在しない社員番号です"
    result = find(社員番号)
    print(result)
    if not result:
        print("ok")
#test()
#test2()
