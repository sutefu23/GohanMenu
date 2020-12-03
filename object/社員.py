# This Python file uses the following encoding: utf-8
from object import FileMakerDB
from object.IDカード import IDカード
# 社員テーブル
class 社員:
    社員番号: str
    社員名称: str
    社員_姓: str
    アマダ社員番号: str
    recordId: str
    IDカード: IDカード

    def __init__(self, record, IDカード: IDカード):
        self.社員番号 = record.string("社員番号")
        self.社員名称 = record.string("社員名称")
        self.社員_姓 = record.string("社員_姓")
        self.アマダ社員番号 = record.string("アマダ社員番号")
        self.IDカード = IDカード

# アクセス用レイアウト
DBName = "DataAPI_8" # pm_osakaname

# IDカードを入れたら社員を返す
def find(IDカード: IDカード):
    query = [{"社員番号": "=="+IDカード.社員番号}]
    db = FileMakerDB.pm_osakaname
    db.prepareToken()
    list = db.find(DBName, query)
    if not list:
        return
    return 社員(list[0], IDカード)

# 動作テスト
def test(): # オブジェクトを返すテスト
    社員番号 = "023"
    result = find(社員番号)
    print(result.社員番号) 
    print(result.社員名称) 
    print(result.アマダ社員番号) 
def test2(): # オブジェクトが存在しない場合のテスト
    社員番号 = "存在しない社員番号です"
    result = find(社員番号)
    print(result)
    if not result:
        print("ok")
#test()
#test2()
