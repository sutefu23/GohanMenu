# This Python file uses the following encoding: utf-8
from enum import Enum
from datetime import date

class 食事種類型(Enum):
    朝食 = "朝食"
    夕食 = "夕食"


class メニュー :
    メニューID: str
    提供日: date
    発注日: date
    種類: 食事種類型 
    内容: str
   

