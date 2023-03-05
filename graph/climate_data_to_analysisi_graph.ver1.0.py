import csv
import datetime
import glob
import re

import pandas as pd
import openpyxl
from dateutil.relativedelta import relativedelta
from monthdelta import monthmod

def func_get_by_perspective(df_slice_all, perspectives1, perspectives2, over_month):
    # df_slice_allの年月日列から月日のみ取り出した列を追加・・pivot_tableのkeyindex
    # 年をまだぐ期間設定対策1として、1月以降を13月～（∔12）に変更
    # 年をまたぐ期間設定対策2として、1月以降が期間の年度合わせ・・要確認（month=3の3は固定で良い？）
    df_slice_all['月日'] = df_slice_all['年月日'].dt.strftime('%m-%d')
    # todo:下記の［1-3］と［：2］は固定？期間設定と連動した処理が必要か？
    df_slice_all['月日'] = [f"{re.sub('^0[1-3]', f'{12 + int(x[:2])}', x)}" for x in df_slice_all['年月日'].dt.strftime('%m-%d')]
    # 年をまたぐ期間（月＝変数over_month）を年月日の数値から減算して、年度を割り出すように変更
    df_slice_all['年度'] = [(x - relativedelta(months=over_month)).strftime('%Y') for x in df_slice_all['年月日']]
    df_slice_all['年'] = df_slice_all['年月日'].dt.strftime('%Y')
    # df_slide_allをpivot_tableに変換（wide型）
    df_slice_perspective = pd.pivot_table(df_slice_all, index='月日',
                                          columns='年度', values=perspectives1)
    # 月日表示を元に戻す際の昇順崩れ防止にNo.を付与
    df_slice_perspective['No'] = range(1, len(df_slice_perspective.index) + 1)
    # df_slice_perspective.to_csv('aaa.csv', encoding='shift-jis')
    # print(df_slice_perspective)
    func_get_describe(df_slice_perspective, perspectives2)


def func_get_describe(df_slice_perspective, perspectives2):
    # Multiindex型のカラム名を統合する（level0とlevel1を統合、level0を削除してMultiindex型を解除
    print(df_slice_perspective, "==")
    koumokus = df_slice_perspective.columns.get_level_values(level=0)
    nendos = df_slice_perspective.columns.get_level_values(level=1)
    new_col_names = {}
    for koumoku, nendo in zip(koumokus, nendos):
        new_col_name = koumoku + "_" + nendo
        new_col_names[nendo] = new_col_name
    # todo:Multiindex型カラムの修正
    print(new_col_names)
    # df_slice_perspective.columns.set_names(new_col_names, inplace=True)
    df_slice_perspective.rename(columns=new_col_names, level=1)
    print(df_slice_perspective.columns)
    print(df_slice_perspective)
    # df_slice_perspective.to_csv('aaa.csv', encoding='shift-jis')


if __name__ == '__main__':
    # step-1:比較する期間の開始日と終了日を設定する・・OK
    # step-2:各年度の開始日と終了日にあたる行番号を特定し、各年度の対象データを抽出する・・OK
    # step-3:各年度の抽出データから項目毎のdataframeを作成する・・OK
    # step-4:比較年度の項目毎dataframeをまとめる・・OK
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
    over_month = kikan_start.month + int(kikan_range_month) - 12
    print(over_month)
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
                # 年毎に取得したデータをall_dfのDataframeにappendする
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
            # 任意の期間で取り出したDataframe（df_slice_all）を項目別・年度別でピボットテーブルを生成・・関数
            func_get_by_perspective(df_slice_all, perspectives1, perspectives2, over_month)
