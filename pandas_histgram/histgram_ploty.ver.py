import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

# 【下準備】表示の制限・・jupyterlabのみ有効
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)

# 【下準備】取り込むリストのDBフォーマットの決定
All_list = {
    'nojyomei': [],
    'item': [],
    'hojyomei': [],
    'ymd': [],
    'jiki': [],
    'class_index': [],
    'class_value': [],
    'freq': [],
    'rel_freq': [],
    'cum_freq': [],
    'rel_cum_freq': []
}

# 所定データの読み込み・・☆☆ここに読み込ませたいcsvファイルをセットする
df = pd.read_csv('C:/Users/minam/Desktop/mypandas/data_sample1.csv', encoding='Shift-JIS', header=0)

# Step-1：農場名での分類
nojyomei_list = df['農場名'].tolist()
nojyomei_list = list(set(nojyomei_list))
nojyomei_list_count = len(nojyomei_list)

# Step-2：圃場名でのデータ抽出と所定DATAFRAMEへの格納
for i in range(len(nojyomei_list)):
    nojyomei = df['農場名'][i]
    df1 = df[df['農場名'] == nojyomei]
    hojyomei_list = df1['圃場名'].tolist()
    hojyomei_list = list(set(hojyomei_list))
    hojyomei_list_count = len(hojyomei_list)
    for j in range(len(hojyomei_list)):
        hojyomei = hojyomei_list[j]
        df2 = df1[df1['圃場名'] == hojyomei]
        dataset1 = df2['xC']

        # 品目・時期をAll_listに格納し、エラー（2つ以上ある場合）を検知する
        item_list = df2['品目'].tolist()
        item_list_count = len(set(item_list))
        if not item_list_count == 1:
            print("エラー：品目が2つ以上あります。")
            break
        else:
            All_list['item'].append(list(set(item_list))[0])
        jiki_list = df2['時期'].tolist()
        jiki_list_count = len(set(jiki_list))
        if not jiki_list_count == 1:
            print("エラー：時期が2つ以上あります。")
            break
        else:
            All_list['jiki'].append(list(set(jiki_list))[0])

        # 農場名と圃場名をAll_listに格納
        All_list['nojyomei'].append(list(set(nojyomei_list))[0])
        All_list['hojyomei'].append(list(set(hojyomei_list))[j])

        # 測定日をdatetimeに変換してAll_listに格納し、エラー（2つ以上ある場合）を検知する
        sokuteibi = df2['測定日'].tolist()
        sokuteibi_count = len(set(sokuteibi))
        if not sokuteibi_count == 1:
            print("エラー：測定日が2つ以上あります。")
            break
        else:
            sokuteibi2 = sokuteibi[j] + ' ' + '00:00:00'
            sokuteibi2 = datetime.datetime.strptime(sokuteibi2, '%Y.%m.%d %H:%M:%S')
            All_list['ymd'].append(sokuteibi2)

        # ヒストグラムの計算値をAll_listに格納
        bins = np.linspace(0, 60, 13)
        freq = dataset1.value_counts(bins=bins, sort=False)
        All_list['freq'].append(freq)
        class_value = (bins[:-1] + bins[1:]) / 2  # 階級値
        All_list['class_value'].append(class_value)
        rel_freq = freq / dataset1.count()  # 相対度数
        All_list['rel_freq'].append(rel_freq)
        cum_freq = freq.cumsum()  # 累積度数
        All_list['cum_freq'].append(cum_freq)
        rel_cum_freq = rel_freq.cumsum()  # 相対累積度数
        All_list['rel_cum_freq'].append(rel_cum_freq)
        class_index = freq.index  # 階層
        All_list['class_index'].append(class_index)
    df_all = pd.DataFrame(All_list)
    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y%m%d')
    save_name = All_list['nojyomei'][0] + '_' + yyyymmdd + '.csv'
    # 特性深度分布の計算結果と紐付け情報を格納したDATAFRAME（df_all）をcsv保存
    df_all.to_csv(save_name, encoding='SHIFT-JIS', index=False)

# 圃場比較グラフ（度数）の生成と保存（JPEG、HTML）
    nojyomei = df_all['nojyomei'][0]

    fig = go.Figure()
    for k in range(len(df_all['hojyomei'])):
        fig.add_trace(go.Bar(x=df_all['class_value'][0],
                             y=df_all['freq'][k],
                             name=df_all['hojyomei'][k],
                             width=1.2,
                             hovertemplate='度数:%{y}, 深度:%{x}cm')
                      )
    fig.update_layout(title=dict(text='圃場比較（度数）_特性深度分布_' + nojyomei,
                                 font=dict(size=20, color='black'),
                                 xref='paper',
                                 x=0.5,
                                 y=0.9,
                                 xanchor='center'
                                 ),
                      xaxis=dict(title='深度（㎝）', range=(0, 60)),
                      yaxis=dict(title='度数', range=(0, 50)),
                      legend=dict(orientation='h',
                                  xanchor='left',
                                  x=0.02,
                                  yanchor='bottom',
                                  y=0.9),
                      width=600,
                      height=400,
                      plot_bgcolor='whitesmoke'
                      )
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    fig.write_image('圃場比較（度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
    fig.write_html('圃場比較（度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
    fig.show()

    # 圃場比較グラフ（相対度数）の生成と保存（JPEG、HTML）
    fig = go.Figure()
    for n in range(len(df_all['hojyomei'])):
        fig.add_trace(go.Scatter(x=df_all['class_value'][0],
                                 y=df_all['rel_freq'][n],
                                 name=df_all['hojyomei'][n],
                                 mode='markers+lines',
                                 marker=dict(size=5),
                                 hovertemplate='相対度数:%{y}, 深度:%{x}cm')
                      )
    fig.update_layout(title=dict(text='圃場比較（度数）_特性深度分布_' + nojyomei,
                                 font=dict(size=20, color='black'),
                                 xref='paper',
                                 x=0.5,
                                 y=0.9,
                                 xanchor='center'
                                 ),
                      xaxis=dict(title='深度（㎝）', range=(0, 60)),
                      yaxis=dict(title='相対度数', range=(0, 1), tickformat='%'),
                      legend=dict(orientation='h',
                                  xanchor='left',
                                  x=0.02,
                                  yanchor='bottom',
                                  y=0.9),
                      width=600,
                      height=400,
                      plot_bgcolor='whitesmoke'
                      )
    fig.layout.yaxis.tickformat = ',.0%'
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    fig.write_image('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
    fig.write_html('圃場比較（相対度数）_特性深度分布_' + nojyomei + '_' + yyyymmdd + '.html')
    fig.show()

    # 各圃場ごとに特性深度分布グラフ（度数・相対度数）を生成し、保存（JPEG、HTML）
    for m, (d1, d2) in enumerate(zip(df_all['freq'], df_all['rel_freq'])):
        # 圃場別特性深度分布グラフ（度数）を生成・保存（JPEG、HTML）
        fig = go.Figure()
        hojyomei = df_all['hojyomei'][m]
        fig.add_trace(go.Bar(x=df_all['class_value'][0],
                             y=d1,
                             name=hojyomei,
                             width=3,
                             hovertemplate='度数:%{y}, 深度:%{x}cm', showlegend=True)
                      )
        fig.update_layout(title=dict(text='特性深度分布（度数）_' + nojyomei + '_' + yyyymmdd,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.5,
                                     y=0.9,
                                     xanchor='center'
                                     ),
                          xaxis=dict(title='深度（㎝）', range=(0, 60)),
                          yaxis=dict(title='度数', range=(0, 50)),
                          legend=dict(orientation='h',
                                      xanchor='left',
                                      x=0.02,
                                      yanchor='bottom',
                                      y=0.9,
                                      bgcolor='white',
                                      bordercolor='grey'
                                      ),
                          width=600,
                          height=400,
                          plot_bgcolor='whitesmoke'
                          )
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
        fig.write_image('特性深度分布（度数）_' + nojyomei + '_' + hojyomei + '_' + yyyymmdd + '.jpeg')
        fig.write_html('特性深度分布（度数）' + nojyomei + '_' + hojyomei + '_' + yyyymmdd + '.html')
        fig.show()
        # 圃場別特性深度分布グラフ（相対度数）を生成・保存（JPEG、HTML）
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_all['class_value'][0],
                                 y=d2,
                                 name=hojyomei,
                                 mode='markers+lines',
                                 marker=dict(size=5),
                                 showlegend=True,
                                 hovertemplate='相対度数:%{y}, 深度:%{x}cm')
                      )
        fig.update_layout(title=dict(text='特性深度分布（相対度数）_' + nojyomei + '_' + yyyymmdd,
                                     font=dict(size=20, color='black'),
                                     xref='paper',
                                     x=0.5,
                                     y=0.9,
                                     xanchor='center'
                                     ),
                          xaxis=dict(title='深度（㎝）', range=(0, 60)),
                          yaxis=dict(title='相対度数', range=(0, 1), tickformat='%'),
                          legend=dict(orientation='h',
                                      xanchor='left',
                                      x=0.02,
                                      yanchor='bottom',
                                      y=0.9,
                                      bgcolor='white',
                                      bordercolor='grey'
                                      ),
                          width=600,
                          height=400,
                          plot_bgcolor='whitesmoke'
                          )
        fig.layout.yaxis.tickformat = ',.0%'
        fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
        fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
        fig.write_image('特性深度分布（相対度数）_' + nojyomei + '_' + hojyomei + '_' + yyyymmdd + '.jpeg')
        fig.write_html('特性深度分布（相対度数）_' + nojyomei + '_' + hojyomei + '_' + yyyymmdd + '.html')
        fig.show()
