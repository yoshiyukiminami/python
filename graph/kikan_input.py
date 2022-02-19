import datetime
from calendar import isleap

# 入力時の年と月を取得
this_year = datetime.date.today().year
this_month = datetime.date.today().month


def check_input_start_year():
    """
    ①過去データ開始年度入力
    :rtype: object
    """
    kako_start_year = None
    while True:
        try:
            kako_start_year = int(input("比較する過去データの開始年度を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if kako_start_year < 2002:
                print("2002年以降の年を入力してください")
                continue
            elif kako_start_year > this_year:
                print("本年度もしくはそれ以前の年を入力してください")
                continue
            else:
                break
    return kako_start_year


def check_input_start_month():
    """
    ②比較する期間の開始月入力
    :rtype: object
    """
    kikan_start_month = None
    while True:
        try:
            kikan_start_month = int(input("比較する期間の開始月を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= kikan_start_month <= 12):
                print("1以上12以下の数値を入力してください")
                continue
            else:
                break
    return kikan_start_month


def check_input_start_day(year, kikan_start_month):
    """
    ②比較する期間の開始日入力
    :rtype: object
    """

    kikan_start_day = None
    while True:
        try:
            kikan_start_day = int(input("比較する期間の開始日を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= kikan_start_day <= ):
                print("1以上12以下の数値を入力してください")
                continue
            else:
                break
    return kikan_start_month
# # ③比較する期間の開始日入力
# while True:
#     try:
#         kikan_start_day = int(input(": "))
#     except ValueError:
#         print("入力値が無効です。再入力してください。")
#         continue
#     else:
#         break
# if kikan_start_day < 1:
#     print("1以上の数値を入力してください")
# elif kikan_start_day > end_day:
#     print(str(end_day) and "以下の数値を入力してください")
# else:
#     print(kikan_start_day)
#
#
# # ④比較する期間の終了月入力
# while True:
#     try:
#         kikan_stop_month = int(input("比較する期間の終了月を入力してください: "))
#     except ValueError:
#         print("入力値が無効です。再入力してください。")
#         continue
#     else:
#         break
# if 1 > kikan_stop_month > 12:
#     print("1以上12以下の数値を入力してください")
# else:
#     print(kikan_stop_month)
#
#
# # ⑤比較する期間の終了日入力
# while True:
#     try:
#         kikan_stop_day = int(input("比較する期間の終了日を入力してください: "))
#     except ValueError:
#         print("入力値が無効です。再入力してください。")
#         continue
#     else:
#         break
# if kikan_stop_day < 1:
#     print("1以上の数値を入力してください")
# elif kikan_stop_day > end_day:
#     print(str(end_day) and "以下の数値を入力してください")
# else:
#     print(kikan_start_day)
