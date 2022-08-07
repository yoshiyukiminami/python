import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt

# 【下準備】日本語対応
plt.rcParams['font.family'] = 'Meiryo'

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

    # 【グラフ下準備】棒の配置位置、ラベルを用意
    x = All_list['class_value'][0]
    labels = All_list['hojyomei']

    # 【グラフ下準備】各系列のデータをAll_listから抽出
    df_series1 = All_list['freq']
    df_series2 = All_list['rel_cum_freq']

    # 【グラフ下準備】グラフサイズを統一
    plt.figure(figsize=[8, 6])

    # 【グラフ下準備】マージンを設定+圃場比較は7圃場までに制限・・圃場比較_特性深度分布のみ
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

    # 【グラフ-1】各圃場毎に特性深度分布（度数と相対累積度数）の複合グラフを生成、JPEG保存
    for k, (v1, v2) in enumerate(zip(df_series1, df_series2)):
        # print(i,v1,v2)
        # pos = x - total_width *( 1- (2*k+1)/len(df_series1) )/2
        fig = plt.figure()
        ax1 = fig.add_subplot()
        ax2 = ax1.twinx()
        # ax1.bar(pos, v1, width = total_width/len(df_series1), label=labels[i], color='g')
        ax1.bar(x, v1, width=3.5, label=labels[k], color='g')
        ax2.plot(x, v2, "--o", label=labels[k], color='orange')
        ax1.set_title('圃場別_特性深度分布' + '_' + nojyomei, size=16)
        ax1.set_xlabel('深度（㎝）', size=12)
        ax1.set_ylabel('度数', size=12)
        ax1.set_ylim(0, 50)
        ax1.grid(axis='y', linestyle='dotted', color='r')
        ax1.set_xticks(x)
        ax2.set_ylabel('相対累積度数', size=12)
        ax2.set_ylim(0, 1)
        ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        handler1, label1 = ax1.get_legend_handles_labels()
        handler2, label2 = ax2.get_legend_handles_labels()
        ax1.legend(handler1 + handler2, label1 + label2, borderaxespad=0, loc='center right')
        fig.savefig('特性深度分布_' + nojyomei + '_' + labels[k] + '_' + yyyymmdd + '.jpeg')

    # 【グラフ-2】全圃場での比較グラフ（度数、相対累積度数の複合）の生成、JPEG保存
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    for l, (y1, y2) in enumerate(zip(df_series1, df_series2)):
        pos = x - total_width * (1 - (2 * l + 1) / len(df_series1)) / 2
        ax1.bar(pos, y1, width=total_width / len(df_series1), label=labels[l])
        ax2.plot(x, y2, "--o", label=labels[l], linewidth=1, markersize=2)
        handler1, label1 = ax1.get_legend_handles_labels()
        handler2, label2 = ax2.get_legend_handles_labels()
    ax1.set_title('圃場比較_特性深度分布_' + nojyomei, size=16)
    ax1.set_xlabel('深度（㎝）', size=12)
    ax1.set_ylabel('度数', size=12)
    ax1.set_ylim(0, 50)
    ax1.grid(axis='y', linestyle='dotted', color='r')
    ax1.set_xticks(x)
    ax1.legend(handler1 + handler2, label1 + label2, borderaxespad=0, loc='center right')
    ax2.set_ylabel('相対累積度数', size=12)
    ax2.set_ylim(0, 1)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    fig.savefig('特性深度分布_' + nojyomei + '_' + yyyymmdd + '.jpeg')
