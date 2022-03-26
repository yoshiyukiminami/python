import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt

# from matplotlib.font_manager import FontProperties

# 日本語対応
# fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc',size=12)
plt.rcParams['font.family'] = 'Meiryo'

# 表示の制限
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)

# 取り込むリストのDBフォーマットを決める
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

# ☆データの読み込み・・ここに読み込ませたいcsvファイルをセットする
df = pd.read_csv('C:/Users/minam/Desktop/mypandas/data_sample1.csv', encoding='Shift-JIS', header=0)

# Step-1：農場名での分類
nojyomei_list = df['農場名'].tolist()
nojyomei_list = list(set(nojyomei_list))
nojyomei_list_count = len(nojyomei_list)

# Step-2：圃場名での分類4
for i in range(len(nojyomei_list)):
    nojyomei = df['農場名'][i]
    df1 = df[df['農場名'] == nojyomei]
    hojyomei_list = df1['圃場名'].tolist()
    hojyomei_list = list(set(hojyomei_list))
    hojyomei_list_count = len(hojyomei_list)
    for j in range(len(hojyomei_list)):
        hojyomei = hojyomei_list[j]
        df2 = df1[df1['圃場名'] == hojyomei]
        dataset1 = df2['パラメータD']

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
        sokuteibi = df2['計測日'].tolist()
        sokuteibi_count = len(set(sokuteibi))
        if not sokuteibi_count == 1:
            print("エラー：計測日が2つ以上あります。")
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
    # df_all.to_csv(save_name, encoding='SHIFT-JIS', index=False)

    # 複数圃場を比較するヒストグラム・グラフ生成
    # 棒の配置位置、ラベルを用意
    x = All_list['class_value'][0]
    labels = All_list['hojyomei']

    # 各系列のデータを用意
    df_series1 = All_list['freq']
    df_series2 = All_list['rel_cum_freq']
    print(df_series1, df_series2)

    # マージンを設定（比較は7圃場までに制限）
    margin = 0.2  # 0 <margin< 1
    if len(df_series1) <= 3:
        bar_width = 4
    else:
        if len(df_series1) > 7:
            print("比較する圃場数が多過ぎます。7圃場以下にしてください")
            break
        else:
            bar_width = len(df_series1) * 0.7
    total_width = bar_width - margin
    print(margin, total_width)

    # 各圃場毎に度数と相対累積度数の複合グラフを生成、JPEGとして保存
    for k, (v1, v2) in enumerate(zip(df_series1, df_series2)):
        # print(i,v1,v2)
        # pos = x - total_width *( 1- (2*i+1)/len(df_series1) )/2
        fig = plt.figure(figsize=(8, 6))
        ax1 = fig.add_subplot()
        ax2 = ax1.twinx()
        # ax1.bar(pos, v1, width = total_width/len(df_series1), label=labels[i], color='g')
        ax1.bar(x, v1, width=3.5, label=labels[k], color='g')
        ax2.plot(x, v2, "--o", label=labels[k], color='orange')
        ax1.set_title('圃場別_特性深度分布' + '_' + nojyomei)
        ax1.set_xlabel('深度（㎝）')
        ax1.set_ylabel('度数')
        ax1.set_ylim(0, 50)
        ax1.grid(axis='y', linestyle='dotted', color='r')
        ax1.set_xticks(x)
        ax2.set_ylabel('相対累積度数')
        ax2.set_ylim(0, 1)
        ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        handler1, label1 = ax1.get_legend_handles_labels()
        handler2, label2 = ax2.get_legend_handles_labels()
        ax1.legend(handler1 + handler2, label1 + label2, borderaxespad=0, loc='center right')
        fig.savefig('特性深度分布_' + nojyomei + '_' + labels[k] + '_' + yyyymmdd + '.jpeg')

    # #グラフ化のための繰り返し処理（旧）
    # for k in range(len(df_all)):
    # dist1 = df_all.iloc[k]
    # title_name = dist1['nojyomei'] + '_' + dist1['hojyomei'] + '_' + dist1['item'] + '_' + str(dist1['ymd'])
    # title_name = title_name.split(' ')[0]
    # label_name = dist1['hojyomei']
    # dist1 = pd.DataFrame(
    #     {"階級値": dist1['class_value'],
    #           "度数": dist1['freq'],
    #           "相対度数": dist1['rel_freq'],
    #           "累積度数": dist1['cum_freq'],
    #           "相対累積度数": dist1['rel_cum_freq'],
    #     },
    #     index=freq.index
    # )
    # #複合グラフ作成（度数=棒グラフ、累積相対度数=折れ線グラフ・2軸）
    # fig, ax1 = plt.subplots()
    # dist1.plot.bar(x="階級値", y="度数", label=label_name, ax=ax1, color='g', width=0.5, ec='g', lw=2)
    # plt.title(title_name)
    # plt.xlabel('深度（㎝）')
    # plt.ylabel('度数')
    # plt.ylim(0, 50)
    # plt.grid(True)
    # ax2 = ax1.twinx()
    # ax2.plot(np.arange(len(dist1)), dist1["相対累積度数"], "--o", color='orange', label=label_name)
    # ax2.set_ylabel("相対累積度数")
    # ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    # handler1, label1 = ax1.get_legend_handles_labels()
    # handler2, label2 = ax2.get_legend_handles_labels()
    # ax1.legend(handler1+handler2, label1+label2, borderaxespad=0, loc='upper left')
    # fig.savefig(title_name + '.jpeg')
