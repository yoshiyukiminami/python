# ver1.1・・ver1.0に対して年度毎にスライスした期間データを辞書型のDataframeに格納し、そこから必要データを抽出してグラフ化するアプローチ
# step-1:比較する期間の開始日と終了日を設定する・・if__name__
# step-2:各年度の開始日と終了日にあたる行番号を特定し、各年度の対象データを抽出する・・if__name__
# step-3:すべてのデータを辞書型Dataframe（alldf）に格納し、df_allとしてcsv保存・・save_alldf_as_dataframe
# step-4:期間でスライスされた測定データからグラフ化に必要な項目を取り出す・・func_get_by_perspective
# step-5:step-4のDataframeに積算演算追加（平均気温、日照時間のみ）する・・:def func_add_column_cumsum
# step-6:step-5のDataframeに2018～2020年平均（暖冬3年）を追加追加する・・func_add_column_mean1&prepare
# step-7:step-6のDataframeに2008～2020年平均（過去12年）を追加する・・func_add_column_mean2&prepare
# step-8:step-7のDataframeを年度毎に辞書型Dataframeに格納する・・func_save_df_slice_as_dict_dataframe
# step-9-1:格納されたdict型Dataframeからグラフ化に必要な系列を抽出し、グラフA（今年・昨年・3年平均・12年平均比較）を作成する
# step-9-2:格納されたdict型Dataframeからグラフ化に必要な系列を抽出し、グラフB（今年・昨年～5年前比較）を作成する

import datetime
import glob
import re
import pandas as pd
from dateutil.relativedelta import relativedelta


def func_get_by_perspective(df: pd.DataFrame, k1: list, k2: list, month: int):
    # df:元のDataframe、k1:抽出する項目、k2：積算を追加する項目、month：年をまたぐ月数
    # dfの「年月日」列から月日に変換した列を追加
    df['月日'] = df['年月日'].dt.strftime('%m-%d')
    # monthがプラスの時（＝年またぎあり）のみ年をまたぐ期間対策を発動する
    if month > 0:
        # 年をまだぐ期間設定対策1として、1月以降を13月～（∔12）に変更し、1月以降の月日が12月31日以降に配列されるようにする
        # seiki_hyogenに表示を変更する文字列を指定
        seiki_hyogen = "^0" + "[" + "1-" + str(month + 1) + "]"
        df['月日'] = [f"{re.sub(seiki_hyogen, f'{12 + int(x[:month])}', x)}" for x in df['年月日'].dt.strftime('%m-%d')]
        # 年をまたぐ期間設定対策2として、1月以降が入る期間設定の場合、1月以降のデータも年度としては12月までの年度に含む
        df['年度'] = [(x - relativedelta(months=month + 1)).strftime('%Y') for x in df['年月日']]
        print("年またぎ有り")
    else:
        # dfの「年月日」列から月日に変換した列を追加
        df['年度'] = df['年月日'].dt.strftime('%Y')
        print("年またぎ無し")
    # df_slide_allをpivot_tableに変換（wide型）
    df_pivot = pd.pivot_table(df, index='月日', columns='年度', values=k1)
    # 月日表示を元に戻す際の昇順崩れ防止に1から連番を降った新しい列（列名：No）を追加し、先頭列に挿入する
    new_col_no = pd.Series(range(1, len(df_pivot.index) + 1), index=df_pivot.index)
    df_pivot.insert(0, 'No', new_col_no)
    func_add_column_cumsum(df_pivot, k1, k2)


def func_add_column_cumsum(df2: pd.DataFrame, k1: list, k2: list):
    # step-5:k2リストの項目のみ、積算演算した列を追加する
    # df2のカラム名（マルチカラムのlevel=1）から年度のリスト(year_list)を生成する
    year_list = set(df2.columns.droplevel(level=0))
    year_list = [x for x in year_list if x]
    # year_listを昇順（年度の古いが先）に並び替える
    for y in year_list:
        int(y)
    year_list.sort()
    # df_slice_perspectiveに積算したperspective2の項目の列を追加する
    # 新しく作成した積算用の列名をリスト（new_col_names）に追加し、次の関数に渡す
    new_col_names = []
    for z in k2:
        for y in year_list:
            new_col_name = '積算' + str(z)
            new_col_names.append(new_col_name)
            df2[(new_col_name, y)] = df2[z, y].cumsum()
    new_col_names = list(set(new_col_names))
    func_add_column_mean1(df2, k1, new_col_names, year_list)


def func_add_column_mean1(df2: pd.DataFrame, k1: list, kn: list, year_list: list):
    # 項目リスト（K1）と積算項目リスト（kn）とをk1に結合する
    for j in kn:
        k1.append(j)
    # step-6-1:各項目の特定期間の平均を算出する（比較データ列の作成）
    for k in k1:
        compare_term1, compare_term1_start, compare_term1_end = func_add_column_mean1_prepare(k, year_list)
        new_col_name = (k + "_比較期間_A", str(compare_term1_start + '-' + compare_term1_end))
        df_k_ave = df2.groupby(['月日'])[compare_term1].mean()
        # print(df_k_ave.apply(lambda a: a[:]), type(g))
        # print(df_k_ave.mean(axis=1))
        # 平均した数値を元のdf3に新しい列として追加する
        df2[new_col_name] = df_k_ave.mean(axis=1)
    # Dataframeの数値を小数点以下1桁に揃える
    # todo:表示変化せず
    pd.options.display.float_format = '{:.1f}'.format
    # print(df2)
    # df2.to_csv('bbb.csv', encoding='shift-jis')
    func_add_column_mean2(df2, k1, year_list)


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


def func_add_column_mean1_prepare(koumoku_basic: list, year: list):
    # 比較データ列の設定期間を決める関数・・その1
    # 設定期間①：暖冬シーズン
    # 比較年の開始日・終了日の設定・・アナログ
    compare_term1_start = '2018'
    compare_term1_end = '2020'
    # 設定年のエラー検知（Dataframeにない年度の選択、無効な設定期間：開始年の方が新しいや同じ年の選択）
    if compare_term1_start not in year:
        print("開始年が対象年にありませんので、以下のリストから再選択してください。")
        print(year)
    else:
        if compare_term1_end not in year:
            print("終了年が対象年にありませんので、以下のリストから再選択してください。")
            print(year)
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



def save_alldf_as_dataframe(df: pd.DataFrame):
    # 年毎に取得したデータをall_dfのDataframeに追加していく
    # DATAFRAMEの原型alldf（辞書型）
    alldf = {'観測地点': [], '年月日': [],
             '平均気温': [], '平均気温（品質）': [], '平均気温（均質）': [],
             '日照時間': [], '日照時間（品質）': [], '日照時間（均質）': [],
             '最高気温': [], '最高気温（品質）': [], '最高気温（均質）': [],
             '最低気温': [], '最低気温（品質）': [], '最低気温（均質）': [],
             '降水量の合計': [], '降水量の合計（品質）': [], '降水量の合計（均質）': [],
             '1時間降水量の最大': [], '1時間降水量の最大（品質）': [], '1時間降水量の最大（均質）': []
             }
    for i, data in enumerate(df.itertuples()):
        alldf['観測地点'].append(data[1])
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
    # すべてを取得した辞書型データフレームのalldfをdf_slice_allというDataframeに変換する
    df_all = pd.DataFrame(alldf)
    # 確認用のcsv変換（df_all.csv）
    df_all.to_csv('df_all.csv', encoding='shift-jis')


if __name__ == '__main__':
    # step-1:比較する期間の開始日と終了日を設定する
    # 開始日（本年度）：kikan_start ex.'2022/9/15'
    kikan_start = '2022/9/15'
    kikan_start = datetime.datetime.strptime(kikan_start, '%Y/%m/%d')
    # 開始日からの期間（月）で終了日を決定・・修正
    kikan_range_month = '5'
    # 期間の終了月が年をまたぐかどうか判定（over_monthがプラスの場合、年またぎありで数値が何か月またぐかを示す）
    over_month = kikan_start.month + int(kikan_range_month) - 12
    # グラフ作成する項目を選定（不要な品質、均質情報の項目は除く）
    # perspective1:グラフ化する項目、perspective2:積算する項目
    perspectives1 = ['平均気温', '日照時間', '最高気温', '最低気温', '降水量の合計', '1時間降水量の最大']
    perspectives2 = ['平均気温', '日照時間']
    # climate_data_save_hoseiフォルダー内にあるファイルをfilesに取得
    filedir = 'C:/Users/minam/Desktop/climate_data_save_hosei/'
    files = glob.glob(filedir + '/*.csv', recursive=True)
    print(files)
    # ファイル名から観測地点を特定
    # todo:観測地点（例：菊川牧之原）が2つ以上のファイルに含まれていた場合の処理
    # ヒント：読み込んだCSVファイルを一つのdataframeにまとめて（concat)エラーチェックをする
    isvalid = True
    # 複数ファイルに同じ観測地点がある場合のエラー回避
    kansoku_points = []
    for file in files:
        with open(file, newline='') as f:
            df = pd.read_csv(f, index_col=0)
            sokutei_point_list = [col for col in df.iteritems()]
            sokutei_point_list = sokutei_point_list[0][1:]
            print(sokutei_point_list[0][1])
            # 観測地点名の取得とファイルに観測地点が複数ある場合、プログラムを中断する
            if len(set(sokutei_point_list[0][1:])) == 1:
                print("観測地点は一つです")
                kansoku_points.append(sokutei_point_list[0][1])
            else:
                print("ファイルに複数の観測地点があります")
                isvalid = False

            print(kansoku_points)
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
                save_alldf_as_dataframe(df_slice_loop)
                # 期間でスライスされた測定データからグラフ化に必要な処理をしていく・・関数
                # func_get_by_perspective(df_slice_loop, perspectives1, perspectives2, over_month)
