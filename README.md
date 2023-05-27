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
python manage.py loaddata .\crm\fixtures\category.json
python manage.py loaddata .\crm\fixtures\company.json
python manage.py loaddata .\crm\fixtures\authuser.json
python manage.py loaddata .\crm\fixtures\crop.json
python manage.py loaddata .\crm\fixtures\area.json
python manage.py loaddata .\crm\fixtures\period.json
python manage.py loaddata .\crm\fixtures\cultivationtype.json
python manage.py loaddata .\crm\fixtures\land.json
python manage.py loaddata .\crm\fixtures\landreview.json
python manage.py loaddata .\crm\fixtures\samplingmethod.json
python manage.py loaddata .\crm\fixtures\ledger.json
python manage.py loaddata .\crm\fixtures\landscorechemical.json
```

- webアプリを動かす
```console
soil_analysis> python manage.py runserver
```

## tokuseishindo
