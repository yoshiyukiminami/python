import glob
import pprint
import re
import pandas as pd
from PIL import Image, ExifTags
from exif import Image

# 座標フォーマット変換（ref -> N：北緯｜S：南緯｜W：西経｜E：東経）
def convert_dms_to_dd(dms, ref):
    dd = dms[0] + dms[1]/60 + dms[2]/(60*60)
    if ref == 'S' or ref == 'W':
        dd = dd * -1
    return dd


# Exif情報から座標情報を取得（途中、座標フォーマット変換関数あり）
def get_coordinates(image):
    latitude = None
    longitude = None
    # 緯度の変換
    if hasattr(image, 'gps_latitude_ref') and hasattr(image, 'gps_latitude'):
        # N or S（北緯 or 南緯）
        latitude_ref = image.gps_latitude_ref
        latitude = convert_dms_to_dd(image.gps_latitude, latitude_ref)
    # 経度の変換
    if hasattr(image, 'gps_longitude_ref') and hasattr(image, 'gps_longitude'):
        # W or E（西経 or 東経）
        longitude_ref = image.gps_longitude_ref
        longitude = convert_dms_to_dd(image.gps_longitude, longitude_ref)
    return latitude, longitude


# 取得したExif情報の中にある無効文字列の排除
def illegal_char_remover(data):
    illegal_characters_re = re.compile(
        r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')
    """Remove ILLEGAL CHARACTER."""
    if isinstance(data, str):
        return illegal_characters_re.sub("", data)
    else:
        return data


if __name__ == '__main__':
    # Step-1 フォルダにある画像（jpeg）を読み込む
    # 定数
    # 読み込むデータを特定するfolder-pathをfiledirに設定する
    picture_dir = 'C:/Users/minam/Desktop/hojyo_picture_diagnosis/'
    picture_save_dir = 'C:/Users/minam/Desktop/hojyo_picture_save/'
    # フォルダー内にあるフォルダー名をfolderlist、ファイル名をfilesに所得する
    pictures = glob.glob(picture_dir + '/*.jpeg', recursive=True)
    pprint.pprint(pictures)

    # # 出力したいExif情報の対応辞書
    # odic = {'GPSInfo': 34853,
    #         'ResolutionUnit': 296,
    #         'ExifOffset': 34665,
    #         'Model': 272,
    #         'Software': 305,
    #         'Orientation': 274,
    #         'DateTime': 306,
    #         'YCbCrPositioning': 531,
    #         'XResolution': 282,
    #         'YResolution': 283,
    #         'HostComputer': 316,
    #         }
    #
    # df = pd.DataFrame(columns=list(odic.keys()))

    # 画像の取得
    for picture in pictures:
        with open(picture, 'rb') as f:
            image = Image(f)
            if image.has_exif == True:
                latitude, longitude = get_coordinates(image)
                print(latitude, longitude)
            else:
                print('Exif データが取得できません')

        # # Exif情報の取得
        # exif_dict = image.getexif()
        # print(exif_dict)
        # edic = dict()
        # for id, value in exif_dict.items():
        #     edic[id] = value
        # # edicから欲しい情報だけをadicに転記
        # adic = dict()
        # for out_key in odic.keys():
        #     if odic[out_key] in edic.keys():
        #         adic[out_key] = edic[odic[out_key]]
        #     else:
        #         # exif情報がない場合
        #         adic[out_key] = '-'

        # # dfにデータを格納
        # for key in adic.keys():
        #     df.at[image, key] = adic[key]
        # exif = [TAGS.get(k, "Unknown") + f": {str(v)}" for k, v in exif_dict.items()]
        # print(exif)
        # exif_str = "\n".join(exif)
        # print(exif_str, type(exif_str), "===")

    # # df書き出し(PILの場合、時々pandasで書き出せない文字が混じるので除去する)
    # df = df.applymap(illegal_char_remover)
    # df.to_excel("df.xlsx", encoding='Shift-JIS')
