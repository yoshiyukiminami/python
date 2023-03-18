import datetime
import glob
import re
import pandas as pd
from dateutil.relativedelta import relativedelta


def func_get_by_perspective(df1: pd.DataFrame, k1: list, k2: list, month: int):
    # df:元のDataframe、k1:抽出する項目、k2：積算を追加する項目、month：年をまたぐ月数
    # dfの「年月日」列から月日に変換した列を追加
    df1['月日'] = df1['年月日'].dt.strftime('%m-%d')
    # monthがプラスの時（＝年またぎあり）のみ年をまたぐ期間対策を発動する
    if month > 0:
        # 年をまだぐ期間設定対策1として、1月以降を13月～（∔12）に変更し、1月以降の月日が12月31日以降に配列されるようにする
        # seiki_hyogenに表示を変更する文字列を指定
        seiki_hyogen = "^0" + "[" + "1-" + str(month + 1) + "]"
        df1['月日'] = [f"{re.sub(seiki_hyogen, f'{12 + int(x[:month])}', x)}" for x in df1['年月日'].dt.strftime('%m-%d')]
        # 年をまたぐ期間設定対策2として、1月以降が入る期間設定の場合、1月以降のデータも年度としては12月までの年度に含む
        df1['年度'] = [(x - relativedelta(months=i)).strftime('%Y') for x in df1['年月日']]
        print("年またぎ有り")
    else:
        # dfの「年月日」列から月日に変換した列を追加
        df1['年度'] = df['年月日'].dt.strftime('%Y')
        print("年またぎ無し")
    # df_slide_allをpivot_tableに変換（wide型）
    df_slice_perspective = pd.pivot_table(df1, index='月日', columns='年度', values=k1)
    # 月日表示を元に戻す際の昇順崩れ防止に1から連番を降った新しい列（列名：No）を追加し、先頭列に挿入する
    new_col_no = pd.Series(range(1, len(df_slice_perspective.index) + 1))
    df_slice_perspective.insert(0, 'No', new_col_no)
    func_get_by_perspective2(df_slice_perspective, k1, k2)


def func_get_by_perspective2(df2: pd.DataFrame, k1: list, k2: list):
    # step-5:k2リストの項目のみ、積算演算した列を追加する
    # df2のカラム名（マルチカラムのlevel=1）から年度のリスト(nendo_list)を生成する
    nendo_list = set(df2.columns.droplevel(level=0))
    nendo_list = [x for x in nendo_list if x]
    # nendo_listを昇順（年度の古いが先）に並び替える
    for y in nendo_list:
        y = int(y)
    nendo_list.sort()
    # df_slice_perspectiveに積算したperspective2の項目の列を追加する
    for z in k2:
        for y in nendo_list:
            new_col_name = '積算' + str(z)
            df2[(new_col_name, z)] = df2[z, y].cumsum()
    func_get_by_perspective3_prepare(k1, k2, nendo_list)


def func_get_by_perspective3_prepare(k1: list, k2: list, nendo_list: list):
    # step-6:各項目の特定期間の平均を算出する・・事前準備（特定期間の設定）
    # 比較した年度・期間の設定
    # ①比較したい期間の初年度
    compare_year_start1 = '2008'
    compare_year_end1 = '2020'

    year_ave_list = []
    for i in range(2008, 2021):
        year_ave_list.append(('平均気温', i))
    print(year_ave_list)



    g = df3.groupby(['月日'])[[('平均気温', '2018'), ('平均気温', '2019'), ('平均気温', '2020')]].mean()
    # print(g.apply(lambda a: a[:]), type(g))
    # print(g.mean(axis=1))
    df3[('平均気温_暖冬平均', '2018-2020')] = g.mean(axis=1)
    # Dataframeの数値を小数点以下1桁に揃える
    pd.options.display.float_format = '{:.1f}'.format
    # print(df3)
    df3.to_csv('bbb.csv', encoding='shift-jis', index_label=None)


if __name__ == '__main__':
    # step-1:比較する期間の開始日と終了日を設定する・・OK
    # step-2:各年度の開始日と終了日にあたる行番号を特定し、各年度の対象データを抽出する・・OK
    # step-3:各年度の抽出データから項目毎のdataframeを作成する・・OK
    # step-4:比較年度の項目毎dataframeをまとめる・・OK
    # step-5:平均気温、日照時間は積算演算したdataframeを追加する・・OK
    # step-6:各項目の2018～2020年平均（暖冬3年）、2008～2020年平均を抽出、グラフ化の元dataframeに追加する
    # step-7:グラフ化元dataframeから比較グラフを作成する

    # step-1:比較する期間の開始日と終了日を設定する
    # 開始日（本年度）：kikan_start ex.'2022/9/15'
    # 終了日（本年度）：kikan_end ex.'2023/2/28'
    kikan_start = '2022/9/15'
    kikan_start = datetime.datetime.strptime(kikan_start, '%Y/%m/%d')
    # 開始日からの期間（月）で終了日を決定・・修正
    kikan_range_month = '5'
    over_month = kikan_start.month + int(kikan_range_month) - 12
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
