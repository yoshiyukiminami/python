# Step-1 soil_chemical_propertiesフォルダにある測定データ（xlsx）から基本情報を読み込む
# Step-2 基本情報を抽出し、PPTXのfield_propertiesを生成する
# Step-3 圃場測定時画像フォルダにある画像データを読み込む
# Step-4 Step-2のfield_prppertiesに該当画像を追加する
import pandas as pd
import glob
import os
import pprint
from pptx import Presentation
from diagnosis.domain.field_property import FieldProperty


if __name__ == '__main__':
    # Step-1 フォルダにある測定データ（xlsx）を読み込む
    # 読み込むデータを特定するfolder-pathをfiledirに設定する
    filedir = 'C:/Users/minam/Desktop/soil_chemical_properties/'
    # フォルダー内にあるフォルダー名をfolderlist、ファイル名をfilesに所得する
    folderlist = os.listdir(filedir)
    print(folderlist)
    files = glob.glob(filedir + '/**/*.xlsx', recursive=True)
    pprint.pprint(files)

    # 【Step-1-1】フォルダにある測定データ（.xlsx）から基本情報を読み込む
    for file in files:
        df = pd.read_excel(file, sheet_name='基本情報')
        df = df.loc[:, ['ID', '出荷団体名', '生産者名', '圃場名', '面積（㎡）', '圃場位置(緯度)', '圃場位置(経度)', '品目名', '作型']]
        # 「土壌化学性データ」シートから必要情報の取得
        df2 = pd.read_excel(file, sheet_name='土壌化学性データ')
        df2 = df2.loc[:, ['ID', '採土日', '採土法']]
        # 「土壌物理性データ」シートから必要情報の取得
        df3 = pd.read_excel(file, sheet_name='土壌物理性データ')
        df3 = df3.loc[:, ['ID', '測定日', '測定法', '測定状態']]
        # 【Step-1-2】取得データの結合（キー列'ID'）と欠損値の判定
        alldf = pd.merge(pd.merge(df, df2, left_on='ID', right_on='ID'), df3, left_on='ID', right_on='ID')
        # print(alldf)
        isvalid = True
        for i in range(len(alldf)):
            if alldf.loc[i].isnull().any():
                print("欠損値のある行が含まれています")
                isvalid = False
            else:
                print("必要情報は正常です")
                # 【Step-1-3】画像タイトルおよび圃場名、採土日、測定日の取得
                df_title = alldf.loc[i]
                # print(df_title)
                picture_titles = df_title[['ID', '出荷団体名', '生産者名', '圃場名', '品目名', '作型']].values
                picture_title = '基本情報_' + '_'.join(picture_titles)
                # print(picture_title)
                hojyomei = df_title[['圃場名']].values
                # print(hojyomei)
                saidobi = df_title[['採土日']].values
                # print(saidobi)
                sokuteibi = df_title[['測定日']].values
                # print(sokuteibi)
