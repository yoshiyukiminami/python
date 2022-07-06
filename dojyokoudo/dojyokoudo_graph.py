import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import glob

# 【全体設定】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)


def koudobunpu_dataset(df2):
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
                                             hovertemplate='硬さ:%{x:.1f}kpa, 深度:%{y}',
                                             orientation='h')
                                  )
                    fig.update_layout(title=dict(text='土壌硬度分布_' + nojyomei + '_' + hojyomei,
                                                 font=dict(size=20, color='black'),
                                                 xref='paper',
                                                 x=0.01,
                                                 y=0.9,
                                                 xanchor='left'
                                                 ),
                                      yaxis=dict(title='深度（㎝）', range=(60, 1)),
                                      xaxis=dict(title='硬さ（kpa）', range=(200, 3000)),
                                      legend=dict(orientation='h',
                                                  xanchor='left',
                                                  x=0.3,
                                                  yanchor='bottom',
                                                  y=0.9),
                                      width=600,
                                      height=800,
                                      plot_bgcolor='white'
                                      )
                    fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
                    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
                # fig.write_image(save_name + '.jpeg', engine='kaleido')
                # fig.write_image('土壌硬度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
                # fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
                fig.show()


def matrix_graphset_a(df_dp, nojyomei, hojyomei, marker_color, marker_symbol):
    # 【Step-1】 散布図A（特性震度×飽和硬度）の生成と保存
    fig = go.Figure()
    for i in range(len(df_dp)):
        point1 = df_dp['圃場内位置'][i]
        point2 = str(df_dp['圃場内位置2'][i])
        name = point1 + '-' + str(point2)
        color = marker_color[point1]
        symbol = marker_symbol[point2]
        x = [df_dp['xC'][i]]
        y = [df_dp['s2'][i]]
        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 name=name,
                                 mode='markers',
                                 marker={'size': 12, 'symbol': symbol,
                                         'color': color,
                                         'opacity': 0.6,
                                         'line': {'width': 0.5,
                                                  'color': color}},
                                 hovertemplate='特性深度:%{x:.1f}cm, 飽和硬度:%{y:.2f}Mpa',
                                 orientation='h')
                      )
        fig.update_layout(title=dict(text='特性深度×飽和硬度_' + nojyomei + '_' + hojyomei,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.01,
                                     y=0.87,
                                     xanchor='left'
                                     ),
                          yaxis=dict(title='硬さMpa）', range=(0, 3)),
                          xaxis=dict(title='深度（cm）', range=(1, 60)),
                          showlegend=False,
                          # legend=dict(orientation='h',
                          #             xanchor='left',
                          #             x=0.3,
                          #             yanchor='bottom',
                          #             y=0.95),
                          width=600,
                          height=600,
                          plot_bgcolor='white'
                          )
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    # fig.write_image(save_name + '.jpeg')
    # fig.write_image('土壌硬度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
    # fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
    fig.show()


def matrix_graphset_b(df_dp, nojyomei, hojyomei, marker_color, marker_symbol):
    # 【Step-1】 散布図B（特性震度×緩衝因子）の生成と保存
    fig = go.Figure()
    for j in range(len(df_dp)):
        point1 = df_dp['圃場内位置'][j]
        point2 = str(df_dp['圃場内位置2'][j])
        name = point1 + '-' + str(point2)
        color = marker_color[point1]
        symbol = marker_symbol[point2]
        x = [df_dp['xC'][j]]
        y = [df_dp['ηC'][j]]
        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 name=name,
                                 mode='markers',
                                 marker={'size': 12, 'symbol': symbol,
                                         'color': color,
                                         'opacity': 0.6,
                                         'line': {'width': 0.5,
                                                  'color': color}},
                                 hovertemplate='特性深度:%{x:.1f}cm, 緩衝因子:%{y:.1f}',
                                 orientation='h')
                      )
        fig.update_layout(title=dict(text='特性深度×緩衝因子_' + nojyomei + '_' + hojyomei,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.01,
                                     y=0.87,
                                     xanchor='left'
                                     ),
                          yaxis=dict(title='硬さの緩急', range=(0, 15000)),
                          xaxis=dict(title='深度（cm）', range=(1, 60)),
                          showlegend=False,
                          # legend=dict(orientation='h',
                          #             xanchor='left',
                          #             x=0.3,
                          #             yanchor='bottom',
                          #             y=0.95),
                          width=600,
                          height=600,
                          plot_bgcolor='white'
                          )
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    # fig.write_image(save_name + '.jpeg')
    # fig.write_image('土壌硬度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
    # fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
    fig.show()


def matrix_graphset_c(df_dp, nojyomei, hojyomei, marker_color, marker_symbol):
    # 【Step-1】 散布図C（特性震度×硬度勾配）の生成と保存
    fig = go.Figure()
    for j in range(len(df_dp)):
        point1 = df_dp['圃場内位置'][j]
        point2 = str(df_dp['圃場内位置2'][j])
        name = point1 + '-' + str(point2)
        color = marker_color[point1]
        symbol = marker_symbol[point2]
        x = [df_dp['xC'][j]]
        y = [df_dp.iloc[j, 14]]
        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 name=name,
                                 mode='markers',
                                 marker={'size': 12, 'symbol': symbol,
                                         'color': color,
                                         'opacity': 0.6,
                                         'line': {'width': 0.5,
                                                  'color': color}},
                                 hovertemplate='特性深度:%{x:.1f}cm, 硬度勾配:%{y:.1f}',
                                 orientation='h')
                      )
        fig.update_layout(title=dict(text='特性深度×硬度勾配_' + nojyomei + '_' + hojyomei,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.01,
                                     y=0.87,
                                     xanchor='left'
                                     ),
                          yaxis=dict(title='硬さの緩急', range=(0, 1)),
                          xaxis=dict(title='深度（cm）', range=(1, 60)),
                          showlegend=False,
                          # legend=dict(orientation='h',
                          #             xanchor='left',
                          #             x=0.3,
                          #             yanchor='bottom',
                          #             y=0.95),
                          width=600,
                          height=600,
                          plot_bgcolor='white'
                          )
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    # fig.write_image(save_name + '.jpeg')
    # fig.write_image('土壌硬度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
    # fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
    fig.show()


def matrix_graphset_d(df_dp, nojyomei, hojyomei, marker_color, marker_symbol):
    # 【Step-1】 散布図D（最大深度×飽和硬度）の生成と保存
    fig = go.Figure()
    for j in range(len(df_dp)):
        point1 = df_dp['圃場内位置'][j]
        point2 = str(df_dp['圃場内位置2'][j])
        name = point1 + '-' + str(point2)
        color = marker_color[point1]
        symbol = marker_symbol[point2]
        x = [df_dp['x2'][j]]
        y = [df_dp['s2'][j]]
        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 name=name,
                                 mode='markers',
                                 marker={'size': 12, 'symbol': symbol,
                                         'color': color,
                                         'opacity': 0.6,
                                         'line': {'width': 0.5,
                                                  'color': color}},
                                 hovertemplate='最大深度:%{x:.1f}cm, 飽和硬度:%{y:.1f}Mpa',
                                 orientation='h')
                      )
        fig.update_layout(title=dict(text='最大深度×飽和硬度_' + nojyomei + '_' + hojyomei,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.01,
                                     y=0.87,
                                     xanchor='left'
                                     ),
                          yaxis=dict(title='硬度（Mpa）', range=(0, 3)),
                          xaxis=dict(title='深度（cm）', range=(1, 60)),
                          showlegend=False,
                          # legend=dict(orientation='h',
                          #             xanchor='left',
                          #             x=0.3,
                          #             yanchor='bottom',
                          #             y=0.95),
                          width=600,
                          height=600,
                          plot_bgcolor='white'
                          )
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    # fig.write_image(save_name + '.jpeg')
    # fig.write_image('土壌硬度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
    # fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
    fig.show()


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
                    koudobunpu_dataset(df2)  # 土壌硬度分布（折れ線）
                    # 【Step-1】df2から不必要な列を削除する・・散布図生成の共通処理
                    df_dp = df2.drop(df2.columns[range(8, 102)], axis=1)
                    df_dp = df_dp.drop(df_dp.columns[range(0, 1)], axis=1)
                    df_dp.reset_index(inplace=True, drop=True)
                    nojyomei = df_dp.iat[0, 0]
                    hojyomei = df_dp.iat[0, 2]
                    # 事前準備1：測定位置ごとの色・線のプロパティを決める・・散布図生成の共通処理
                    marker_color = {'A': '#1616A7', 'B': '#1CA71C', 'C': '#FB0D0D'}
                    marker_symbol = {'1': 'square', '2': 'diamond', '3': 'triangle-up'}
                    matrix_graphset_a(df_dp, nojyomei, hojyomei, marker_color, marker_symbol)  # 特性深度×飽和硬度
                    matrix_graphset_b(df_dp, nojyomei, hojyomei, marker_color, marker_symbol)  # 特性深度×緩衝因子
                    matrix_graphset_c(df_dp, nojyomei, hojyomei, marker_color, marker_symbol)  # 特性深度×硬度勾配
                    matrix_graphset_d(df_dp, nojyomei, hojyomei, marker_color, marker_symbol)  # 最大深度×飽和硬度
