# ver1.1・・ver1.0に対して年度毎にスライスした期間データを辞書型のDataframeに格納し、そこから必要データを抽出してグラフ化するアプローチ
# step-1:比較する期間の開始日と終了日を設定する・・if__name__
# step-2:各年度の開始日と終了日にあたる行番号を特定し、各年度の対象データを抽出する・・if__name__
# step-3:期間でスライスされた測定データからグラフ化に必要な項目を取り出す・・func_get_by_perspective
# step-4:step-3のDataframeに積算演算追加（平均気温、日照時間のみ）する・・:def func_add_column_cumsum
# step-5:step-4のDataframeを辞書（all_slice）に格納、Dataframeとしてstep-6に受け渡し・・func_save_df_slice_as_dict
# step-6:step-5のDataframeに2018～2020年平均（暖冬3年）を追加追加する・・func_add_column_mean1 + set_term1
# step-7:step-6のDataframeに2008～2020年平均（過去12年）を追加する・・func_add_column_mean2 + set_term2
# step-8-1:格納されたdict型Dataframeからグラフ化に必要な系列を抽出し、グラフA（今年・昨年・3年平均・12年平均比較）を作成する
# step-8-2:格納されたdict型Dataframeからグラフ化に必要な系列を抽出し、グラフB（今年・昨年～5年前比較）を作成する
import collections
import datetime
import glob
import re
import pandas as pd
from dateutil.relativedelta import relativedelta


def func_get_by_perspective(df: pd.DataFrame, k1: list, k2: list, year: int):
    # step-3:期間でスライスされた測定データからグラフ化に必要な項目を取り出す
    # df:期間でスライスされたDataframe、k1:抽出する項目、k2：積算を追加する項目、year：dfの年度
    # dfの「年月日」列から月日に変換した列を追加
    # todo:chain-indexing警告の解除
    df.loc[:, '月日'] = df.loc[:, '年月日'].dt.strftime('%m-%d')
    # yearから年度列を追加
    df.loc[:, '年度'] = str(year)
    # 月日表示を元に戻す際の昇順崩れ防止に1から連番を降った新しい列（列名：No）を追加し、先頭列に挿入する
    new_col_no = pd.Series(range(1, len(df.index) + 1), index=df.index)
    df.insert(0, 'No', new_col_no)
    # dfをpivot_tableに変換（wide型、df_pivot:Dataframe）
    df_pivot = pd.pivot_table(df, index=['No', '月日'], columns='年度', values=k1)
    # Multi-columnの名前を変更（level=0が'None'→'項目'、level=1はそのまま）
    df_pivot.columns.set_names(['項目', '年度'], inplace=True)
    func_add_column_cumsum(df_pivot, k2, year)


def func_add_column_cumsum(df1: pd.DataFrame, k2: list, year: int):
    # step-4:項目（カラム名・level=0）からk2項目のみ積算演算した列を追加する
    # df1に積算した項目列を追加する
    for koumoku in k2:
        new_col_name = '積算' + koumoku
        df1.loc[:, (new_col_name, str(year))] = df1[koumoku, str(year)].cumsum()
    # df1.to_csv('df1.csv', encoding='shift-jis')
    func_save_df_slice_as_dict(df1, year)


def func_save_df_slice_as_dict(df2: pd.DataFrame, year: int):
    # step-5:step-4のDataframeを辞書（all_slice）に格納、Dataframeとしてstep-6に受け渡し
    print(df2, year, type(year))
    all_slice = {}


def func_add_column_mean1(df2: pd.DataFrame):
    # step-5:step-4のDataframeに2018～2020年平均（暖冬3年）を追加追加する
    for col in df2.columns:
        print(col)
        compare_term1, compare_term1_start, compare_term1_end = func_add_column_mean1_set_term1(col)
        new_col_name = (col[0] + "_比較期間_A", str(compare_term1_start + '-' + compare_term1_end))
        print(new_col_name)
        df_ave1 = df2.groupby(['月日'])[compare_term1].mean()
        # print(df_k_ave.apply(lambda a: a[:]), type(g))
        # print(df_k_ave.mean(axis=1))
        # 平均した数値を元のdf3に新しい列として追加する
        df2[new_col_name] = df_ave1.mean(axis=1)
        # Dataframeの数値を小数点以下1桁に揃える
        # todo:表示変化せず
        pd.options.display.float_format = '{:.1f}'.format
    # print(df2)
    # df2.to_csv('bbb.csv', encoding='shift-jis')
    func_add_column_mean2(df2)


def func_add_column_mean2(df3: pd.DataFrame, koumokus: list, years: list):
    # step-6-2:各項目の特定期間の平均を算出する（比較データ列の作成）
    for koumoku in koumokus:
        compare_term2, compare_term2_start, compare_term2_end = func_add_column_mean2_prepare(koumoku, years)
        new_col_name = (koumoku + "_比較期間_B", str(compare_term2_start + '-' + compare_term2_end))
        df_k_ave = df3.groupby(['月日'])[compare_term2].mean()
        # print(df_k_ave.apply(lambda a: a[:]), type(g))
        # print(df_k_ave.mean(axis=1))
        # 平均した数値を元のdf3に新しい列として追加する
        df3[new_col_name] = df_k_ave.mean(axis=1)
    # Dataframeの数値を小数点以下1桁に揃える
    # todo:表示変化せず
    pd.options.display.float_format = '{:.1f}'.format
    # print(df3)
    # df3.to_csv('ccc.csv', encoding='shift-jis')
    func_reset_index_month(df3)


def func_reset_index_month(df_pregraph: pd.DataFrame):
    # 年またぎ対応のために変更した月日の表示（例：13月）を元の月表示に戻す
    reset_index = []
    for i in df_pregraph.index:
        # 月日（index）の先頭2文字（月）から12を引いた数字を生成（年またぎの13月～の表現をリセット）
        d1 = str(int(i.split('-')[0]) - 12).zfill(2)
        # 月日の先頭2文字=月が13～29の場合、月数字から12を引いた数字に置換、それ以外はそのまま
        reset_index.append(re.sub(r'(^1[3-9]|^2[0-9])', d1, i))
    df_pregraph['月日'] = [month for month in reset_index]
    df_pregraph.set_index(df_pregraph['月日'], inplace=True)
    df_pregraph.to_csv('df_pregraph.csv', encoding='shift-jis')
    # print(df_pregraph)


def func_add_column_mean1_set_term1(koumokus: list):
    # 比較データ列の設定期間を決める関数・・その1
    # 設定期間①：暖冬シーズン
    # 比較年の開始日・終了日の設定・・アナログ
    compare_term1_start = '2018'
    compare_term1_end = '2020'
    # 設定年のエラー検知（Dataframeにない年度の選択、無効な設定期間：開始年の方が新しいや同じ年の選択）
    # koumokusの年度をリストに取り出す
    year_list = []
    for y in koumokus:
        print(y, type(y))
        year_list.append(y[0])
    print(year_list)
    if compare_term1_start not in year_list:
        print("開始年が対象年にありませんので、以下のリストから再選択してください。")
        print(year_list)
    else:
        if compare_term1_end not in year_list:
            print("終了年が対象年にありませんので、以下のリストから再選択してください。")
            print(year_list)
        else:
            if int(compare_term1_end) - int(compare_term1_start) <= 0:
                print("開始年と終了年が同じか、無効な期間設定になっています。")
            else:
                compare_term1 = []
                for j in range(int(compare_term1_start), int(compare_term1_end) + 1):
                    compare_term1.append((koumoku_basic, str(j)))
                return compare_term1, compare_term1_start, compare_term1_end


def func_add_column_mean2_prepare(koumokus: list, year: list):
    # 比較データ列の設定期間を決める関数・・その2
    # 設定期間②：13年シーズン
    # 比較年の開始日・終了日の設定・・アナログ
    compare_term2_start = '2008'
    compare_term2_end = '2021'
    # 設定年のエラー検知（Dataframeにない年度の選択、無効な設定期間：開始年の方が新しいや同じ年の選択）
    if compare_term2_start not in year:
        print("開始年が対象年にありませんので、以下のリストから再選択してください。")
        print(year)
    else:
        if compare_term2_end not in year:
            print("終了年が対象年にありませんので、以下のリストから再選択してください。")
            print(year)
        else:
            if int(compare_term2_end) - int(compare_term2_start) <= 0:
                print("開始年と終了年が同じか、無効な期間設定になっています。")
            else:
                compare_term2 = []
                for j in range(int(compare_term2_start), int(compare_term2_end) + 1):
                    compare_term2.append((koumokus, str(j)))
                return compare_term2, compare_term2_start, compare_term2_end


if __name__ == '__main__':
    # step-1:比較する期間の開始日と終了日を設定する
    # 開始日（本年度）：kikan_start ex.'2022/9/15'
    kikan_start = '2022/9/15'
    kikan_start = datetime.datetime.strptime(kikan_start, '%Y/%m/%d')
    # 開始日からの期間（月）で終了日を決定・・修正
    kikan_range_month = '5'
    # グラフ作成する項目を選定（不要な品質、均質情報の項目は除く）
    # perspective1:グラフ化する項目、perspective2:積算する項目
    perspectives1 = ['平均気温', '日照時間', '最高気温', '最低気温', '降水量の合計', '1時間降水量の最大']
    perspectives2 = ['平均気温', '日照時間']
    # climate_data_save_hoseiフォルダー内にあるファイルをfilesに取得
    filedir = 'C:/Users/minam/Desktop/climate_data_save_hosei/'
    files = glob.glob(filedir + '/*.csv', recursive=True)
    print(files)

    # ファイル名から観測地点を特定
    isvalid = True
    # 同じ観測地点が複数のファイルに含まれていた場合（エラー）の回避
    kansoku_points = []
    for file in files:
        with open(file, newline='') as f:
            df = pd.read_csv(f, index_col=0)
            sokutei_point_list = [col for col in df.iteritems()]
            sokutei_point_list = sokutei_point_list[0][1:]
            # 観測地点名の取得とファイルに観測地点が複数ある場合、プログラムを中断する
            if len(set(sokutei_point_list[0][1:])) == 1:
                print("OK:観測地点は一つです")
                kansoku_points.append(sokutei_point_list[0][1])
                # dfの日付列をまとめてdatetime型に変換する
                df['年月日'] = pd.to_datetime(df['年月日'])
                # 変換したdfから日付（期間）でスライスする
                # 期間開始・終了を年毎に取得する
                for loop_year in range(2008, kikan_start.year + 1):
                    temp_kikan_start = datetime.datetime.strptime(f"{loop_year}-{kikan_start.month}-{kikan_start.day}",
                                                                  '%Y-%m-%d')
                    temp_kikan_end = temp_kikan_start + relativedelta(months=int(kikan_range_month))
                    df_slice_loop = df[df['年月日'].isin(pd.date_range(temp_kikan_start, temp_kikan_end))]
                    # print(df_slice_loop)
                    func_get_by_perspective(df_slice_loop, perspectives1, perspectives2, loop_year)
            else:
                print("NG:ファイルに複数の観測地点があります")
                isvalid = False


    # kansoku_pointsにファイル毎の観測地点をリスト化し、要素個数と重複要素数の差があればエラーメッセージ（重複あり→エラー）
    if not len(kansoku_points) == len(collections.Counter(kansoku_points)):
        print("NG:複数のファイルに同じ観測地点が含まれています")
        isvalid = False
    else:
        print("OK:ファイルに重複した観測地点はありません")
