# データの前処理
# 【Step_0】ヘッダーの不一致検知・・エラー00
# 【Step_1】農場名・圃場名の空欄（データなし）検知・・エラー01、02
# 【Step_2-1】紐付け情報エラーA・・圃場内位置、圃場内位置2の記入漏れまたは入力条件エラー（A～E以外、1~5以外、文字属性）・・エラー03~06
# 【Step_2-2】紐付け情報エラーB・・品目、測定日、時期の記入漏れまたは入力条件エラー（1項目に複数入力、文字属性）・・エラー07～10
# 【Step_3】パラメータ計算値エラー・・空欄（NAN）またはエラー値（負数）の検出・・エラー11
# 【Step_4】測定ミス検知・・土壌硬度データ数値から測定ミスを判定　※1～60㎝のMAX-MINが差が232kpa以内はエラー・・エラー12
# 【Step_5】並び替え・・農場名、圃場名が同じ組み合わせで昇順
# （方針変更-20220611）このプログラムではあくまでも空欄やエラー値（負数、測定ミス）の検出を目的とし、修正・追記は手作業で実施する。削除や修正を自動化しない。
# 【action_1】Step_0～2-2は差戻し（修正ループ）、3～4はエラーデータ行を削除
# 【action_2】Step_4まで通過したデータはtable1（元データDB→パラメータ・マトリックスグラフ、土壌硬度・線グラフで使用）に格納
# 【action_3】Step_4まで通過したデータから均一性評価サービスに必要な数値を計算し、table2（均一性評価サービスDB）に格納
# 【action_4】Step_4まで通過したデータから作土層管理サービス（仮）に必要な数値を計算し、table3（作土層管理サービス）に格納

import pandas as pd
import datetime
import glob

# 【下準備1】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)

# 【下準備2】基本ヘッダーの読み込み
basic_header = pd.read_csv('C:/Users/minam/Desktop/mypandas/basic_header_format.csv',
                           encoding='Shift-JIS', header=0)

# ☆所定データの読み込み・・【展開】特定フォルダから複数ファイルを同時に読み込む処理
filedir = 'C:/Users/minam/Desktop/dataprecheck/'
files = glob.glob(filedir + '/**/*.csv')
print(files)

# フォルダに格納されているファイルを順番にdfに読み込んでエラーチェック処理
for file in files:
    print(file)
    df = pd.read_csv(file, encoding='Shift-JIS', header=0)
    # print(df)

    # 【Step_0】ヘッダーの不一致を検出、「農場名」「圃場名」「圃場内位置」「圃場内位置2」の順に並べ替え
    df_header = df[:0]
    if not list(df_header.columns.values) == list(basic_header.columns.values):
        print("エラー00：ヘッダーが違うので、標準のヘッダーを使用ください")
    else:
        print("ヘッダーは標準ヘッダーと一致")

    # 【Step_1】農場名および圃場名の空欄（データなし）検知＆空欄行表示・・エラー01、02
    df_nojyomei = df['農場名']
    df_hojyomei = df['圃場名']
    df_nojyomei_list = list(set(df_nojyomei))
    df_hojyomei_list = list(set(df_hojyomei))
    print(df_nojyomei_list, df_hojyomei_list)

    isvalid = True
    if not df_nojyomei.notnull().all():
        print("エラー01：農場名に空欄があります")
        print("空欄のある行は以下の通り・・")
        print(df.query('農場名 != 農場名'))
        isvalid = False
    else:
        print("農場名に空欄はありません")
        if not df_hojyomei.notnull().all():
            print("エラー02：圃場名に空欄があります")
            print("空欄のある行は以下の通り・・")
            print(df.query('圃場名 != 圃場名'))
            isvalid = False
        else:
            print("圃場名に空欄はありません")

    # 【Step_2-1】紐付け情報エラーA・・圃場内位置、圃場内位置2の記入漏れまたは入力条件エラー（A～E以外、1~5以外、文字属性）・・エラー03～06
    df_point1 = df['圃場内位置']
    df_point2 = df['圃場内位置2']
    # print(df_point1, df_point2, type(df_point1))

    #  測定位置の範囲をリスト化
    point1_list = ['A', 'B', 'C', 'D', 'E']
    point2_list = [1, 2, 3, 4, 5]

    if isvalid:
        #  圃場内位置および圃場内位置2の空欄（データなし）を検知＆空欄行表示・・エラー03、04
        if not df_point1.notnull().all():
            print("エラー03：圃場内位置に空欄があります")
            print("空欄のある行は以下の通り・・")
            print(df.query('圃場内位置 != 圃場内位置'))
            isvalid = False
        else:
            print("圃場内位置に空欄はありません")
            if not df_point2.notnull().all():
                print("エラー04：圃場内位置2に空欄があります")
                print("空欄のある行は以下の通り・・")
                print(df.query('圃場内位置2 != 圃場内位置2'))
                isvalid = False
            else:
                print("圃場内位置2に空欄はありません")

        if isvalid:
            # 圃場内位置の入力条件エラー：リスト（A～E）以外の文字・数値で入力検知＆エラー行表示
            for i in df_point1:
                if i not in point1_list:
                    print("エラー05：圃場内位置に無効な文字が入力されています")
                    print("無効な文字・数字が入力されている行は以下の通りです")
                    print(df.query("not 圃場内位置 in ['A', 'B', 'C', 'D', 'E']"))
                    isvalid = False
            if isvalid:
                print("圃場内位置に無効な文字・数字はありません")

            if isvalid:
                # 圃場内位置2の入力条件エラー検知：リスト（1～5）以外の数値や文字で入力＆エラー行表示
                for j in df_point2:
                    if j not in point2_list:
                        print("エラー06：圃場内位置2に無効な数値が入力されています")
                        print("無効な文字・数字が入力されている行は以下の通りです")
                        print(df.query("not 圃場内位置2 in [1, 2, 3, 4, 5]"))
                        isvalid = False
                if isvalid:
                    print("圃場内位置2に無効な文字・数字はありません")

    # 【Step_2-2】紐付け情報エラーB・・品目、測定日、時期の記入漏れまたは入力条件エラー（1項目に複数入力、文字属性）・・エラー07～10

    # 【下処理1】農場名での分類
    nojyomei_list = df['農場名'].tolist()
    nojyomei_list = list(set(nojyomei_list))
    nojyomei_list_count = len(nojyomei_list)

    # Step-2-2：紐付け情報エラーB・・品目・測定日・時期の記入漏れまたは入力条件エラー検知（測定日：データ型、時期：登録外）
    if isvalid:
        for k in range(nojyomei_list_count):
            nojyomei = df['農場名'][k]
            df1 = df[df['農場名'] == nojyomei]
            hojyomei_list = df1['圃場名'].tolist()
            hojyomei_list = list(set(hojyomei_list))
            hojyomei_list_count = len(hojyomei_list)
            for m in range(len(hojyomei_list)):
                hojyomei = hojyomei_list[m]
                df2 = df1[df1['圃場名'] == hojyomei]
                print(hojyomei)

                # 品目・時期の入力条件エラー検知（空欄、複数）+エラーのある圃場名を表示
                item_list = df2['品目'].tolist()
                item_list_count = len(set(item_list))
                if not item_list_count == 1:
                    print("エラー07：品目で空欄または異なった文字列があります")
                    print('圃場名：' + hojyomei)
                    isvalid = False
                if isvalid:
                    print("品目が空欄や異なった文字列はありません")
                    jiki_list = df2['時期'].tolist()
                    jiki_list_count = len(set(jiki_list))
                    if not jiki_list_count == 1:
                        print("エラー08：時期で空欄または異なった文字列があります")
                        print('圃場名：' + hojyomei)
                        isvalid = False
                    if isvalid:
                        print(hojyomei + "時期で空欄や異なった文字列はありません")
                        # 測定日の入力条件エラー検知（空欄、複数、表示形式）+エラーのある圃場名を表示
                        sokuteibi_list = df2['測定日'].tolist()
                        sokuteibi_list = list(set(sokuteibi_list))
                        sokuteibi_list_count = len(sokuteibi_list)
                        # print(sokuteibi_list, sokuteibi_list_count)
                        if not sokuteibi_list_count == 1:
                            print("エラー09：測定日で空欄または異なった文字列があります")
                            print('圃場名：' + hojyomei)
                            isvalid = False
                        if isvalid:
                            try:
                                sokuteibi = sokuteibi_list[0] + ' ' + '00:00:00'
                                sokuteibi = datetime.datetime.strptime(sokuteibi,
                                                                       '%Y.%m.%d %H:%M:%S')
                                # print(sokuteibi)
                            except ValueError:
                                print("エラー10：測定日が空欄または表示形式が間違っています")
                                print('圃場名：' + hojyomei)
                                isvalid = False
                            if isvalid:
                                print("測定日で空欄や間違った表示形式はありません")

    # 【Step_3】パラメータ計算値エラー・・NANまたはエラー値の検出（負）・・エラー11
    # 　エラー値を検出した行情報を配列に保持・・削除する際に削除業を特定

    if isvalid:
        error_count = 0
        df_pm = df.loc[:, 'x0':'Slope\n(Mpa/cm)']
        for n, row in df_pm.iterrows():
            # チェック1：空欄の検出
            if row.isnull().values.sum() != 0:
                print(f'エラー11：{n + 1}行目にパラメータ計算値の空欄があります')
                error_count += 1

        df_pm_nc = df.loc[:, 'ηC']
        for n, row in enumerate(df_pm_nc):
            # チェック2：負の値（ncのみ）
            if row < 0:
                print(f'エラー11：{n + 1}行目に負の値があります')
                error_count += 1

        if error_count == 0:
            print("パラメータ計算値の空欄および負の値はありませんでした")

    # ##ここから未処理##
    # 【Step_4】測定ミス検知・・土壌硬度データ数値から測定ミスを判定　※1～60㎝のMAX-MINが差が232kpa以内はエラー・・エラー12
    # 現状、岡田さん作成のプログラムと併用してバッジ処理するやり方で進める。
    # # ##ここまで未処理##

    # 【Step_5】並び替え・・農場名、圃場名が同じ組み合わせで昇順
    df = df.sort_values(by=['農場名', '圃場名', '圃場内位置', '圃場内位置2'], ascending=True)
    # 各ファイル毎に 元のファイル名に”_precheck.csv”を追加してCSVで保存
    file_name = file.rsplit('\\', 1)[1]
    file_name = file_name.rsplit('.')[0]
    # print(file_name)
    df.to_csv(file_name + '_precheck.csv', encoding='Shift-JIS', index=None)
