# データの前処理
# 0.フォーマットの不一致・・headerの文字列及び列数の不一致・・Done
# 1.並び替え・・農場名、圃場名が同じ組み合わせで昇順または降順　※農場名、圃場名の文字属性チェックは必要か？
# 2-1.紐付け情報エラーA・・圃場内位置、圃場内位置2の記入漏れまたは入力条件エラー（A～E以外、1~5以外、文字属性）
# 2-2.紐付け情報エラーB・・品目、測定日、時期の記入漏れまたは入力条件エラー（1項目に複数入力、文字属性）
# 3.パラメータ計算値エラー・・NANまたはエラー値の検出（負）
# 4.測定ミス検知・・土壌硬度データ数値から測定ミスを判定　※1～60㎝のMAX-MINが差が232kpa以内はエラー
# action1:0～2-2は差戻し（修正ループ）、3～4はエラーデータ行を削除
# action2:4まで通過したデータはtable1（元データDB→パラメータ・マトリックスグラフ、土壌硬度・線グラフで使用）に格納
# action3:4まで通過したデータから均一性評価サービスに必要な数値を計算し、table2（均一性評価サービスDB）に格納
# action4:4まで通過したデータから作土層管理サービス（仮）に必要な数値を計算し、table3（作土層管理サービス）に格納

import pandas as pd
import datetime

# 【下準備】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)

# 基本ヘッダーの読み込み
basic_header = pd.read_csv('C:/Users/minam/Desktop/mypandas/basic_header_format.csv',
                           encoding='Shift-JIS', header=0)

# 所定データの読み込み・・【展開】特定フォルダから複数ファイルを同時に読み込む処理
df = pd.read_csv('C:/Users/minam/Desktop/mypandas/data_sample_hp-1-base.csv', encoding='Shift-JIS',
                 header=0)

# Step-0＆1：ヘッダーの不一致を検出、「農場名」「圃場名」「圃場内位置」「圃場内位置2」の順に並べ替え
df_header = df[:0]
# print(df_header, basic_header)

if not list(df_header.columns.values) == list(basic_header.columns.values):
    print("エラー00：ヘッダーが違うので、標準のヘッダーを使用ください。")
else:
    df = df.sort_values(by=['農場名', '圃場名', '圃場内位置', '圃場内位置2'], ascending=True)
    # df.to_csv('df.csv', encoding='Shift-JIS', index=None)
    # print(df, type(df))

    # Step2-1：紐付け情報エラーA・・圃場内位置、圃場内位置2の記入漏れまたは入力条件エラー（A～E、1～5以外、文字属性）
    df_point1 = df['圃場内位置']
    df_point2 = df['圃場内位置2']

    point1_list = ['A', 'B', 'C', 'D', 'E']
    point2_list = [1, 2, 3, 4, 5]

    # 圃場内位置の入力条件エラー検知：未入力（NAN）または、A～E以外のアルファベットや文字・数値で入力
    for i in df_point1:
        if i not in point1_list:
            print("エラー01：圃場内位置が未入力または無効な文字が入力されています")
            break
        else:
            continue

    # 圃場内位置2の入力条件エラー検知：未入力（NAN）または、1～5以外の数値や文字で入力
    for j in df_point2:
        if j not in point2_list:
            print("エラー02：圃場内位置2が未入力または無効な数値が入力されています")
            break
        else:
            continue

    # Step-2-2：【下処理1】農場名での分類
    nojyomei_list = df['農場名'].tolist()
    nojyomei_list = list(set(nojyomei_list))
    nojyomei_list_count = len(nojyomei_list)

    # 農場名が空欄または複数ある場合にエラー表示
    if nojyomei_list_count > 1:
        print('エラー03：農場名が空欄または複数あります')
    else:
        # print(nojyomei_list)
        # Step-2-2：紐付け情報エラーB・・品目・測定日・時期の記入漏れまたは入力条件エラー検知（測定日：データ型、時期：登録外）
        for k in range(nojyomei_list_count):
            nojyomei = df['農場名'][k]
            df1 = df[df['農場名'] == nojyomei]
            hojyomei_list = df1['圃場名'].tolist()
            hojyomei_list = list(set(hojyomei_list))
            hojyomei_list_count = len(hojyomei_list)
            for m in range(len(hojyomei_list)):
                hojyomei = hojyomei_list[m]
                df2 = df1[df1['圃場名'] == hojyomei]

                # 品目・時期の入力条件エラー検知（空欄、複数）+エラーのある圃場名を表示
                item_list = df2['品目'].tolist()
                item_list_count = len(set(item_list))
                if not item_list_count == 1:
                    print("エラー04：品目が空欄または複数あります")
                    print('圃場名：' + hojyomei)
                    break
                else:
                    jiki_list = df2['時期'].tolist()
                    jiki_list_count = len(set(jiki_list))
                    if not jiki_list_count == 1:
                        print("エラー05：時期が空欄または複数あります")
                        print('圃場名：' + hojyomei)
                        break
                    else:
                        # 測定日の入力条件エラー検知（空欄、複数、表示形式）+エラーのある圃場名を表示
                        sokuteibi_list = df2['測定日'].tolist()
                        sokuteibi_list = list(set(sokuteibi_list))
                        sokuteibi_list_count = len(sokuteibi_list)
                        print(sokuteibi_list, sokuteibi_list_count)
                        if not sokuteibi_list_count == 1:
                            print("エラー06：測定日が空欄または複数あります")
                            print('圃場名：' + hojyomei)
                            break
                        else:
                            try:
                                sokuteibi = sokuteibi_list[m] + ' ' + '00:00:00'
                                sokuteibi = datetime.datetime.strptime(sokuteibi,
                                                                       '%Y.%m.%d %H:%M:%S')
                                print(sokuteibi)
                            except ValueError:
                                print("エラー07：測定日の表示形式が間違っています")
                                print('圃場名：' + hojyomei)
                                break
