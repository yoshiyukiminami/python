# python リポジトリ
```console
pip install -r requirements.txt
```
```console
pip freeze > requirements.txt
```

## data processing
## diagnosis
- ex_programは旧プログラム
### 1.特性深度
- source: `diagnosis/soil_physical_diagnosis.ver2.0.py`  
- `土壌物理性診断_{id}_{圃場名}_{品目}_{計測日}_{時期}.jpeg`  
- `output/土壌物理性診断_Agsoil_圃場-A_レタス_2022.03.25_定植時.jpeg` に保存する
### 2.化学性
- source: `diagnosis/soil_diagnosis_report.ver2.2.py`  
- `土壌化学性診断_{ID}_{圃場名}_{品目}_{作型}_{採土日}.jpeg`  
- `output/土壌化学性診断_B生産者_１番圃場_キャベツ_露地_2022.06.03.jpeg` に保存する
### 3.写真加工
- source: `diagnosis/hojyo_picture_convert.ver1.1.py`
### 4.基本情報（パワポ出力）
- source: `diagnosis/soil_diagnosis_basic_information.ver2.1.py`  
- `output/create_powerpnt.pptx` に保存する

## dojyokoudo
## graph
## invalid data
## okada
サンプルコード提供などに使っています
## pandas histgram
## resize
圃場で撮った写真をまとめてリサイズします
- ファイルを直接実行する前提になっています
- カレントディレクトリに `image_folder_in` `image_folder_out` のフォルダがある前提になっています（ないとなにもせずに処理完了）
`image_folder_in` のフォルダにある写真を変換して `image_folder_out` のフォルダに出力します
## tokuseishindo
