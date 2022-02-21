import calendar
import datetime

# 入力時の年と月を取得
this_year = datetime.date.today().year
this_month = datetime.date.today().month


def check_valid_date(from_to_in_the_year, previous_years):
    """
    設定したい期間の開始及び収量年月日と比較した過去データの期間を入力
    :rtype: object
    """
    from_to_in_the_year = None
    previous_years = None

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

    kikan_start_day = None
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

    from_date = datetime.datetime(kikan_start_year, kikan_start_month, kikan_start_day, 0, 0, 0)
    print(from_date)

    kikan_stop_year = None
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

    kikan_stop_day = None
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

    to_date = datetime.datetime(kikan_stop_year, kikan_stop_month, kikan_stop_day, 0, 0, 0)
    print(to_date)
    from_to_in_the_year = [from_date, to_date]
    print(from_to_in_the_year)

    while True:
        try:
            previous_years = int(input("比較したい過去データの期間（1～20までの整数）を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (1 <= previous_years <= 20):
                print("1～20までの整数を入力してください")
                continue
            elif (kikan_start_year - 2002) < previous_years:
                print("過去データがないため、短い期間を再入力してください")
                continue
            else:
                break

    print(previous_years)

    return from_to_in_the_year, previous_years
