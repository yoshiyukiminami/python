import csv
import datetime
import glob
import pandas as pd

def data_back_stitch(df_csv, error_index_name):
    print(df_csv[error_index_name], type(df_csv[error_index_name]))
    # 平均気温、最高気温、最低気温のみ数値を補正、それ以外は「0」を代入
    error_line = df_csv[error_index_name]
    idx = {}  # [平均材料1, 修正パンチイン, 修正パンチアウト, 平均材料2]
    punch_in = False
    for i, val in enumerate(error_line.isnull()):
        if not punch_in and val is True:
            idx["mean1"] = i - 1
            idx["punch_in"] = i
            punch_in = True
        if punch_in and val is False:
            idx["punch_out"] = i - 1
            idx["mean2"] = i
            if error_index_name == '平均気温' or error_index_name == '最高気温' or error_index_name == '最低気温':
                for j in range(idx["punch_in"], idx["punch_out"] + 1):
                    figure_count = len(range(idx["punch_in"], idx["punch_out"])) + 2
                    hosei_figure = (error_line[idx["mean2"]] - error_line[idx["mean1"]]) / figure_count
                    if error_line[idx["mean2"]] - error_line[idx["mean1"]] < 0:
                        error_line[j] = error_line[idx["mean1"]] + hosei_figure * j
                    else:
                        error_line[j] = error_line[idx["mean1"]] - (hosei_figure * j)
                    df_csv = data_back_stitch(df_csv, idx["mean2"])
                break
            else:
                for j in range(idx["punch_in"], idx["punch_out"] + 1):
                    error_line[j] = 0
    print(error_line)

    return df_csv


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
        print(save_name)
        df_climate.to_csv(save_name, encoding='Shift-JIS')

    # 空白の補正（平均気温、最高気温、最低気温とその品質・均質情報のみ）
    # climate_data_saveフォルダー内にあるファイルをfile2に取得
    files2 = glob.glob(save_filedir + '/*.csv', recursive=True)
    for file2 in files2:
        df_csv = pd.read_csv(file2, encoding='Shift-JIS')
        df_csv_check = df_csv[['平均気温', '平均気温（品質）', '平均気温（均質）',
                               '最高気温', '最高気温（品質）', '最高気温（均質）',
                               '最低気温', '最低気温（品質）', '最低気温（品質）']]
        df_csv_check = df_csv_check.isnull().any()
        for index, value in enumerate(df_csv_check):
            if value is True:
                error_index_name = str(df_csv_check.index[index])
                error_msg1 = error_index_name + "に欠損値があるため、修正が必要です。"
                print(error_msg1)
                # 欠損値を補正する関数
                df_csv = data_back_stitch(df_csv, error_index_name)
            else:
                print("欠損値はありません")

    # 補正したdf_csvをclimate_data_save_hoseiフォルダーに再保存（保存名は変更）
    save_name_hosei = save_filedir + '気象元データ_2008-2023_' + kansoku_point + '_hosei.csv'
    print(save_name_hosei)
    # df_csv_hosei.to_csv(save_name, encoding='Shift-JIS')
