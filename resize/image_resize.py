import math
from PIL import Image
import glob

images = glob.glob('./image_folder_in/*')
for image in images:
    img = Image.open(image)  # 画像の読み込み
    img_width, img_height = img.size  # 画像のサイズを取得

    if img_height < img_width:
        # 絵が横向きの場合、縮小率を計算（w500, h300 の画像を例とします）
        scale = img_width / 533  # e.g. 500 / 512 = 0.98
        size = (533, math.ceil(img_height / scale))  # e.g. (512, 300 / 0.98) → (512, 307)
    else:
        # 絵が縦向きの場合（w300, h500 の画像を例とします）
        scale = img_height / 533
        size = (math.ceil(img_width / scale), 533)  # e.g. (300 / 0.98, 512) → (307, 512)
        
    # resize
    img = img.resize(size)
    print(img_width, img_height, img.size)

    # 名前を変えて保存
    tmp = image.split('\\')[-1].split(".")
    img.save('./image_folder_out/' + tmp[0] + "_resize." + tmp[1])