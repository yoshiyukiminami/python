import datetime
from calendar import isleap

# 入力時の年と月を取得
this_year = datetime.date.today().year
this_month = datetime.date.today().month

# ①過去データ開始年度入力
while True:
    try:
        kako_start_year = int(input("比較する過去データの開始年度を入力してください: "))
    except ValueError:
        print("入力値が無効です。再入力してください。")
        continue
    else:
        break
if kako_start_year < 2002:
    print("2002年以降の年を入力してください")
elif kako_start_year > this_year:
    print("本年度もしくはそれ以前の年を入力してください")
else:
    print(kako_start_year)


# ②比較する期間の開始月入力
while True:
    try:
        kikan_start_month = int(input("比較する期間の開始月を入力してください: "))
    except ValueError:
        print("入力値が無効です。再入力してください。")
        continue
    else:
        break
if 1 > kikan_start_month > 12:
    print("1以上12以下の数値を入力してください")
else:
    print(kikan_start_month)


# 入力月により日入力ルールを設定
if kikan_start_month == (1, 3, 5, 7, 8, 10, 12):
    end_day = 31
elif kikan_start_month == 2 and isleap(this_year):
    print("今年はうるう年")
    end_day = 29
elif kikan_start_month == 2 and not isleap(this_year):
    print("今年は平年")
    end_day = 28
else:
    end_day = 30


# ③比較する期間の開始日入力
while True:
    try:
        kikan_start_day = int(input("比較する期間の開始日を入力してください: "))
    except ValueError:
        print("入力値が無効です。再入力してください。")
        continue
    else:
        break
if kikan_start_day < 1:
    print("1以上の数値を入力してください")
elif kikan_start_day > end_day:
    print(str(end_day) and "以下の数値を入力してください")
else:
    print(kikan_start_day)


# ④比較する期間の終了月入力
while True:
    try:
        kikan_stop_month = int(input("比較する期間の終了月を入力してください: "))
    except ValueError:
        print("入力値が無効です。再入力してください。")
        continue
    else:
        break
if 1 > kikan_stop_month > 12:
    print("1以上12以下の数値を入力してください")
else:
    print(kikan_stop_month)


# ⑤比較する期間の終了日入力
while True:
    try:
        kikan_stop_day = int(input("比較する期間の終了日を入力してください: "))
    except ValueError:
        print("入力値が無効です。再入力してください。")
        continue
    else:
        break
if kikan_stop_day < 1:
    print("1以上の数値を入力してください")
elif kikan_stop_day > end_day:
    print(str(end_day) and "以下の数値を入力してください")
else:
    print(kikan_start_day)
