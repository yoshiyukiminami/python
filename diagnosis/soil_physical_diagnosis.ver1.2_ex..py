import pandas as pd
import numpy as np
import datetime
import time
import glob
import matplotlib
import matplotlib.pyplot as plt

# exとの違いは生成したグラフの保存先
# Ver1.2・・ID列追加と保存名にID追加、基準値の変更（15㎝→20㎝）
# グラフの保存名に「_ver1.2」を追加

# 【下準備】日本語対応
plt.rcParams['font.family'] = 'Meiryo'
# 【グラフ下準備】グラフサイズを統一
plt.figure(figsize=[12, 8], dpi=72)

def graphset_1x3(df_all, df_ave, line_color, line_shape, y, graph_title):
    # 1つのfigに4つのaxesを行2×列2で描画
    fig, axes = plt.subplots(1, 3, tight_layout=True, squeeze=False)
    # 【特性深度分布（度数）_0, 0】df_allの'freq'をX軸に設定
    x = df_all['freq'][0]
    # 【特性深度分布（度数）_0, 0】グラフ生成
    # 「50%」「std_ddof=1」の数値がによってBAR・線色を変更する
    data_set_high = {'50%': 30, 'std_ddof=1': 3}
    # 基準値を15㎝から20㎝に変更（20221207）
    data_set_low = {'50%': 20, 'std_ddof=1': 7}
    sakudoshin = df_all['50%'][0]
    sakudoshin_h = data_set_high['50%']
    sakudoshin_l = data_set_low['50%']
    baratsuki = df_all['std_ddof=1'][0]
    baratsuki_h = data_set_high['std_ddof=1']
    baratsuki_l = data_set_low['std_ddof=1']
    # sakudoshin2 = '{:.1f}'.format(sakudoshin)
    # baratsuki2 = '{:.1f}'.format(baratsuki)
    sakudoshin3 = sakudoshin - baratsuki
    sakudoshin4 = sakudoshin + baratsuki
    # print(sakudoshin3, sakudoshin4)
    if sakudoshin >= sakudoshin_h:
        s_color = 'y'
    else:
        if sakudoshin <= sakudoshin_l:
            s_color = 'b'
        else:
            s_color = 'grey'
    axes[0, 0].barh(y, x, color=s_color, height=4, align='center')
    axes[0, 0].set_title('特性深度分布（度数）', size=10)
    axes[0, 0].set_xlabel('度数（ポイント）', size=8)
    axes[0, 0].set_ylabel('深さ（㎝）', size=8)
    axes[0, 0].set_xlim(0, 50)
    axes[0, 0].set_ylim(60, 1)
    axes[0, 0].axhline(sakudoshin, linestyle='--', color='r', lw=1.5, alpha=0.5)
    axes[0, 0].axhline(10, linestyle=':', color='grey', lw=0.5)
    axes[0, 0].axhline(20, linestyle=':', color='grey', lw=0.5)
    axes[0, 0].axhline(30, linestyle=':', color='grey', lw=0.5)
    axes[0, 0].axhline(40, linestyle=':', color='grey', lw=0.5)
    axes[0, 0].axhline(50, linestyle=':', color='grey', lw=0.5)
    axes[0, 0].axvline(25, linestyle=':', color='grey', lw=0.5)
    axes[0, 0].minorticks_on()

    # 【特性深度分布（相対度数）_0, 1】df_allの'rel_freq'をX軸に設定
    x = df_all['rel_freq'][0]
    # 【特性深度分布（相対度数）_0, 1】グラフ生成
    # 「50%」「std_ddof=1」の数値がによってBAR・線色を変更する
    if baratsuki >= baratsuki_l:
        s_color = 'orange'
    else:
        if baratsuki <= baratsuki_h:
            s_color = 'g'
        else:
            s_color = 'grey'
    axes[0, 1].plot(x, y, s_color, linewidth=3)
    axes[0, 1].set_title('特性深度分布（相対度数 %）', size=10)
    axes[0, 1].set_xlabel('相対度数（％）', size=8)
    axes[0, 1].set_ylabel('深さ（㎝）', size=8)
    axes[0, 1].set_xlim(0, 1)
    axes[0, 1].set_ylim(60, 1)
    axes[0, 1].set_yticks([])
    axes[0, 1].xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    axes[0, 1].axhline(sakudoshin3, linestyle=':', color='r', lw=1.5, alpha=0.5)
    axes[0, 1].axhline(sakudoshin, linestyle='--', color='r', lw=1.5, alpha=0.5)
    axes[0, 1].axhline(sakudoshin4, linestyle=':', color='r', lw=1.5, alpha=0.5)
    axes[0, 1].axhline(10, linestyle=':', color='grey', lw=0.5)
    axes[0, 1].axhline(20, linestyle=':', color='grey', lw=0.5)
    axes[0, 1].axhline(30, linestyle=':', color='grey', lw=0.5)
    axes[0, 1].axhline(40, linestyle=':', color='grey', lw=0.5)
    axes[0, 1].axhline(50, linestyle=':', color='grey', lw=0.5)
    axes[0, 1].axvline(0.5, linestyle=':', color='grey', lw=0.5)
    axes[0, 1].minorticks_on()

    # 【土壌硬度分布グラフ_0, 3】準備-1 df_aveからX軸の設定
    x = df_ave.columns.to_list()
    del x[0: 8]
    for j in range(len(df_ave)):
        y = list(df_ave.iloc[j])
        point1 = y[6]
        point2 = str(y[7])
        name = point1 + '-' + str(point2)
        # print(name)
        del y[0: 8]
        color = line_color[point1]
        dash = line_shape[point2]
        axes[0, 2].plot(y, x, color, dash, lw=0.8, label=name)
        # axes[0, 2].legend(name, fontsize=6, labelcolor=color, loc='best')

    axes[0, 2].set_title('土壌硬度分布（測定地点別）', size=10)
    axes[0, 2].set_xlabel('硬さ（kPa）', size=8)
    axes[0, 2].set_ylabel('深さ（㎝）', size=8)
    axes[0, 2].set_xlim(0, 3000)
    axes[0, 2].set_ylim(60, 1)
    axes[0, 2].set_yticks([])
    axes[0, 2].axhline(sakudoshin, linestyle='--', color='r', lw=1.5, alpha=0.5)
    axes[0, 2].axhline(10, linestyle=':', color='grey', lw=0.5)
    axes[0, 2].axhline(20, linestyle=':', color='grey', lw=0.5)
    axes[0, 2].axhline(30, linestyle=':', color='grey', lw=0.5)
    axes[0, 2].axhline(40, linestyle=':', color='grey', lw=0.5)
    axes[0, 2].axhline(50, linestyle=':', color='grey', lw=0.5)
    axes[0, 2].axvline(1500, linestyle='--', color='grey', lw=1.0)
    # axes[0, 2].set_legend(loc="center", bbox_to_anchor=(0.5, 1.05), ncol=2)

    # 生成したグラフの保存
    filedir = 'C:/Users/minam/Desktop/soil_physical_graph/'
    filename = filedir + graph_title + '_ver1.2.jpeg'
    fig.suptitle(graph_title, fontsize=10)
    # fig.savefig(filename)
    plt.savefig(filename)
    # plt.show()


def soil_data_dataset(df_dp1, df_dp2, nojyomei, hojyomei, id):
    # 【Step-1】土壌硬度分布グラフ生成のためのデータ加工
    # 【Step-1-1】硬度分布データのデータフレーム決定・・point1=圃場内側定位置1、point2=圃場内測定位置2
    All_list = {'id': [], 'nojyomei': [], 'hojyomei': [], 'item': [], 'ymd': [], 'jiki': [],
                'point1': [], 'point2': [], '1cm': [], '2cm': [], '3cm': [], '4cm': [], '5cm': [],
                '6cm': [], '7cm': [], '8cm': [], '9cm': [], '10cm': [], '11cm': [], '12cm': [],
                '13cm': [], '14cm': [], '15cm': [], '16cm': [], '17cm': [], '18cm': [], '19cm': [],
                '20cm': [], '21cm': [], '22cm': [], '23cm': [], '24cm': [], '25cm': [], '26cm': [],
                '27cm': [], '28cm': [], '29cm': [], '30cm': [], '31cm': [], '32cm': [], '33cm': [],
                '34cm': [], '35cm': [], '36cm': [], '37cm': [], '38cm': [], '39cm': [], '40cm': [],
                '41cm': [], '42cm': [], '43cm': [], '44cm': [], '45cm': [], '46cm': [], '47cm': [],
                '48cm': [], '49cm': [], '50cm': [], '51cm': [], '52cm': [], '53cm': [], '54cm': [],
                '55cm': [], '56cm': [], '57cm': [], '58cm': [], '59cm': [], '60cm': []
                }
    # 【Step-1-2】品目・時期・測定日でエラー（2つ以上ある場合）を検知しAll_listに格納する
    item_list = df_dp2['品目'].tolist()
    item_list_count = len(set(item_list))
    isvalid = True
    if not item_list_count == 1:
        print("エラー：品目が2つ以上あります。")
        isvalid = False
    else:
        item = item_list[0]
        jiki_list = df_dp2['時期'].tolist()
        jiki_list_count = len(set(jiki_list))
        if not jiki_list_count == 1:
            print("エラー：時期が2つ以上あります。")
            isvalid = False
        else:
            jiki = jiki_list[0]
            sokuteibi = df_dp2['測定日'].tolist()
            sokuteibi_count = len(set(sokuteibi))
            if not sokuteibi_count == 1:
                print("エラー：測定日が2つ以上あります。")
                isvalid = False
            else:
                # 測定日をdatetimeに変換する
                sokuteibi2 = sokuteibi[0] + ' ' + '00:00:00'
                sokuteibi2 = datetime.datetime.strptime(sokuteibi2, '%Y.%m.%d %H:%M:%S')

                # 【Step-1-3】df_dp2に格納したデータ（文字列含む）の平均値を算出しAll_listに格納する
                df_ave = df_dp2.groupby(['圃場内位置', '圃場内位置2']).mean()
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
                tuika_list = [id, nojyomei, hojyomei, item, sokuteibi2, jiki]
                tuika_header = ['id', 'nojyomei', 'hojyomei', 'item', 'ymd', 'jiki']
                df_ave.insert(loc=0, column='point2', value=point2_list)
                df_ave.insert(loc=0, column='point1', value=point1_list)
                for i, (tuika, tuikah) in enumerate(zip(tuika_list, tuika_header)):
                    df_ave.insert(loc=i, column=tuikah, value=tuika)
                df_ave.reset_index(inplace=True, drop=True)
                # df_ave.to_csv('df_ave.csv', encoding='SHIFT-JIS', index=False)


                # 【Step-2】特性深度分布グラフ生成のためのデータ加工
                # 【Step-2-1】取り込むリストのDBフォーマットの決定・・All_list2
                All_list2 = {'id': [], 'nojyomei': [], 'hojyomei': [], 'item': [], 'ymd': [],
                             'jiki': [], 'class_index': [], 'class_value': [], 'freq': [],
                             'rel_freq': [], 'cum_freq': [], 'rel_cum_freq': [], 'count': [],
                             'mean': [], 'std': [], 'min': [], '25%': [], '50%': [], '75%': [],
                             'max': [], 'skew': [], 'kurt': [], 'var_ddof=1': [], 'std_ddof=1': []
                             }
                # 【Step-2-2】df_dpからAll_listに基本情報（ID・農場名・圃場名・品目・測定日・時期）を格納
                # ID、農場名と圃場名をAll_list2に格納
                All_list2['id'].append(id)
                All_list2['nojyomei'].append(nojyomei)
                All_list2['hojyomei'].append(hojyomei)
                # 品目・測定日・時期はエラー（欠損値を含む複数）検知を実施し、All_list2に格納する
                item_list = df_dp1['品目'].tolist()
                item_list_count = len(set(item_list))
                isvalid = True
                if not item_list_count == 1:
                    print("エラー：品目が2つ以上あります。")
                    isvalid = False
                else:
                    All_list2['item'].append(list(set(item_list))[0])
                    jiki_list = df_dp1['時期'].tolist()
                    jiki_list_count = len(set(jiki_list))
                    isvalid = True
                    if not jiki_list_count == 1:
                        print("エラー：時期が2つ以上あります。")
                        isvalid = False
                    else:
                        All_list2['jiki'].append(list(set(jiki_list))[0])
                        sokuteibi = df_dp1['測定日'].tolist()
                        sokuteibi_count = len(set(sokuteibi))
                        isvalid = True
                        if not sokuteibi_count == 1:
                            print("エラー：測定日が2つ以上あります。")
                            isvalid = False
                        else:
                            sokuteibi2 = sokuteibi[0]
                            All_list2['ymd'].append(sokuteibi2)
                            # 【Step-2-3] ヒストグラムの計算値をAll_listに格納
                            dataset1 = df_dp1['xC']
                            bins = np.linspace(0, 60, 13)
                            freq = dataset1.value_counts(bins=bins, sort=False)
                            All_list2['freq'].append(freq)
                            class_value = (bins[:-1] + bins[1:]) / 2  # 階級値
                            All_list2['class_value'].append(class_value)
                            rel_freq = freq / dataset1.count()  # 相対度数
                            All_list2['rel_freq'].append(rel_freq)
                            cum_freq = freq.cumsum()  # 累積度数
                            All_list2['cum_freq'].append(cum_freq)
                            rel_cum_freq = rel_freq.cumsum()  # 相対累積度数
                            All_list2['rel_cum_freq'].append(rel_cum_freq)
                            class_index = freq.index  # 階層
                            All_list2['class_index'].append(class_index)
                            # 統計量の計算値をAll_Listに格納
                            # describeメソッドで個数～最大値を一括で計算
                            stats = dataset1.describe()
                            # print(stats)
                            stats_count = pd.Series(data=stats)['count']
                            All_list2['count'].append(stats_count)  # 個数
                            stats_mean = pd.Series(data=stats)['mean']
                            All_list2['mean'].append(stats_mean)  # 平均値
                            stats_std = pd.Series(data=stats)['std']
                            All_list2['std'].append(stats_std)  # 標準偏差（標本分数）
                            stats_min = pd.Series(data=stats)['min']
                            All_list2['min'].append(stats_min)  # 最小値
                            stats_25 = pd.Series(data=stats)['25%']
                            All_list2['25%'].append(stats_25)  # 四分位数（25%）
                            stats_50 = pd.Series(data=stats)['50%']
                            All_list2['50%'].append(stats_50)  # 四分位数（50%）
                            stats_75 = pd.Series(data=stats)['75%']
                            All_list2['75%'].append(stats_75)  # 四分位数（75%）
                            stats_max = pd.Series(data=stats)['max']
                            All_list2['max'].append(stats_max)  # 最大値
                            All_list2['skew'].append(dataset1.skew())  # 歪度
                            All_list2['kurt'].append(dataset1.kurt())  # 尖度
                            All_list2['var_ddof=1'].append(dataset1.var(ddof=1))  # 分散（不偏分散）
                            All_list2['std_ddof=1'].append(dataset1.std(ddof=1))  # 標準偏差（不偏分散）
                df_all = pd.DataFrame(All_list2)
                # 特性深度グラフのY軸データ（共通）をyに代入
                y = df_all['class_value'][0]
                filedir = 'C:/Users/minam/Desktop/tokusei_csv/'
                save_name1 = filedir + '土壌硬度分布_' + id + '_' + nojyomei + '_' + hojyomei + '_' + sokuteibi2
                save_name2 = filedir + '特性深度分布_' + id + '_' + nojyomei + '_' + hojyomei + '_' + sokuteibi2
                # 特性深度分布の計算結果（df_all）と土壌硬度分布の計算結果（df_ave）をcsv保存
                df_ave.to_csv(save_name1 + '.csv', encoding='SHIFT-JIS', index=False)
                df_all.to_csv(save_name2 + '.csv', encoding='SHIFT-JIS', index=False)
                # 事前準備1：測定位置ごとの色・線のプロパティを決める
                line_color = {'A': 'b', 'B': 'orange', 'C': 'r'}
                line_shape = {'1': '-', '2': ':', '3': '-.'}
                # 事前準備2：グラフタイトルを設定
                # graph_titles = df_all[['nojyomei', 'hojyomei', 'item', 'ymd', 'jiki']].values
                graph_titles = df_all[['id', 'hojyomei', 'item', 'ymd', 'jiki']].values
                graph_titles2 = graph_titles[0]
                graph_title = '土壌物理性診断_' + '_'.join(graph_titles2)
                graphset_1x3(df_all, df_ave, line_color, line_shape, y, graph_title)
                # time.sleep(1.5)


if __name__ == '__main__':
    # ☆所定データの読み込み・・【展開】特定フォルダから複数ファイルを同時に読み込む処理
    filedir = 'C:/Users/minam/Desktop/tokusei_precal/'
    files = glob.glob(filedir + '/**/*.csv')
    # 読み込んだファイルを「農場名」「圃場名」「圃場内測定位置」「圃場内測定位置2」で分類し、df2に格納
    for file in files:
        print(file)
        df = pd.read_csv(file, encoding='Shift-JIS', header=0)

        # Step-1：農場名での分類
        nojyomei_list = df['農場名'].tolist()
        nojyomei_list = list(set(nojyomei_list))
        # print(nojyomei_list)

        # Step-2：圃場名でのデータ抽出と所定DATAFRAMEへの格納
        for nojyomei in nojyomei_list:
            df1 = df[df['農場名'] == nojyomei]
            hojyomei_list = df1['圃場名'].tolist()
            hojyomei_list = list(set(hojyomei_list))
            for hojyomei in hojyomei_list:
                df2 = df1[df1['圃場名'] == hojyomei]
                id_list = df2['ID'].tolist()
                id_list = list(set(id_list))
                point1_list = df2['圃場内位置'].tolist()
                point2_list = df2['圃場内位置2'].tolist()
                point1_list = list(set(point1_list))
                point2_list = list(set(point2_list))

                # 測定位置情報のエラー検知
                isvalid = True
                if not len(point1_list) == len(point2_list):
                    print("測定位置情報が一致しません。処理を中断しました")
                    isvalid = False
                else:
                    # IDが複数あるエラー検知
                    if not len(id_list) == 1:
                        print("1圃場にIDが複数あります。処理を中断しました")
                        isvalid = False
                    else:
                        # 【Step-3】dfから不必要な列を削除する
                        df_dp2 = df2.drop(df2.columns[range(73, 111)], axis=1)
                        df_dp2 = df_dp2.drop(df_dp2.columns[range(9, 13)], axis=1)
                        df_dp2 = df_dp2.drop(df_dp2.columns[range(0, 1)], axis=1)
                        df_dp2.reset_index(inplace=True, drop=True)
                        id = df_dp2.iat[0, 0]
                        nojyomei = df_dp2.iat[0, 1]
                        hojyomei = df_dp2.iat[0, 3]
                        # 【Step-4】df2から不必要な列を削除する・・散布図生成の共通処理
                        df_dp1 = df2.drop(df2.columns[range(9, 103)], axis=1)
                        df_dp1 = df_dp1.drop(df_dp1.columns[range(0, 1)], axis=1)
                        df_dp1.reset_index(inplace=True, drop=True)
                        soil_data_dataset(df_dp1, df_dp2, nojyomei, hojyomei, id)  # グラフ化のためのデータ加工関数へ
