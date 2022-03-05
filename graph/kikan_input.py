import calendar
import datetime

# 入力時の年と月を取得
this_year = datetime.date.today().year
this_month = datetime.date.today().month


def check_valid_date1():
    """
    設定したい期間の開始年月日を入力
    :rtype: object
    """
    from_date = None
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
                try:
                    from_date = datetime.datetime(kikan_start_year, kikan_start_month,
                                                  kikan_start_day, 0, 0, 0)
                except ValueError:
                    print("無効な日を設定しています。再入力してください")
                    continue
                else:
                    print(from_date)
                    break

    to_date = None
    kikan_stop_year = None
    while True:
        try:
            kikan_stop_year = int(input("設定したい期間の終了年を入力してください: "))
        except ValueError:
            print("入力値が無効です。再入力してください。")
            continue
        else:
            if not (from_date.year <= kikan_stop_year <= this_year):
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
            if from_date.year == kikan_stop_year and (from_date.month - kikan_stop_month) < 0:
                print("終了月が開始月の前に設定されています。終了月は開始月以降で設定ください")
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
                print("設定したい終了月の日数範囲にある数値を入力してください")
                continue
            if from_date.month == kikan_stop_month and (from_date.day - kikan_stop_day) < 0:
                print("終了日が開始日の前に設定されています。終了日は開始日以降で設定ください")
                continue
            else:
                try:
                    to_date = datetime.datetime(kikan_stop_year, kikan_stop_month, kikan_stop_day,
                                                0, 0, 0)
                except ValueError:
                    print("無効な日が設定されています。再入力してください")
                    continue
                else:
                    print(to_date)
                    break

    previous_years = None
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
            elif (from_date.year - 2002) < previous_years:
                print("過去データがないため、短い期間を再入力してください")
                continue
            else:
                print(previous_years)
                break

    return from_date, to_date, previous_years


if __name__ == "__main__":
    print(check_valid_date1())
