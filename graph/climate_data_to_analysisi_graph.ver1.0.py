import csv
import datetime
import glob
import re

import pandas as pd
import openpyxl
from dateutil.relativedelta import relativedelta
from monthdelta import monthmod

def func_get_by_perspective2(df_slice_all, perspectives1, perspectives2, kikan_start):
    # print(df_slice_all)
    df_slice_all['月日'] = df_slice_all['年月日'].dt.strftime('%m-%d')
    df_slice_all['月日'] = [f"{re.sub('^0[1-3]', f'{12 + int(x[:2])}', x)}" for x in df_slice_all['年月日'].dt.strftime('%m-%d')]
    df_slice_all['年度'] = [(x - relativedelta(months=3)).strftime('%Y') for x in df_slice_all['年月日']]
    print("===", df_slice_all)
    kikan_start_date = kikan_start.strftime('%m-%d')
    # print(kikan_start_date)
    df_slice_all['年'] = df_slice_all['年月日'].dt.strftime('%Y')
    # df_slice_all['No'] = df_slice_all.groupby('年').cumcount()
    # print(df_slice_all, df_slice_all['月日'].dtypes)
    df_slice_perspective = pd.pivot_table(df_slice_all, index='月日',
                                          columns='年度', values=perspectives1)
    df_slice_perspective.to_csv('aaa.csv', encoding='shift-jis')
    print(df_slice_perspective)


def func_get_by_perspective(df_slice_loop, perspectives1, perspectives2):
    df_slice_loop = df_slice_loop.reset_index(drop=True)
    df_slice_loop['月日'] = df_slice_loop['年月日'].dt.strftime('%m-%d')
    col_name_year = df_slice_loop['年月日'][0].strftime('%Y')
    # 切り出したDataframeにNoと年（開始日の年→pivot_tableした時のカラム名になる）列を追加
    df_slice_loop['No'] = range(1, len(df_slice_loop.index) + 1)
    df_slice_loop['年度'] = col_name_year
    # print("===", df_slice_loop)
    sokutei_point = df_slice_loop['観測地点'].iloc[0, ]
    # 測定項目毎に切り出してwide-dataにpivotする
    for perspective in perspectives1:
        df_perspective = pd.pivot_table(df_slice_loop, index=['No', '月日'], columns='年度',
                                        values=perspective)
        col_rename = df_perspective.columns.values + "_" + str(perspective)
        col_prename = df_perspective.columns.values[0]
        col_rename = col_rename[0]
        df_perspective.rename(columns={col_prename: col_rename}, inplace=True)
        print(df_perspective)
        # perspective2にある項目は積算したDataframeを生成する
        if perspective in perspectives2:
            df_perspective_sekisan = df_perspective.cumsum()
            col_prename2 = df_perspective_sekisan.columns.values[0]
            print(col_prename2)
            col_rename2 = col_prename2.split('_')
            # col_rename2 = col_prename2.insert(1, "積算")
            print(col_rename2)
            print(df_perspective_sekisan)


if __name__ == '__main__':
    # step-1:比較する期間の開始日と終了日を設定する・・OK
    # step-2:各年度の開始日と終了日にあたる行番号を特定し、各年度の対象データを抽出する・・OK
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
    # グラフ作成する項目を選定
    # perspective1:グラフ化する項目、perspective2:積算する項目
    perspectives1 = ['平均気温', '日照時間', '最高気温', '最低気温', '降水量の合計', '1時間降水量の最大']
    perspectives2 = ['平均気温', '日照時間']
    # climate_data_save_hoseiフォルダー内にあるファイルをfilesに取得
    filedir = 'C:/Users/minam/Desktop/climate_data_save_hosei/'
    files = glob.glob(filedir + '/*.csv', recursive=True)
    print(files)

    # DATAFRAMEの原型alldf（辞書型）
    alldf = {'観測地点': [], '年月日': [],
             '平均気温': [], '平均気温（品質）': [], '平均気温（均質）': [],
             '日照時間': [], '日照時間（品質）': [], '日照時間（均質）': [],
             '最高気温': [], '最高気温（品質）': [], '最高気温（均質）': [],
             '最低気温': [], '最低気温（品質）': [], '最低気温（均質）': [],
             '降水量の合計': [], '降水量の合計（品質）': [], '降水量の合計（均質）': [],
             '1時間降水量の最大': [], '1時間降水量の最大（品質）': [], '1時間降水量の最大（均質）': []
             }

    # ファイル名から観測地点を特定
    # todo:観測地点（例：菊川牧之原）が2つ以上のファイルに含まれていた場合の処理
    # ヒント：読み込んだCSVファイルを一つのdataframeにまとめて（concat)エラーチェックをする
    isvalid = True
    for file in files:
        with open(file, newline='') as f:
            df = pd.read_csv(f, index_col=0)
            sokutei_point_list = [col for col in df.iteritems()]
            sokutei_point_list = sokutei_point_list[0][1:]
            # 観測地点名の取得とファイルに観測地点が複数ある場合、プログラムを中断する
            if len(set(sokutei_point_list[0][1:])) == 1:
                print("観測地点は一つです")
            else:
                print("ファイルに複数の観測地点があります")
                isvalid = False

            # dfの日付列をまとめてdatetime型に変換する
            df['年月日'] = pd.to_datetime(df['年月日'])
            # 変換したdfから日付（期間）でスライスする
            # 期間開始・終了を年毎に取得する
            for loop_year in range(2008, kikan_start.year + 1):
                temp_kikan_start = datetime.datetime.strptime(f"{loop_year}-{kikan_start.month}-{kikan_start.day}",
                                                              '%Y-%m-%d')
                temp_kikan_end = temp_kikan_start + relativedelta(months=int(kikan_range_month))
                df_slice_loop = df[df['年月日'].isin(pd.date_range(temp_kikan_start, temp_kikan_end))]
                # 指定期間で抽出したデータから項目別のdataframeを生成する
                # func_get_by_perspective(df_slice_loop, perspectives1, perspectives2)

                for i, data in enumerate(df_slice_loop.itertuples()):
                    # print(i, "==", data, type(data))
                    alldf['観測地点'].append(data[1])
                    # alldf['年月日'].append(datetime.datetime.strptime(data[2], '%Y-%m-%d'))
                    alldf['年月日'].append(data[2])
                    alldf['平均気温'].append(float(data[3]))
                    alldf['平均気温（品質）'].append(int(data[4]))
                    alldf['平均気温（均質）'].append(int(data[5]))
                    alldf['日照時間'].append(float(data[6]))
                    alldf['日照時間（品質）'].append(int(data[7]))
                    alldf['日照時間（均質）'].append(int(data[8]))
                    alldf['最高気温'].append(float(data[9]))
                    alldf['最高気温（品質）'].append(int(data[10]))
                    alldf['最高気温（均質）'].append(int(data[11]))
                    alldf['最低気温'].append(float(data[12]))
                    alldf['最低気温（品質）'].append(int(data[13]))
                    alldf['最低気温（均質）'].append(int(data[14]))
                    alldf['降水量の合計'].append(float(data[15]))
                    alldf['降水量の合計（品質）'].append(int(data[16]))
                    alldf['降水量の合計（均質）'].append(int(data[17]))
                    alldf['1時間降水量の最大'].append(float(data[18]))
                    alldf['1時間降水量の最大（品質）'].append(int(data[19]))
                    alldf['1時間降水量の最大（均質）'].append(int(data[20]))
            df_slice_all = pd.DataFrame(alldf)
            # df_slice_all.to_csv('df_slice_all.csv', encoding='shift-jis')
            func_get_by_perspective2(df_slice_all, perspectives1, perspectives2, kikan_start)
