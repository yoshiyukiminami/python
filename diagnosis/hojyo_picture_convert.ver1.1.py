import glob
import math
import os
import pprint
import re
import numpy as np
import pyexiv2
import pandas as pd
from PIL import Image

def get_datetime(exifdata):
    imagedatetime = exifdata['Exif.Image.DateTime']
    imagedatetime = imagedatetime.split(' ')[0]
    imagedatetime1 = imagedatetime.replace(':', '.')
    imagedatetime2 = imagedatetime.replace(':', '')
    return imagedatetime1, imagedatetime2


# 座標フォーマット変換
def conv_deg(v):
    v_list = re.split('\s', v)
    d_list = v_list[0].split('/')
    m_list = v_list[1].split('/')
    s_list = v_list[2].split('/')
    # 分数を度に変換
    d = float(d_list[0]) / float(d_list[1])
    m = float(m_list[0]) / float(m_list[1])
    s = float(s_list[0]) / float(s_list[1])
    return d + (m / 60.0) + (s / 3600.0)


# Exif情報から座標情報を取得（途中、座標フォーマット変換関数あり）
def get_gpsdata(exifdata):
    # 緯度の変換
    latitude = conv_deg(exifdata['Exif.GPSInfo.GPSLatitude'])
    latitude_ref = exifdata['Exif.GPSInfo.GPSLatitudeRef']
    if latitude_ref != "N":
        latitude = 0 - latitude
    # 経度の変換
    longitude = conv_deg(exifdata['Exif.GPSInfo.GPSLongitude'])
    longitude_ref = exifdata['Exif.GPSInfo.GPSLongitudeRef']
    if longitude_ref != "E":
        longitude = 0 - longitude
    return latitude, longitude


def get_nearest_value(latitude, longitude, imagedatetime1, df_compare):
    list1 = df_compare['圃場位置(緯度)']
    # print(list1)
    list2 = df_compare['圃場位置(経度)']
    # print(list2)
    idx1 = np.abs(np.asarray(list1) - latitude).argmin()
    idx2 = np.abs(np.asarray(list2) - longitude).argmin()
    print(idx1, idx2)
    if idx1 == idx2:
        id = df_compare['ID'][idx1]
        hojyo_name = df_compare['圃場名'][idx1]
        return id, hojyo_name
    else:
        print("一致する座標が無いまたは複数あります。")
        id = "0000-00000-00000"
        hojyo_name = "圃場名不明"
        return id, hojyo_name


def Image_resize(img1, pre_name2):
    print(pre_name2)
    img_width, img_height = img1.size  # 画像のサイズを取得
    # 画像の向き判定
    if img_height < img_width:
        # 絵が横向きの場合、縮小率を計算（w500, h300 の画像を例とします）
        scale = img_width / 533  # e.g. 500 / 512 = 0.98
        size = (533, math.ceil(img_height / scale))  # e.g. (512, 300 / 0.98) → (512, 307)
    else:
        # 絵が縦向きの場合（w300, h500 の画像を例とします）
        scale = img_height / 533
        size = (math.ceil(img_width / scale), 533)  # e.g. (300 / 0.98, 512) → (307, 512)
    # 画像を縮小
    img_resize = img1.resize(size)
    img_resize.save(pre_name2)


if __name__ == '__main__':
    # 定数
    picture_dir = 'C:/Users/minam/Desktop/hojyo_picture_rename_resize/'
    filedir = 'C:/Users/minam/Desktop/soil_chemical_properties/'

    # フォルダー内にある基本情報エクセルファイル（xlsx）を取り込み
    files = glob.glob(filedir + '/**/*.xlsx', recursive=True)
    # pprint.pprint(pictures)
    # pprint.pprint(files)

    # 基本情報から「ID」「座標情報」「圃場名」「採土日」「測定日」を取り出しdf_compareに格納
    for file in files:
        df_comp1 = pd.read_excel(file, sheet_name='基本情報')
        df_comp1 = df_comp1.loc[:, ['ID',  '圃場名', '圃場位置(緯度)', '圃場位置(経度)']]
        # 「土壌化学性データ」シートから必要情報の取得
        df_comp2 = pd.read_excel(file, sheet_name='土壌化学性データ')
        df_comp2 = df_comp2.loc[:, ['ID', '採土日']]
        # 「土壌物理性データ」シートから必要情報の取得
        df_comp3 = pd.read_excel(file, sheet_name='土壌物理性データ')
        df_comp3 = df_comp3.loc[:, ['ID', '測定日']]
        # 【Step-1-2】取得データの結合（キー列'ID'）と欠損値の判定
        df_compare = pd.merge(pd.merge(df_comp1, df_comp2, left_on='ID', right_on='ID'), df_comp3, left_on='ID', right_on='ID')
        print(df_compare)

    # フォルダー内にある画像を取り込み
    pictures1 = glob.glob(picture_dir + '/*.jpeg', recursive=True)
    # 画像の名前自動付与
    for j, picture1 in enumerate(pictures1):
        pre_name1 = picture1
        print(pre_name1)
        with pyexiv2.Image(picture1) as img:
            exifdata = img.read_exif()
            # pprint.pprint(exifdata)
            # EXIFデータから撮影日を取得する関数
            imagedatetime1, imagedatetime2 = get_datetime(exifdata)
            # EXIFデータから撮影場所の座標を取得する関数
            latitude, longitude = get_gpsdata(exifdata)
            id, hojyo_name = get_nearest_value(latitude, longitude, imagedatetime1, df_compare)
            picture_save_name = "圃場画像_" + id + '_' + hojyo_name + '_' + str(j) + '_' + str(imagedatetime2) + ".jpeg"
            os.rename(pre_name1, picture_dir + picture_save_name)

    # 画像のサイズ縮小
    pictures2 = glob.glob(picture_dir + '/*.jpeg', recursive=True)
    for picture2 in pictures2:
        pre_name2 = picture2
        img1 = Image.open(picture2)
        Image_resize(img1, pre_name2)