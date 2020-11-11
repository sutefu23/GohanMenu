import queue
import unittest
import config
from object import IDカード, メニュー, 社員, 注文
from util import read
from queue import Queue
基準日 = config.デバッグ日付
test_idm = "62275C7830312E4C5C786533505C783038644327"

class TestRead(unittest.TestCase):
    def test_waiting_tag(self):
        queue = Queue()
        while True:
            read.waiting_tag()
            if not queue.empty():
                break
        idm = queue.get()
        print(idm)
        self.assertEqual(idm, 10)

