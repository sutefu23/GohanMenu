# This Python file uses the following encoding: utf-8
from datetime import date
from object import 社員, メニュー, 注文


def find_order(date: date, staff: 社員) -> 注文:
  order = 注文()
  return order

def find_menu(date: date) -> メニュー:
  menu = メニュー()
  return menu
