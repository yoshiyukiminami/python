import csv
import datetime
import glob
import pandas as pd
import openpyxl
from dateutil.relativedelta import relativedelta
from monthdelta import monthmod


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('Python')
    # step-1:比較する期間の開始日と終了日を設定する
    # step-2:各年度の開始日と終了日にあたる行番号を特定し、各年度の対象データを抽出する
    # step-3:各年度の抽出データから項目毎のdataframeを作成する
    # step-4:比較年度の項目毎dataframeをまとめる
    # step-5:平均気温、日照時間は積算演算したdataframeを作成する
    # step-6:各dataframeから本年度（2022）、昨年度（2021）、2018～2020年平均（暖冬3年）、2008～2020年平均を抽出、グラフ化の元dataframeを作成する
    # step-7:グラフ化元dataframeから比較グラフを作成する

    # step-1:比較する期間の開始日と終了日を設定する
    # 開始日（本年度）：kikan_start ex.'2022/9/15'
    # 終了日（本年度）：kikan_end ex.'2023/2/28'
    kikan_start = '2022/9/15'
    kikan_start = datetime.datetime.strptime(kikan_start, '%Y/%m/%d')
    # 開始日からの期間（月）で終了日を決定・・修正
    kikan_range_month = '5'
    # kikan_end = '2023/2/28'
    # kikan_end = datetime.datetime.strptime(kikan_end, '%Y/%m/%d')

    # climate_data_save_hoseiフォルダー内にあるファイルをfilesに取得
    filedir = 'C:/Users/minam/Desktop/climate_data_save_hosei/'
    files = glob.glob(filedir + '/*.csv', recursive=True)
    print(files)

    # ファイル名から観測地点を特定
    # todo:観測地点（例：菊川牧之原）が2つ以上のファイルに含まれていた場合の処理
    # ヒント：読み込んだCSVファイルを一つのdataframeにまとめて（concat)エラーチェックをする
    isvalid = True
    for file in files:
        with open(file, newline='') as f:
            df = pd.read_csv(f)
            sokutei_point_list = [col for col in df.iteritems()]
            sokutei_point_list = sokutei_point_list[1][1:]
            # 観測地点名の取得とファイルに観測地点が複数ある場合、プログラムを中断する
            if len(set(sokutei_point_list[0][1:])) == 1:
                print("観測地点は一つです")
            else:
                print("ファイルに複数の観測地点があります")
                isvalid = False

            # todo:dataframeのsliceを調べる・・https://note.nkmk.me/python-pandas-datetime-timestamp/
            # dfの日付列をまとめてdatetime型に変換する
            df['年月日'] = pd.to_datetime(df['年月日'])
            # 変換したdfから日付（期間）でスライスする
            # 期間開始・終了を年毎に取得する
            df_header = df.head(0)
            print(df_header, type(df_header))
            for loop_year in range(2008, kikan_start.year + 1):
                temp_kikan_start = datetime.datetime.strptime(f"{loop_year}-{kikan_start.month}-{kikan_start.day}",
                                                              '%Y-%m-%d')
                temp_kikan_end = temp_kikan_start + relativedelta(months=int(kikan_range_month))

                df_slice_loop = df[df['年月日'].isin(pd.date_range(temp_kikan_start, temp_kikan_end))]
                print(df_slice_loop, type(df_slice_loop))
            # func_filtered_df(df, , kikan_start, kikan_end)
