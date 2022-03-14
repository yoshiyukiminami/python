import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 日本語対応
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc', size=12)

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

# Step-2：圃場名での分類
for i in range(len(nojyomei_list)):
    # for nojyomei in nojyomei_list:
    nojyomei = df['農場名'][i]
    df1 = df[df['農場名'] == nojyomei]
    hojyomei_list = df1['圃場名'].tolist()
    hojyomei_list = list(set(hojyomei_list))
    hojyomei_list_count = len(hojyomei_list)
    for j in range(len(hojyomei_list)):
        # for hojyomei in hojyomei_list:
        hojyomei = hojyomei_list[j]
        df2 = df1[df1['圃場名'] == hojyomei]
        dataset1 = df2['パラメータD']
        print(dataset1)

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

        print(nojyomei)
        print(hojyomei)
        print(sokuteibi2)

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
    df_all.to_csv('aaa.csv', encoding='SHIFT-JIS', index=False)

    # グラフの装飾
    # plt.xlim(0, 60)                 # (1) x軸の表示範囲
    # plt.ylim(0, 50)                 # (2) y軸の表示範囲
    # plt.title("特性深度ヒストグラム", fontproperties=fp, fontsize=14)  # (3) タイトル
    # plt.xlabel("深度（㎝）", fontproperties=fp, fontsize=12)            # (4) x軸ラベル
    # plt.ylabel("度数", fontproperties=fp, fontsize=12)      # (5) y軸ラベル
    # plt.grid(True)                            # (6) 目盛線の表示
    # plt.tick_params(labelsize = 12)    # (7) 目盛線のラベルサイズ
    # plt.legend(loc="upper right", prop=fp, fontsize=13) # (5)凡例表示
    # グラフの描画
    # plt.hist(dataset1 , alpha=0.5, bins=13, range=(0, 60), label=hojyomei, color= 'r') #(8) ヒストグラムの描画
    # plt.show()
    # dataset1

    for k in range(len(df_all)):
        print(k)
        dist1 = df_all.iloc[[k]]
        print(dist1)
        title_name = [dist1['nojyomei'].str.cat([dist1['hojyomei'], dist1['item']], sep='_')]
        print(title_name)
        dist1 = pd.DataFrame(
            {
                "階級値": class_value,
                "度数": freq,
                "相対度数": rel_freq,
                "累積度数": cum_freq,
                "相対累積度数": rel_cum_freq,
            },
            index=freq.index
        )

        fig, ax1 = plt.subplots()
        dist1.plot.bar(x="階級値", y="度数", ax=ax1, color='g', width=0.5, ec='g', lw=2)
        plt.title(title_name, fontproperties=fp)
        plt.xlabel('深度（㎝）', fontproperties=fp)
        plt.ylabel('度数', fontproperties=fp)
        plt.ylim(0, 50)
        plt.grid(True)

        ax2 = ax1.twinx()
        ax2.plot(np.arange(len(dist1)), dist1["相対累積度数"], "--o", color='orange')
        ax2.set_ylabel("相対累積度数", fontproperties=fp)
        plt.legend(loc='best', prop=fp)
        print(fig)
        # fig.savefig(k+ '.jpeg')
