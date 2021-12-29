# from PIL import Image  #Imageという機能をPILから使うと宣言
# img = Image.open('image_folder_in/モニタリング装置設置場所_野菜くらぶ静岡_20211102.png')  #image_folder_inにあるモニタリング装置・・という名前の画像を開く
# img_resize = img.resize((256, 256))
# img_resize.save('image_folder_out/モニタリング装置設置場所_野菜くらぶ静岡_20211102.png')
# import glob
# import math
# import cv2
# images = glob.glob('./image_folder_in/*')
# print(glob.glob('./image_folder_in/*'))
# for image in images:
#     img = cv2.imread(img)                   # 画像の Height & width を取得
#     img_height,img_width = img.shape[:2]    # 画像の向きを確認
#     if img_height < img_width:              # 縮小率を計算（横向き）
#         scale = img_width / 512             # リサイズするサイズ（横, 縦）を設定（長手は512に固定）
#         size = (512, math.ceil(img_height / scale))
#     else:                                   # 縦向き
#         scale = img_height / 512
#         size = (math.ceil(img_width / scale), 512)  # リサイズするサイズ（横, 縦）を設定（長手は512に固定）
    #cubic_img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)               #縮小、バイキュービック補間
    #cv2.imwrite('dist_sample.jpg', cubic_img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  # 画像を保存（圧縮品質80）

    #img_resize = img.resize((512, img))
    # img.resize(size)
    # tmp = image.split('\\')[-1].split(".")
    # cv2.imwrite('./image_folder_out/' + tmp[0] + "_resize." + tmp[1], img, (cv2.IMWRITE_JPEG_QUALITY, 10))


# import cv2
# def create_resize_photo(long_side_size):
#     # 画像の読み込み
#     img = cv2.imread('sample.jpg')
#     # 画像の Height & width を取得
#     img_height, img_width = img.shape[:2]
#     # 画像の向きを確認
#     if img_height < img_width:  # 横向き
#         # 縮小率を計算
#         scale = img_width / long_side_size
#         # リサイズするサイズ（横, 縦）を設定
#         size = (long_side_size, math.ceil(img_height / scale))
#     else:  # 縦向き
#         scale = img_height / long_side_size
#         size = (math.ceil(img_width / scale), long_side_size)
#     # 画像をリサイズ（縮小、バイキュービック補間）
#     cubic_img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
#     # 画像を保存（圧縮品質80）
#     cv2.imwrite('dist_sample.jpg', cubic_img, [
#                 int(cv2.IMWRITE_JPEG_QUALITY), 80])

import math
from PIL import Image
import glob

images = glob.glob('./image_folder_in/*')
for image in images:
    img = Image.open(image)  # 画像の読み込み
    img_width, img_height = img.size  # 画像のサイズを取得

    if img_height < img_width:
        # 絵が横向きの場合、縮小率を計算（w800として）
        scale = img_width / 800
        size = (800, math.ceil(img_height / scale))
    else:
        # 絵が縦向きの場合
        scale = img_height / 800
        size = (math.ceil(img_width / scale), 800)
        
    # resize・・求められたsizeに縮小
    img = img.resize(size)
    print(img_width, img_height, img.size) #デバッグ（削除可能）

    # 名前を変えて保存
    tmp = image.split('\\')[-1].split(".")
    img.save('./image_folder_out/' + tmp[0] + "_縮小." + tmp[1])
