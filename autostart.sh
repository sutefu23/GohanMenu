#!/bin/bash -
cd ~/GohanMenu
while :
  do
    if [ "ping -c 1 -W 1 github.com" ]; then
      echo "コネクション確認"
      git pull
      break
    else
      sleep 1
      echo "コネクション確認リトライ"
    fi
  done


while :
  do
    if [ "`ps ax | grep python main.py`" ]; then
      # "ソフト起動中"
      sleep 1
    else
      echo "ソフト起動を確認できないため起動処理"
      sudo python main.py
    fi
  done