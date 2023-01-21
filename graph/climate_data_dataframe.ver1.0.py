import csv
import datetime
import glob
import numpy as np
import pandas as pd


def back_stitch3(line: list, line_name: str, offset: int = 0) -> list:
    """
    返し縫いのように平均値で埋めていく
    :param line_name: 補正される対象列の名前
    :param line: 補正される対象（1列分のデータ）
    :param offset: カーソルの初期位置（例：100列処理するうち20列目から開始に19を指定）
    :return: 修正後の line
    """
    if offset != len(line):
        idx = {}  # [平均材料1, 修正パンチイン, 修正パンチアウト, 平均材料2]
        punch_in = False
        for col, value in enumerate(line[offset::]):
            if not punch_in and np.isnan(value):
                idx["mean1"] = offset + col - 1
                idx["punch_in"] = offset + col
                punch_in = True
            if punch_in and not np.isnan(value):
                idx["punch_out"] = offset + col - 1
                idx["mean2"] = offset + col
                # print(idx, "idx")
                if line_name == '平均気温' or line_name == '最高気温' or line_name == '最低気温':
                    how_many_times = max(idx["mean1"], idx["mean2"]) - min(idx["mean1"], idx["mean2"]) + 1
                    # print(how_many_times, "how_many_times")
                    tolerance = np.linspace(line[idx["mean1"]], line[idx["mean2"]], how_many_times)
                    # print(tolerance, "tolerance")
                    for i, n_value in enumerate(tolerance):
                        line[idx["mean1"] + i] = n_value
                    line = back_stitch3(line, line_name, idx["mean2"])
                    break
                elif line_name == '平均気温（品質）' or line_name == '平均気温（均質）':
                    for j in range(idx["punch_in"], idx["punch_out"] + 1):
                        line[j] = 0
                    line = back_stitch3(line, line_name, idx["mean2"])
                    break
                elif line_name == '最高気温（品質）' or line_name == '最高気温（均質）':
                    for j in range(idx["punch_in"], idx["punch_out"] + 1):
                        line[j] = 0
                    line = back_stitch3(line, line_name, idx["mean2"])
                    break
                elif line_name == '最低気温（品質）' or line_name == '最低気温（均質）':
                    for j in range(idx["punch_in"], idx["punch_out"] + 1):
                        line[j] = 0
                    line = back_stitch3(line, line_name, idx["mean2"])
                    break
                else:
                    break
    return line


def find_invalid_data(file2: str):
    """
    shift-jisを前提としたcsvを読み込み、欠損値（NaN）を含む行をlistで返す\n
    step1: 列単位で欠損値（NaN）の有無を検知する\n
    step2: 欠損値（NaN）を含む列のデータをline：listで関数（back_stitch）に渡す\n
    step3: 関数（back_stitch）では欠損値（NaN）に補正値を代入する\n
    :param file2: CSVパス
    :return:
    """
    # 補正されたデータをrecords、列名をrecords2に追加してリスト化
    records = []
    records2 = []
    # 受けたPath名から所定のcsvファイルを読み込む
    df_csv = pd.read_csv(file2, encoding='shift-jis')
    df_csv_nan_any = df_csv.isnull().any()
    for k, item in enumerate(df_csv_nan_any):
        if item is True:
            line_name = str(df_csv_nan_any.index[k])
            print(line_name + f"に欠損値（NaN）が含まれています。")
            line = list(df_csv[df_csv_nan_any.index[k]])
            records2.append(line_name)
            records.append(back_stitch3(line, line_name))
    return records, records2, df_csv

if __name__ == '__main__':
    # 定数
    filedir = 'C:/Users/minam/Desktop/climate_data_dl/'
    save_filedir = 'C:/Users/minam/Desktop/climate_data_save/'
    save_hosei_filedir = 'C:/Users/minam/Desktop/climate_data_save_hosei/'

    # DATAFRAMEの原型alldf（辞書型）
    alldf = {'観測地点': [], '年月日': [],
             '平均気温': [], '平均気温（品質）': [], '平均気温（均質）': [],
             '日照時間': [], '日照時間（品質）': [], '日照時間（均質）': [],
             '最高気温': [], '最高気温（品質）': [], '最高気温（均質）': [],
             '最低気温': [], '最低気温（品質）': [], '最低気温（均質）': [],
             '降水量の合計': [], '降水量の合計（品質）': [], '降水量の合計（均質）': [],
             '1時間降水量の最大': [], '1時間降水量の最大（品質）': [], '1時間降水量の最大（均質）': []
             }

    # climate_data_dlフォルダー内にあるファイルをfilesに取得
    files = glob.glob(filedir + '/*.csv', recursive=True)
    # ファイル名から観測地点を特定
    isvalid = True
    for file in files:
        with open(file, newline='') as f:
            reader = csv.reader(f)
            row_list = [row for row in reader]
            sokutei_point_list = row_list[2][1:]
            # 観測地点名の取得とファイルに観測地点が複数ある場合、プログラムを中断する
            if len(set(sokutei_point_list)) == 1:
                sokutei_point = sokutei_point_list[0]
            else:
                print("ファイルに複数の測定地点があります")
                isvalid = False
            data_list = row_list[6:]
            for data in data_list:
                alldf['観測地点'].append(sokutei_point)
                alldf['年月日'].append(datetime.datetime.strptime(data[0], '%Y/%m/%d'))
                alldf['平均気温'].append(data[1])
                alldf['平均気温（品質）'].append(data[2])
                alldf['平均気温（均質）'].append(data[3])
                alldf['日照時間'].append(data[4])
                alldf['日照時間（品質）'].append(data[5])
                alldf['日照時間（均質）'].append(data[6])
                alldf['最高気温'].append(data[7])
                alldf['最高気温（品質）'].append(data[8])
                alldf['最高気温（均質）'].append(data[9])
                alldf['最低気温'].append(data[10])
                alldf['最低気温（品質）'].append(data[11])
                alldf['最低気温（均質）'].append(data[12])
                alldf['降水量の合計'].append(data[13])
                alldf['降水量の合計（品質）'].append(data[14])
                alldf['降水量の合計（均質）'].append(data[15])
                alldf['1時間降水量の最大'].append(data[16])
                alldf['1時間降水量の最大（品質）'].append(data[17])
                alldf['1時間降水量の最大（均質）'].append(data[18])

    df_climate = pd.DataFrame(alldf)
    # 2つ以上の観測地点が混在している場合に警告（処理中断）、OKの場合はCSVファイルでSAVEホルダーに保存
    kansoku_point_list = df_climate['観測地点']
    if not len(set(kansoku_point_list)) == 1:
        print("警告：観測地点が複数あります。")
        isvalid = False
    else:
        kansoku_point = kansoku_point_list[0]
        df_climate = df_climate.sort_values(by="年月日")
        df_climate = df_climate.reset_index(drop=True)
        # 保存ファイル名の生成
        save_name = save_filedir + '気象元データ_2008-2023_' + kansoku_point + '.csv'
        df_climate.to_csv(save_name, encoding='Shift-JIS', index=False)

    # 空白の補正（平均気温、最高気温、最低気温とその品質・均質情報のみ）
    # climate_data_saveフォルダー内にあるファイルをfile2に取得
    files2 = glob.glob(save_filedir + '/*.csv', recursive=True)
    for file2 in files2:
        records, records2, df_csv = find_invalid_data(file2)
        df_climate_exchange = pd.DataFrame(records).T.set_axis(records2, axis='columns')
        # print(df_csv, "処理対象")
        # print(df_climate_exchange)
        for target_column in df_csv.columns.intersection(df_climate_exchange.columns):
            # print(target_column, "更新中")
            for i, value in enumerate(df_csv[target_column]):
                df_csv[target_column][i] = df_climate_exchange[target_column][i]
                # print(df_csv[target_column][i], "置換結果")
        # df_csv.to_csv('df_csv_exchange.csv', encoding='Shift-JIS')

        save_name_hosei = save_hosei_filedir + '気象元データ_2008-2023_' + kansoku_point + '_hosei.csv'
        df_csv.to_csv(save_name_hosei, encoding='shift-jis', index=True)
        print('欠損値修正版の出力が完了しました')
