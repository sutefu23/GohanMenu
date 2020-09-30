# This Python file uses the following encoding: utf-8
from enum import Enum

class 食事要求状態(Enum):
    未処理 = "未処理"
    受取待ち = "受取待ち"
    受渡済 = "受渡済"
