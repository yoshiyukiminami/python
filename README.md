# python リポジトリ
```console
pip install -r requirements.txt
```
```console
pip freeze > requirements.txt
```

## data processing
## diagnosis
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

## soil analysis
- `.env` をもらってください
- ローカルmysqlに `soil_db` というデータベースを作成してから以下コマンドを実行
```console
python manage.py makemigrations crm
python manage.py migrate
python manage.py loaddata .\crm\fixtures\test_data1.json
```

## tokuseishindo
