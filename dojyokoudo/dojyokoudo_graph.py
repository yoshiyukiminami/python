import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import glob

# 【全体設定】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)


def koudobunpu_dataset(df_point):
    # 【Step-1】硬度分布データのデータフレーム決定・・point1=圃場内側定位置1、point2=圃場内測定位置2
    All_list = {
        'nojyomei': [], 'item': [], 'hojyomei': [], 'ymd': [], 'jiki': [], 'point1': [], 'point2': [],
        '1cm': [], '2cm': [], '3cm': [], '4cm': [], '5cm': [], '6cm': [], '7cm': [], '8cm': [], '9cm': [],
        '10cm': [], '11cm': [], '12cm': [], '13cm': [], '14cm': [], '15cm': [], '16cm': [], '17cm': [],
        '18cm': [], '19cm': [], '20cm': [], '21cm': [], '22cm': [], '23cm': [], '24cm': [], '25cm': [],
        '26cm': [], '27cm': [], '28cm': [], '29cm': [], '30cm': [], '31cm': [], '32cm': [], '33cm': [],
        '34cm': [], '35cm': [], '36cm': [], '37cm': [], '38cm': [], '39cm': [], '40cm': [], '41cm': [],
        '42cm': [], '43cm': [], '44cm': [], '45cm': [], '46cm': [], '47cm': [], '48cm': [], '49cm': [],
        '50cm': [], '51cm': [], '52cm': [], '53cm': [], '54cm': [], '55cm': [], '56cm': [], '57cm': [],
        '58cm': [], '59cm': [], '60cm': []
    }

    # 【Step-2】品目・時期をAll_listに格納し、エラー（2つ以上ある場合）を検知する
    item_list = df_point['品目'].tolist()
    item_list_count = len(set(item_list))
    isvalid = True
    if not item_list_count == 1:
        print("エラー：品目が2つ以上あります。")
        isvalid = False
        # break
    else:
        All_list['item'].append(list(set(item_list))[0])
    jiki_list = df_point['時期'].tolist()
    jiki_list_count = len(set(jiki_list))
    if not jiki_list_count == 1:
        print("エラー：時期が2つ以上あります。")
        isvalid = False
        # break
    else:
        All_list['jiki'].append(list(set(jiki_list))[0])
    # 測定日をdatetimeに変換してAll_listに格納し、エラー（2つ以上ある場合）を検知する
    sokuteibi = df_point['測定日'].tolist()
    sokuteibi_count = len(set(sokuteibi))
    if not sokuteibi_count == 1:
        print("エラー：測定日が2つ以上あります。")
        isvalid = False
        # break
    else:
        sokuteibi2 = sokuteibi[0] + ' ' + '00:00:00'
        sokuteibi2 = datetime.datetime.strptime(sokuteibi2, '%Y.%m.%d %H:%M:%S')
        All_list['ymd'].append(sokuteibi2)

        # 【Step-3】農場名・圃場名・圃場内側定位置・圃場内側定位置2をAll_listに格納
    All_list['nojyomei'].append(set(df_point['農場名'][0]))
    All_list['hojyomei'].append(set(df_point['圃場名'][0]))
    All_list['point1'].append(set(df_point['圃場内位置'][0]))
    All_list['point2'].append(set(df_point['圃場内位置2'][0]))

    # ここから未処理
    # 【Step-4】土壌硬度データの測定地点（1㎝～60㎝）ごとの平均値×1/1000した数値を格納
    df_point_mean = df_point.mean(axis=0, skipna=True)
    print(df_point_mean)


def koudobunpu_graphset(df_point):
    # ここから未処理
    # tokuseishindo_datasetで格納された土壌硬度データから分布グラフを生成
    for m, (d1, d2) in enumerate(zip(df_all['freq'], df_all['rel_freq'])):
        # 圃場別特性深度分布グラフ（度数）を生成・保存（JPEG、HTML）
        fig = go.Figure()
        hojyomei = df_all['hojyomei'][m]
        nojyomei = df_all['nojyomei'][m]
        sokuteibi = df_all['ymd'][m].strftime('%Y.%m.%d')
        fig.add_trace(go.Bar(y=df_all['class_value'][0],
                             x=d1,
                             name=hojyomei,
                             width=3,
                             hovertemplate='度数:%{x}, 深度:%{y}cm', showlegend=True,
                             orientation='h')
                      )
        fig.update_layout(title=dict(text='特性深度分布（度数）_' + nojyomei + '_' + sokuteibi,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.01,
                                     y=0.9,
                                     xanchor='left'
                                     ),
                          yaxis=dict(title='深度（㎝）', range=(60, 0)),
                          xaxis=dict(title='度数', range=(0, 50)),
                          legend=dict(orientation='h',
                                      xanchor='left',
                                      x=0.6,
                                      yanchor='bottom',
                                      y=0.9,
                                      bgcolor='white',
                                      bordercolor='grey'
                                      ),
                          width=600,
                          height=400,
                          plot_bgcolor='white'
                          )
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
        filedir = 'C:/Users/minam/Desktop/tokusei_histgram_picture/'
        fig_name = 'histgram-1_' + nojyomei + '_' + hojyomei + '_' + sokuteibi + '.jpeg'
        fig_name1 = filedir + fig_name
        print(fig_name1)
        # fig.write_image(fig_name1)
        # fig.write_image('特性深度分布（度数）_' + nojyomei + '_' + hojyomei + '_' + sokuteibi + '.jpeg')
        # fig.write_html(fig_name1)
        fig.show()
        # ここまで未処理


if __name__ == '__main__':
    # ☆所定データの読み込み・・【展開】特定フォルダから複数ファイルを同時に読み込む処理
    filedir = 'C:/Users/minam/Desktop/tokusei_precal/'
    files = glob.glob(filedir + '/**/*.csv')
    print(files)

    # 読み込んだファイルを「農場名」「圃場名」「圃場内測定位置」「圃場内測定位置2」で分類し、df_pointに格納
    for file in files:
        print(file)
        df = pd.read_csv(file, encoding='Shift-JIS', header=0)
        # print(df)

        # Step-1：農場名での分類
        nojyomei_list = df['農場名'].tolist()
        nojyomei_list = list(set(nojyomei_list))
        nojyomei_list_count = len(nojyomei_list)
        print(nojyomei_list, nojyomei_list_count)

        # ここから未処理
        # Step-2：圃場名でのデータ抽出と所定DATAFRAMEへの格納
        for i in range(len(nojyomei_list)):
            nojyomei = nojyomei_list[i]
            df1 = df[df['農場名'] == nojyomei]
            hojyomei_list = df1['圃場名'].tolist()
            hojyomei_list = list(set(hojyomei_list))
            hojyomei_list_count = len(hojyomei_list)
            print(i, nojyomei, hojyomei_list, hojyomei_list_count)

            for j in range(len(hojyomei_list)):
                hojyomei = hojyomei_list[j]
                df2 = df1[df1['圃場名'] == hojyomei]
                print(j, hojyomei)
                point1_list = df2['圃場内位置'].tolist()
                point2_list = df2['圃場内位置2'].tolist()
                point1_list = list(set(point1_list))
                point2_list = list(set(point2_list))
                print(point1_list, point2_list)

                # 測定位置情報のエラー検知
                isvalid = True
                if not len(point1_list) == len(point2_list):
                    print("測定位置情報が一致しません")
                    isvalid = False
                    # break
                else:
                    # 圃場内測定位置・圃場内測定位置2の組み合わせ毎にdf_pointのデータフレームに格納
                    for k in point1_list:
                        df_point = df2[df2['圃場内位置'] == k]
                        # print(df_point, k)
                        for m in point2_list:
                            df_point = df_point[df_point['圃場内位置2'] == m]
                            # print(df_point, m)
                            koudobunpu_dataset(df_point)

                        #                 #ヒストグラムの計算値をAll_listに格納
#                 bins = np.linspace(0, 60, 13)
#                 freq = dataset1.value_counts(bins=bins, sort=False)
#                 All_list['freq'].append(freq)
#                 class_value = (bins[:-1] + bins[1:]) / 2  # 階級値
#                 All_list['class_value'].append(class_value)
#                 rel_freq = freq / dataset1.count()  # 相対度数
#                 All_list['rel_freq'].append(rel_freq)
#                 cum_freq = freq.cumsum()  # 累積度数
#                 All_list['cum_freq'].append(cum_freq)
#                 rel_cum_freq = rel_freq.cumsum()  # 相対累積度数
#                 All_list['rel_cum_freq'].append(rel_cum_freq)
#                 class_index = freq.index  # 階層
#                 All_list['class_index'].append(class_index)

#                 # 統計量の計算値をAll_Listに格納
#                 # describeメソッドで個数～最大値を一括で計算
#                 stats = dataset1.describe()
#                 # print(stats)
#                 stats_count = pd.Series(data=stats)['count']
#                 All_list['count'].append(stats_count) # 個数
#                 stats_mean = pd.Series(data=stats)['mean']
#                 All_list['mean'].append(stats_mean) # 平均値
#                 stats_std = pd.Series(data=stats)['std']
#                 All_list['std'].append(stats_std) # 標準偏差（標本分数）
#                 stats_min = pd.Series(data=stats)['min']
#                 All_list['min'].append(stats_min) # 最小値
#                 stats_25 = pd.Series(data=stats)['25%']
#                 All_list['25%'].append(stats_25) # 四分位数（25%）
#                 stats_50 = pd.Series(data=stats)['50%']
#                 All_list['50%'].append(stats_50) # 四分位数（50%）
#                 stats_75 = pd.Series(data=stats)['75%']
#                 All_list['75%'].append(stats_75) # 四分位数（75%）
#                 stats_max = pd.Series(data=stats)['max']
#                 All_list['max'].append(stats_max) # 最大値
#                 All_list['skew'].append(dataset1.skew()) # 歪度
#                 All_list['kurt'].append(dataset1.kurt()) # 尖度
#                 All_list['var_ddof=1'].append(dataset1.var(ddof=1)) # 分散（不偏分散）
#                 All_list['std_ddof=1'].append(dataset1.std(ddof=1)) # 標準偏差（不偏分散）

#             #Step-3：特性深度分布の計算結果と紐付け情報を格納したDATAFRAME（df_all）をcsv保存
#             # 保存名は最初の農場名+変換日時∔CSV・・暫定的に
#             df_all = pd.DataFrame(All_list)
#             today = datetime.datetime.today()
#             yyyymmdd = today.strftime('%Y%m%d-%H%M%S')
#             save_name1 = All_list['nojyomei'][i] + '_' + yyyymmdd + '.csv'
#             filedir = 'C:/Users/minam/Desktop/tokusei_csv/'
#             save_name2 = filedir + save_name1
#             # print(save_name2)
#             # df_all.to_csv(save_name2 + '.csv', encoding='SHIFT-JIS', index=False)
#             # ここまで未処理
