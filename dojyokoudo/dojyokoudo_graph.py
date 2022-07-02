import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import glob

# 【全体設定】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)


def koudobunpu_dataset():
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

    # 【Step-2】1～60㎝のデータ列を取り出す
    df_dp = df2.drop(df2.columns[range(72, 110)], axis=1)
    df_dp = df_dp.drop(df_dp.columns[range(0, 12)], axis=1)
    # print(df_dp)

    # 【Step-3】品目・時期・測定日でエラー（2つ以上ある場合）を検知しAll_listに格納する
    item_list = df2['品目'].tolist()
    item_list_count = len(set(item_list))
    isvalid = True
    if not item_list_count == 1:
        print("エラー：品目が2つ以上あります。")
        isvalid = False
    else:
        All_list['item'].append(set(item_list))
        jiki_list = df2['時期'].tolist()
        jiki_list_count = len(set(jiki_list))
        if not jiki_list_count == 1:
            print("エラー：時期が2つ以上あります。")
            isvalid = False
        else:
            All_list['jiki'].append(set(jiki_list))
            sokuteibi = df2['測定日'].tolist()
            sokuteibi_count = len(set(sokuteibi))
            if not sokuteibi_count == 1:
                print("エラー：測定日が2つ以上あります。")
                isvalid = False
            else:
                # 測定日をdatetimeに変換する
                sokuteibi2 = sokuteibi[0] + ' ' + '00:00:00'
                sokuteibi2 = datetime.datetime.strptime(sokuteibi2, '%Y.%m.%d %H:%M:%S')
                All_list['ymd'].append(sokuteibi2)

    # 【Step-3】農場名・圃場名・圃場内位置・圃場内位置2をAll_listに格納する
    All_list['nojyomei'].append(set(df2['農場名']))
    All_list['hojyomei'].append(set(df2['圃場名']))
    All_list['point1'].append(set(df2['圃場内位置']))
    All_list['point2'].append(set(df2['圃場内位置2']))

    # 【Step-4】df_dpに格納したデータ（文字列含む）を一括でmeanする
    df_ave = df_dp.mean()
    print(df_ave)
    for i in range(0, 60):
        j = str(i + 1) + 'cm'
        # print(i, j)
        All_list[j].append(df_ave[i])

    print(All_list)


# #ここから未処理
# def koudobunpu_graphset():
#     #硬度分布グラフ（折れ線）の生成と保存（JPEG、HTML）
#     fig = go.Figure()
#     for l in range(len(df_all['hojyomei'])):
#         fig.add_trace(go.Scatter(y=df_all['class_value'][0],
#                                  x=df_all['rel_freq'][l],
#                                  name=df_all['hojyomei'][l],
#                                  mode='markers+lines',
#                                  marker=dict(size=5),
#                                  hovertemplate='相対度数:%{x}, 深度:%{y}cm',
#                                 orientation='h')
#                      )
#     fig.update_layout(title=dict(text='圃場比較（度数）_特性深度分布_' + nojyomei,
#                                  font=dict(size=20, color='black'),
#                                  xref='paper',
#                                  x=0.01,
#                                  y=0.9,
#                                  xanchor='left'
#                                 ),
#                       yaxis=dict(title='深度（㎝）', range=(60, 0)),
#                       xaxis=dict(title='相対度数', range=(0, 1), tickformat='%'),
#                       legend=dict(orientation='h',
#                                   xanchor='left',
#                                   x=0.6,
#                                   yanchor='bottom',
#                                   y=0.9),
#                       width=600,
#                       height=400,
#                       plot_bgcolor='white'
#                      )
#     fig.layout.xaxis.tickformat= ',.0%'
#     fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
#     fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
#     fig.write_image('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
#     fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
#     fig.show()


if __name__ == '__main__':
    # ☆所定データの読み込み・・【展開】特定フォルダから複数ファイルを同時に読み込む処理
    filedir = 'C:/Users/minam/Desktop/tokusei_precal/'
    files = glob.glob(filedir + '/**/*.csv')
    print(files)

    # 読み込んだファイルを「農場名」「圃場名」「圃場内測定位置」「圃場内測定位置2」で分類し、df2に格納
    for file in files:
        print(file)
        df = pd.read_csv(file, encoding='Shift-JIS', header=0)
        # print(df)

        # Step-1：農場名での分類
        nojyomei_list = df['農場名'].tolist()
        nojyomei_list = list(set(nojyomei_list))
        nojyomei_list_count = len(nojyomei_list)
        # print(nojyomei_list, nojyomei_list_count)

        # ここから未処理
        # Step-2：圃場名でのデータ抽出と所定DATAFRAMEへの格納
        for i in range(len(nojyomei_list)):
            nojyomei = nojyomei_list[i]
            df = df[df['農場名'] == nojyomei]
            hojyomei_list = df['圃場名'].tolist()
            hojyomei_list = list(set(hojyomei_list))
            hojyomei_list_count = len(hojyomei_list)
            # print(i, nojyomei, hojyomei_list, hojyomei_list_count)

            for j in range(len(hojyomei_list)):
                hojyomei = hojyomei_list[j]
                df = df[df['圃場名'] == hojyomei]
                # print(j, hojyomei)
                point1_list = df['圃場内位置'].tolist()
                point2_list = df['圃場内位置2'].tolist()
                point1_list = list(set(point1_list))
                point2_list = list(set(point2_list))
                # print(point1_list, point2_list)
                # koudobunpu_dataset()

                # 測定位置情報のエラー検知
                isvalid = True
                if not len(point1_list) == len(point2_list):
                    print("測定位置情報が一致しません")
                    isvalid = False
                    # break
                else:
                    # 圃場内測定位置・圃場内測定位置2の組み合わせ毎にdf2のデータフレームに格納
                    for k in point1_list:
                        df1 = df[df['圃場内位置'] == k]
                        print(k)
                        for m in point2_list:
                            df2 = df1[df1['圃場内位置2'] == m]
                            print(m)
                            koudobunpu_dataset()
