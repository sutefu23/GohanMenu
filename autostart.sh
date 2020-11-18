#!/bin/bash -
cd ~/GohanMenu
sleep 15
git pull

while :
  do
    if [ "`sudo ps ax | grep python main.py`" ]; then
      # "ソフト起動中"
      sleep 1
    else
      echo "ソフト起動を確認できないため起動処理"
      sudo python main.py
    fi
  done