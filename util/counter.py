#!/usr/bin python
# -*- coding: utf-8 -*-
import time
import config

class Timer:
    mile_stone = 0
    def __new__(cls): #シングルトン
        if not hasattr(cls, "_instance"):
            print("計測開始")
            cls.mile_stone = time.perf_counter()
            cls._instance = super(Timer, cls).__new__(cls)
        return cls._instance

    def init(self):
        self.mile_stone = time.perf_counter()

    def measure(self, text:str=None):
        interval = time.perf_counter() - self.mile_stone
        if config.環境 == "開発":
                print(text, ":", interval)
        self.mile_stone = time.perf_counter()
