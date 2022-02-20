import calendar
import datetime

# 入力時の年と月を取得
this_year = datetime.date.today().year
this_month = datetime.date.today().month


def check_input_kikan_start_year():
    """
    ①設定したい期間の開始年を入力
    :rtype: object
    """
    kikan_start_year = None
    while True:
        try:
            kikan_start_year = int(input("設定したい期間の開始年を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (2002 <= kikan_start_year <= this_year):
                print("2002年以降で今年までの数値を入力してください")
                continue
            else:
                break
    return kikan_start_year


def check_input_kikan_start_month():
    """
    ②設定したい期間の開始月を入力
    :rtype: object
    """
    kikan_start_month = None
    while True:
        try:
            kikan_start_month = int(input("設定したい期間の開始月を入力してください: "))
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


def check_input_kikan_start_day():
    """
    ③設定したい期間の開始日を入力
    :rtype: object
    """
    kikan_start_day = None
    kikan_start_year = 2021
    kikan_start_month = 1
    month_count = calendar.monthrange(kikan_start_year, kikan_start_month)[1]
    print(month_count)
    while True:
        try:
            kikan_start_day = int(input("設定したい期間の開始日を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= kikan_start_day <= month_count):
                print("設定したい開始月の日数範囲にある数値を入力してください")
                continue
            else:
                break
    return kikan_start_day


def check_input_kikan_stop_year():
    """
    ①設定したい期間の終了年を入力
    :rtype: object
    """
    kikan_stop_year = None
    kikan_start_year = 2021
    while True:
        try:
            kikan_stop_year = int(input("設定したい期間の終了年を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (kikan_start_year <= kikan_stop_year <= this_year):
                print("開始年以降で今年までの数値を入力してください")
                continue
            else:
                break
    return kikan_stop_year


def check_input_kikan_stop_month():
    """
    ②設定したい期間の終了月を入力
    :rtype: object
    """
    kikan_stop_month = None
    while True:
        try:
            kikan_stop_month = int(input("設定したい期間の終了月を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= kikan_stop_month <= 12):
                print("1以上12以下の数値を入力してください")
                continue
            else:
                break
    return kikan_stop_month


def check_input_kikan_stop_day():
    """
    ③設定したい期間の終了日を入力
    :rtype: object
    """
    kikan_stop_day = None
    kikan_stop_year = 2022
    kikan_stop_month = 2
    month_count = calendar.monthrange(kikan_stop_year, kikan_stop_month)[1]
    print(month_count)
    while True:
        try:
            kikan_stop_day = int(input("設定したい期間の終了日を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= kikan_stop_day <= month_count):
                print("設定したい開始月の日数範囲にある数値を入力してください")
                continue
            else:
                break
    return kikan_stop_day


def check_input_kako_compare_kikan():
    """
    ⑦比較する過去データの期間を選択
    :rtype: object
    """
    kako_data_kikan = None
    kikan_start_year = 2010
    while True:
        try:
            kako_data_kikan = int(input("比較したい過去データの期間（1～20までの整数）を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= kako_data_kikan <= 20):
                print("1～20までの整数を入力してください")
                continue
            elif (kikan_start_year - 2002) < kako_data_kikan:
                print("過去データがないため、短い期間を再入力してください")
                continue
            else:
                break
    return kako_data_kikan
