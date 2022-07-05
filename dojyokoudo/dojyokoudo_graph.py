import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import glob
import csv

# 【全体設定】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)


def koudobunpu_dataset():
    # 【Step-1】硬度分布データのデータフレーム決定・・point1=圃場内側定位置1、point2=圃場内測定位置2
    All_list = {
        'nojyomei': [], 'hojyomei': [], 'item': [], 'ymd': [], 'jiki': [], 'point1': [], 'point2': [],
        '1cm': [], '2cm': [], '3cm': [], '4cm': [], '5cm': [], '6cm': [], '7cm': [], '8cm': [], '9cm': [],
        '10cm': [], '11cm': [], '12cm': [], '13cm': [], '14cm': [], '15cm': [], '16cm': [], '17cm': [],
        '18cm': [], '19cm': [], '20cm': [], '21cm': [], '22cm': [], '23cm': [], '24cm': [], '25cm': [],
        '26cm': [], '27cm': [], '28cm': [], '29cm': [], '30cm': [], '31cm': [], '32cm': [], '33cm': [],
        '34cm': [], '35cm': [], '36cm': [], '37cm': [], '38cm': [], '39cm': [], '40cm': [], '41cm': [],
        '42cm': [], '43cm': [], '44cm': [], '45cm': [], '46cm': [], '47cm': [], '48cm': [], '49cm': [],
        '50cm': [], '51cm': [], '52cm': [], '53cm': [], '54cm': [], '55cm': [], '56cm': [], '57cm': [],
        '58cm': [], '59cm': [], '60cm': []
    }

    # 【Step-2】dfから不必要な列を削除する
    df_dp = df2.drop(df2.columns[range(72, 110)], axis=1)
    df_dp = df_dp.drop(df_dp.columns[range(8, 12)], axis=1)
    df_dp = df_dp.drop(df_dp.columns[range(0, 1)], axis=1)
    df_dp.reset_index(inplace=True, drop=True)
    nojyomei = df_dp.iat[0, 0]
    hojyomei = df_dp.iat[0, 2]

    # 【Step-3】品目・時期・測定日でエラー（2つ以上ある場合）を検知しAll_listに格納する
    item_list = df_dp['品目'].tolist()
    item_list_count = len(set(item_list))
    isvalid = True
    if not item_list_count == 1:
        print("エラー：品目が2つ以上あります。")
        isvalid = False
    else:
        item = item_list[0]
        jiki_list = df_dp['時期'].tolist()
        jiki_list_count = len(set(jiki_list))
        if not jiki_list_count == 1:
            print("エラー：時期が2つ以上あります。")
            isvalid = False
        else:
            jiki = jiki_list[0]
            sokuteibi = df_dp['測定日'].tolist()
            sokuteibi_count = len(set(sokuteibi))
            if not sokuteibi_count == 1:
                print("エラー：測定日が2つ以上あります。")
                isvalid = False
            else:
                # 測定日をdatetimeに変換する
                sokuteibi2 = sokuteibi[0] + ' ' + '00:00:00'
                sokuteibi2 = datetime.datetime.strptime(sokuteibi2, '%Y.%m.%d %H:%M:%S')

                # 【Step-4】df_dpに格納したデータ（文字列含む）の平均値を算出しAll_listに格納する
                df_ave = df_dp.groupby(['圃場内位置', '圃場内位置2']).mean()
                new_header = ['1cm', '2cm', '3cm', '4cm', '5cm', '6cm', '7cm', '8cm', '9cm', '10cm',
                              '11cm', '12cm', '13cm', '14cm', '15cm', '16cm', '17cm', '18cm', '19cm',
                              '20cm', '21cm', '22cm', '23cm', '24cm', '25cm', '26cm', '27cm', '28cm',
                              '29cm', '30cm', '31cm', '32cm', '33cm', '34cm', '35cm', '36cm', '37cm',
                              '38cm', '39cm', '40cm', '41cm', '42cm', '43cm', '44cm', '45cm', '46cm',
                              '47cm', '48cm', '49cm', '50cm', '51cm', '52cm', '53cm', '54cm', '55cm',
                              '56cm', '57cm', '58cm', '59cm', '60cm'
                              ]
                df_ave.columns = new_header
                df_ave_index = df_ave.index
                point1_list = df_ave_index.get_level_values(0)
                point2_list = df_ave_index.get_level_values(1)
                tuika_list = [nojyomei, hojyomei, item, sokuteibi2, jiki]
                tuika_header = ['nojyomei', 'hojyomei', 'item', 'ymd', 'jiki']
                df_ave.insert(loc=0, column='point2', value=point2_list)
                df_ave.insert(loc=0, column='point1', value=point1_list)
                for i, (tuika, tuikah) in enumerate(zip(tuika_list, tuika_header)):
                    df_ave.insert(loc=i, column=tuikah, value=tuika)
                df_ave.reset_index(inplace=True, drop=True)
                # print(df_ave)
                # 【課題】dataframeからdict型のAll_listに追記する
                # com_header = df_ave.columns
                # df_ave_count = len(df_ave)
                # print(com_header, df_ave_count)
                # for j in range(df_ave_count):
                #     All_list[com_header].append(df_ave[com_header][j])
                # print(All_list)
                savetime = datetime.datetime.now()
                yyyymmdd = savetime.strftime('%Y-%m-%d_%H-%M-%S')
                save_name = str(nojyomei) + '_' + str(hojyomei) + '_' + yyyymmdd
                # 特性深度分布の計算結果と紐付け情報を格納したDATAFRAME（df_all）をcsv保存・・暫定的に
                # df_ave.to_csv(save_name + '.csv', encoding='SHIFT-JIS', index=False)

                # データセットされたdf_aveから土壌硬度分布グラフ（折れ線）を生成する
                # 事前準備1：測定位置ごとの色・線のプロパティを決める
                line_color = {'A': '#1616A7', 'B': '#1CA71C', 'C': '#FB0D0D'}
                line_shape = {'1': 'solid', '2': 'dot', '3': 'dash'}

                # 硬度分布グラフ（折れ線）の生成と保存（JPEG、HTML）
                x = df_ave.columns.to_list()
                del x[0: 7]
                fig = go.Figure()
                for j in range(len(df_ave)):
                    m = j + 1
                    y = list(df_ave.iloc[j])
                    point1 = y[5]
                    point2 = str(y[6])
                    name = point1 + '-' + str(point2)
                    del y[0: 7]
                    color = line_color[point1]
                    dash = line_shape[point2]
                    fig.add_trace(go.Scatter(y=x,
                                             x=y,
                                             name=name,
                                             mode='lines',
                                             line=dict(color=color, dash=dash),
                                             hovertemplate='硬さ:%{x:2f}kpa, 深度:%{y}cm',
                                             orientation='h')
                                  )
                    fig.update_layout(title=dict(text='土壌硬度分布_' + nojyomei + '_' + hojyomei,
                                                 font=dict(size=20, color='black'),
                                                 xref='paper',
                                                 x=0.01,
                                                 y=0.92,
                                                 xanchor='left'
                                                 ),
                                      yaxis=dict(title='深度（㎝）', range=(60, 1)),
                                      xaxis=dict(title='硬さ（kpa）', range=(200, 3000)),
                                      legend=dict(orientation='h',
                                                  xanchor='left',
                                                  x=0.3,
                                                  yanchor='bottom',
                                                  y=0.97),
                                      width=600,
                                      height=800,
                                      plot_bgcolor='white'
                                      )
                    fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
                    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
                # fig.write_image(save_name + '.jpeg')
                # fig.write_image('土壌硬度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
                # fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
                fig.show()
                # time.sleep(1)


if __name__ == '__main__':
    # ☆所定データの読み込み・・【展開】特定フォルダから複数ファイルを同時に読み込む処理
    filedir = 'C:/Users/minam/Desktop/tokusei_precal/'
    files = glob.glob(filedir + '/**/*.csv')
    print(files)

    # 読み込んだファイルを「農場名」「圃場名」「圃場内測定位置」「圃場内測定位置2」で分類し、df2に格納
    for file in files:
        print(file)
        df = pd.read_csv(file, encoding='Shift-JIS', header=0)

        # Step-1：農場名での分類
        nojyomei_list = df['農場名'].tolist()
        nojyomei_list = list(set(nojyomei_list))
        # print(nojyomei_list)

        # ここから未処理
        # Step-2：圃場名でのデータ抽出と所定DATAFRAMEへの格納
        for nojyomei in nojyomei_list:
            df1 = df[df['農場名'] == nojyomei]
            hojyomei_list = df1['圃場名'].tolist()
            hojyomei_list = list(set(hojyomei_list))
            for hojyomei in hojyomei_list:
                df2 = df1[df1['圃場名'] == hojyomei]
                point1_list = df2['圃場内位置'].tolist()
                point2_list = df2['圃場内位置2'].tolist()
                point1_list = list(set(point1_list))
                point2_list = list(set(point2_list))

                # 測定位置情報のエラー検知
                isvalid = True
                if not len(point1_list) == len(point2_list):
                    print("測定位置情報が一致しません")
                    isvalid = False
                else:
                    koudobunpu_dataset()
                    # #圃場内測定位置・圃場内測定位置2の組み合わせ毎にdf4のデータフレームに格納
                    # for k in point1_list:
                    #     df3 = df2[df2['圃場内位置'] == k]
                    #     # print(k)
                    #     for m in point2_list:
                    #         df4 = df3[df3['圃場内位置2'] == m]
