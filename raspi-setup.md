# アップグレードコマンド（半日ほど時間かかります。）
`sudo apt -y update`
`sudo apt -y upgrade`
`sudo apt -y dist-upgrade`
`sudo apt -y install -y rpi-update`
`sudo apt -y install rpi-update`
`sudo curl -L --output /usr/bin/rpi-update https://raw.githubusercontent.com/Hexxeh/rpi-update/master/rpi-update && sudo chmod +x /usr/bin/rpi-update`
`sudo rpi-update`
`sudo apt-get install -y git`
`sudo reboot`


# pyenv のインストールとパスを追記
`git clone https://github.com/yyuu/pyenv.git ~/.pyenv`

`sudo vi ~/.profile`
#追記
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH" 
eval "$(pyenv init -)"

`source ~/.profile`

`pyenv install 3.8.5`
`pyenv global 3.8.5`

# GohanMenuダウンロード
`git clone https://github.com/osakaname/GohanMenu.git`
`cd GohanMenu`

# パッケージの一括インストール
`pip install --upgrade pip`
`pip install -r requirements.txt`
`pip install git+https://github.com/sn4k3/FakeRPi`

# PyQt5をいれる（１.５時間くらいかかる）
`sudo apt-get install qt-sdk qtbase5-dev libgl1-mesa-dev qt5-default`
`pip install PyQt5`

# コマンドパスを通す
`sudo vi ~/.profile`
#追記
export PATH="$HOME/.local/bin:$PATH"
`source ~/.profile`


# コマンドをsuユーザーでも使える様に
`visudo`

#Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin  コメントアウト
Defaults    env_keep += "HOME"  # 追加
Defaults    env_keep += "PATH"  # 追加
Defaults    env_keep += "PYENV_ROOT"  # 追加


# 画面の設定
`sudo apt-get install xscreensaver`

Raspberry Pi の再起動
メニュー > 設定 > Screensaver を選択
「モード」>「ブランク・スクリーンのみ」で分数を指定