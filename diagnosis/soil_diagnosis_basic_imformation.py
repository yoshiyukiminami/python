# Step-1 soil_chemical_propertiesフォルダにある測定データ（xlsx）から基本情報を読み込む
# Step-2 基本情報を抽出し、PPTXのfield_propertiesを生成する
# Step-3 圃場測定時画像フォルダにある画像データを読み込む
# Step-4 Step-2のfield_prppertiesに該当画像を追加する
import datetime
import glob
import os
import pprint
import pandas as pd
from pptx import Presentation
from pptx.util import Cm
from pptx.enum.text import MSO_AUTO_SIZE


def make_index(alldf, df_title):
    prs = Presentation()
    # 1ページ目に「タイトル」スライドのレイアウトを指定
    slide_layout_0 = prs.slide_layouts[0]
    slide_1 = prs.slides.add_slide(slide_layout_0)
    # 2ページ目に「目次」スライドのレイアウトを指定
    slide_layout_1 = prs.slide_layouts[5]
    slide_2 = prs.slides.add_slide(slide_layout_1)
    # テキストの編集・・「タイトル」スライド
    # 報告日の取得
    d_today = datetime.date.today()
    title = slide_1.placeholders[0]
    title.text = "土壌診断結果報告書"
    subtitle = slide_1.placeholders[1]
    subtitle_text = "Agsoil株式会社\n報告日：" + str(d_today)
    subtitle.text = subtitle_text
    # テキストの編集・・「目次」スライト
    title2 = slide_2.placeholders[0]
    title2.text = "目次"
    # 目次表の生成
    # 表のレイアウト設定
    rows = len(alldf) + 1
    # rows = 26
    cols = 3
    table_shape = slide_2.shapes.add_table(rows, cols, Cm(3), Cm(5), Cm(20), Cm(8))
    # table_shape = slide_2.shapes.add_table(rows, cols, Cm(1), Cm(3), Cm(15), Cm(5))
    table = table_shape.table
    # 列見出しのテキスト設定
    category = ['No', 'ID', '圃場名']
    for i in range(len(category)):
        cell = table.cell(0, i)  # cellオブジェクトの取得
        cell.text = category[i]  # textプロパティで値を設定する
    # alldfから目次を作成する・・ここから
    alldf_indexs = alldf.loc[:, ['ID', '圃場名']]
    for j, alldf_index in alldf_indexs.iterrows():
        cell0 = table.cell(j + 1, 0)  # cellオブジェクトの取得
        cell0.text = str(j + 1)  # textプロパティで値を設定する
        cell1 = table.cell(j + 1, 1)
        cell1.text = str(alldf_index['ID'])
        cell2 = table.cell(j + 1, 2)
        cell2.text = alldf_index['圃場名']
    # PowerPointを保存
    prs.save("output/create_powerpnt.pptx")

def make_picture_table(alldf):
    # 土壌物理性グラフ（jpeg）のリストを読み込む
    filedir1 = 'C:/Users/minam/Desktop/soil_physical_graph2/'
    files_pg = glob.glob(filedir1 + '/**/*.jpeg', recursive=True)
    pprint.pprint(files_pg)
    # 土壌化学性グラフ（jpeg）のリストを読み込む
    filedir2 = 'C:/Users/minam/Desktop/soil_chemical_graph2/'
    files_cg = glob.glob(filedir2 + '/**/*.jpeg', recursive=True)
    pprint.pprint(files_cg)
    # 圃場画像（jpeg）のリストを読み込む
    filedir3 = 'C:/Users/minam/Desktop/hojyo_picture2/'
    files_hp = glob.glob(filedir3 + '/**/*.jpeg', recursive=True)
    pprint.pprint(files_hp)

    # ここから仕掛
    for file_pg in files_pg:
        print(file_pg)
        pg_name = file_pg.split('\\')
        pg_name = pg_name[-1]
        pg_name_id = pg_name.split('_')
        pg_name_id = pg_name_id[1]
        print(pg_name_id)


if __name__ == '__main__':
    # Step-1 フォルダにある測定データ（xlsx）を読み込む
    # 読み込むデータを特定するfolder-pathをfiledirに設定する
    filedir = 'C:/Users/minam/Desktop/soil_chemical_properties/'
    # フォルダー内にあるフォルダー名をfolderlist、ファイル名をfilesに所得する
    folderlist = os.listdir(filedir)
    files = glob.glob(filedir + '/**/*.xlsx', recursive=True)
    pprint.pprint(files)

    # 【Step-1-1】フォルダにある測定データ（.xlsx）から基本情報を読み込む
    for file in files:
        df = pd.read_excel(file, sheet_name='基本情報')
        df = df.loc[:,
             ['ID', '出荷団体名', '生産者名', '圃場名', '面積（㎡）', '圃場位置(緯度)', '圃場位置(経度)', '品目名',
              '作型']]
        # 「土壌化学性データ」シートから必要情報の取得
        df2 = pd.read_excel(file, sheet_name='土壌化学性データ')
        df2 = df2.loc[:, ['ID', '採土日', '採土法']]
        # 「土壌物理性データ」シートから必要情報の取得
        df3 = pd.read_excel(file, sheet_name='土壌物理性データ')
        df3 = df3.loc[:, ['ID', '測定日', '測定法', '測定状態']]
        # 【Step-1-2】取得データの結合（キー列'ID'）と欠損値の判定
        alldf = pd.merge(pd.merge(df, df2, left_on='ID', right_on='ID'), df3, left_on='ID', right_on='ID')
        print(alldf, type(alldf))
        # alldf.to_csv('aaa')
        # IDをキー列にして昇順ソート、インデックスもリセット
        alldf = alldf.sort_values(by="ID")
        alldf = alldf.reset_index()
        # sortができていない【課題】
        isvalid = True
        for i in range(len(alldf)):
            if alldf.loc[i].isnull().any():
                print("欠損値のある行が含まれています")
                isvalid = False
            else:
                print("必要情報は正常です")
                # 【Step-1-3】画像タイトルおよび圃場名、採土日、測定日の取得
                df_title = alldf.loc[i]
                picture_titles = df_title[['ID', '出荷団体名', '生産者名', '圃場名', '品目名', '作型']].values
                picture_title = '基本情報_' + '_'.join(picture_titles)
                hojyomei = df_title[['圃場名']].values
                saidobi = df_title[['採土日']].values
                sokuteibi = df_title[['測定日']].values
        # ひな形のPPTXを読み込み目次を作成
        make_index(alldf, df_title)
        make_picture_table(alldf)

