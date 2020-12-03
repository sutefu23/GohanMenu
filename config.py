import datetime
import sys

朝食期限時刻 = datetime.time(10, 30)  # 10時半
発注締切時刻 = datetime.time(15, 15)

#デバッグ日付 = datetime.date(2020, 11, 2)  # デバッグ用の今日の日付。開発時に有効
デバッグ日付 = datetime.date.today()  # デバッグ用の今日の日付。開発時に有効

セッション期限 = datetime.timedelta(minutes=1)

# python main.py devで開発起動
if len(sys.argv) > 1 and sys.argv[1] == "dev":
	環境 = "開発"  # 開発 or 本番
else:
	環境 = "本番"  # 開発 or 本番
