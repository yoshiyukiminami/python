# Step-1 soil_chemical_propertiesフォルダにある測定データ（xlsx）を読み込む
# Step-2 土壌化学性分析データを抽出し、グラフ表示用のDATAFRAMEに取り込む
# Step-3 分析データをグラフ化する
import pandas as pd
import glob
import os
import pprint
import matplotlib
import matplotlib.pyplot as plt

# 【下準備】日本語対応
plt.rcParams['font.family'] = 'Meiryo'
# 【グラフ下準備】グラフサイズを統一
plt.figure(figsize=[8, 8])

def graphset_2x2(df2, graph_title, hojyomei):
    # 1つのfigに4つのaxesを行2×列2で描画
    fig, axes = plt.subplots(2, 2, tight_layout=True, squeeze=False, sharex='col')

    # 【窒素関連_0, 0】準備-1 df2からグラフに必要な項目のみ分離
    df_n = df2.iloc[[5, 17, 18, 26, 27]]
    # 【窒素関連_0, 0】準備-2 データを換算するための基準値設定
    dataset_nh = {'EC(mS/cm)': 0.2, 'NH4-N(mg/100g)': 1.5, 'NO3-N(mg/100g)': 3.5, '無機態窒素': 15, 'NH4/無機態窒素': 0.6}
    dataset_nl = {'EC(mS/cm)': 0.05, 'NH4-N(mg/100g)': 0.2, 'NO3-N(mg/100g)': 0.7, '無機態窒素': 4, 'NH4/無機態窒素': 0.1}
    # 【窒素関連_0, 0】準備-3 df_nの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_nh):
        x = df_n[j] / dataset_nh[j]
        df_n[j] = x
    df_n2 = pd.DataFrame(df_n)

    # 窒素に関連する土壌化学性項目グラフを生成[0, 0]
    for n, m in df_n2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー、LOW基準以下はブルー
        x = m.values
        L_level = (1 * dataset_nl[n]) / dataset_nh[n]
        if x >= 1:
            color = 'red'
            if x >= 2:
                x_text = 1
                t_color = 'yellow'
            else:
                x_text = x
                t_color = 'red'
        else:
            x_text = x
            if x <= L_level:
                color = 'blue'
                t_color = 'blue'
            else:
                color = 'grey'
                t_color = 'black'
        y = [n]
        axes[0, 0].barh(y, x, color=color, height=0.5, align='center')
        axes[0, 0].set_title('窒素関連', size=11)
        # axes[0, 0].set_xlabel('飽和度（基準値100％）', size=8)
        axes[0, 0].set_ylabel('測定項目', size=8)
        axes[0, 0].set_xlim(0, 3)
        axes[0, 0].set_yticks([])
        # axes[0, 0].set_xticklabels(x, fontsize=8)
        axes[0, 0].text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=8)
        axes[0, 0].xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        axes[0, 0].axvline(1, linestyle='dotted', color='orange', lw=0.8)
        axes[0, 0].axvline(2, linestyle='dotted', color='red', lw=0.8)
        axes[0, 0].invert_yaxis()

    # 【リン酸関連_1, 0】準備-1 df2からグラフに必要な項目のみ分離
    df_p = df2.iloc[[15, 16]]
    # 【リン酸関連_1, 0】準備-2 データを換算するための基準値設定
    dataset_ph = {'P2O5(mg/100g)': 50, 'リン吸(mg/100g)': 700}
    dataset_pl = {'P2O5(mg/100g)': 10, 'リン吸(mg/100g)': 2000}
    # 【リン酸関連_1, 0】準備-3 df_pの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_ph):
        x = df_p[j] / dataset_ph[j]
        df_p[j] = x
    df_p2 = pd.DataFrame(df_p)
    # リン酸に関連する土壌化学性項目グラフを生成
    for n, m in df_p2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー、LOW基準以下はブルー
        x = m.values
        L_level = (1 * dataset_pl[n]) / dataset_ph[n]
        if x >= 1:
            color = 'red'
            if x >= 2:
                x_text = 1
                t_color = 'yellow'
            else:
                x_text = x
                t_color = 'red'
        else:
            x_text = x
            if x <= L_level:
                color = 'blue'
                t_color = 'blue'
            else:
                color = 'grey'
                t_color = 'black'
        y = [n]
        axes[1, 0].barh(y, x, color=color, height=0.5, align='center')
        axes[1, 0].set_title('リン酸関連', size=11)
        axes[1, 0].set_xlabel('飽和度（基準値100％）', size=8)
        axes[1, 0].set_ylabel('測定項目', size=8)
        axes[1, 0].set_xlim(0, 3)
        axes[1, 0].set_yticks([])
        axes[1, 0].set_xticklabels(x, fontsize=8)
        axes[1, 0].text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=8)
        axes[1, 0].xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        axes[1, 0].axvline(1, linestyle='dotted', color='orange', lw=0.8)
        axes[1, 0].axvline(2, linestyle='dotted', color='red', lw=0.8)
        axes[1, 0].invert_yaxis()

    # 【塩基類関連_0, 1】準備-1 df2からグラフに必要な項目のみ分離
    df_enki = df2.iloc[[6, 8, 9, 10, 14, 21, 22]]
    # 【塩基類関連_0, 1】準備-2 データを換算するための基準値設定
    dataset_enkih = {'ｐH': 6.5, 'CaO(mg/100g)': 400, 'MgO(mg/100g)': 70, 'K2O(mg/100g)': 40,
                    '塩基飽和度(%)': 0.8, 'CaO/MgO': 8, 'MgO/K₂O': 6
                     }
    dataset_enkil = {'ｐH': 6, 'CaO(mg/100g)': 200, 'MgO(mg/100g)': 25, 'K2O(mg/100g)': 15,
                     '塩基飽和度(%)': 0.5, 'CaO/MgO': 5, 'MgO/K₂O': 3
                     }
    # 【塩基類関連_0, 1】準備-3 df_enkiの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_enkih):
        x = df_enki[j] / dataset_enkih[j]
        df_enki[j] = x
    df_enki2 = pd.DataFrame(df_enki)
    # 塩基類に関連する土壌化学性項目グラフを生成
    for n, m in df_enki2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー、LOW基準以下はブルー
        x = m.values
        L_level = (1 * dataset_enkil[n]) / dataset_enkih[n]
        if x >= 1:
            color = 'red'
            if x >= 2:
                x_text = 1
                t_color = 'yellow'
            else:
                x_text = x
                t_color = 'red'
        else:
            x_text = x
            if x <= L_level:
                color = 'blue'
                t_color = 'blue'
            else:
                color = 'grey'
                t_color = 'black'
        y = [n]
        axes[0, 1].barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        axes[0, 1].set_title('塩基類関連', size=11)
        # axes[0, 1].set_xlabel('飽和度（基準値100％）', size=8)
        axes[0, 1].set_ylabel('測定項目', size=8)
        axes[0, 1].set_xlim(0, 3)
        axes[0, 1].set_yticks([])
        # axes[0, 1].set_xticklabels(x, fontsize=8)
        axes[0, 1].text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=8)
        axes[0, 1].xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        axes[0, 1].axvline(1, linestyle='dotted', color='orange', lw=0.8)
        axes[0, 1].axvline(2, linestyle='dotted', color='red', lw=0.8)
        axes[0, 1].invert_yaxis()

    # 【土壌ポテンシャル関連_1, 1】準備-1 df2からグラフに必要な項目のみ分離
    df_soil = df2.iloc[[7, 19, 20]]
    # 【土壌ポテンシャル関連_1, 1】準備-2 データを換算するための基準値設定
    dataset_soilh = {'CEC(meq/100g)': 40, '腐植(%)': 0.08, '仮比重': 1}
    dataset_soill = {'CEC(meq/100g)': 12, '腐植(%)': 0.03, '仮比重': 0.6}
    # 【土壌ポテンシャル関連_1, 1】準備-3 df_soilの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_soilh):
        x = df_soil[j] / dataset_soilh[j]
        df_soil[j] = x
    df_soil2 = pd.DataFrame(df_soil)
    # 土壌ポテンシャルに関連する土壌化学性項目グラフを生成
    for n, m in df_soil2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー、LOW基準以下はブルー
        x = m.values
        L_level = (1 * dataset_soill[n]) / dataset_soilh[n]
        if x >= 1:
            color = 'red'
            if x >= 2:
                x_text = 1
                t_color = 'yellow'
            else:
                x_text = x
                t_color = 'red'
        else:
            x_text = x
            if x <= L_level:
                color = 'blue'
                t_color = 'blue'
            else:
                color = 'grey'
                t_color = 'black'
        y = [n]
        axes[1, 1].barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        axes[1, 1].set_title('土壌ポテンシャル関連', size=11)
        axes[1, 1].set_xlabel('飽和度（基準値100％）', size=8)
        axes[1, 1].set_ylabel('測定項目', size=8)
        axes[1, 1].set_xlim(0, 3)
        axes[1, 1].set_yticks([])
        axes[1, 1].set_xticklabels(x, fontsize=8)
        axes[1, 1].text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=8)
        axes[1, 1].xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        axes[1, 1].axvline(1, linestyle='dotted', color='orange', lw=0.8)
        axes[1, 1].axvline(2, linestyle='dotted', color='red', lw=0.8)
        axes[1, 1].invert_yaxis()

    # 生成したグラフの保存
    filedir = 'C:/Users/minam/Desktop/soil_chemical_graph/'
    filename = filedir + graph_title + '.jpeg'
    fig.suptitle(graph_title)
    fig.savefig(filename)
    # plt.savefig(filename)
    plt.show()


if __name__ == '__main__':
    # Step-1 フォルダにある測定データ（xlsx）を読み込む
    # 読み込むデータを特定するfolder-pathをfiledirに設定する
    filedir = 'C:/Users/minam/Desktop/soil_chemical_properties/'
    # フォルダー内にあるフォルダー名をfolderlist、ファイル名をfilesに所得する
    folderlist = os.listdir(filedir)
    print(folderlist)
    files = glob.glob(filedir + '/**/*.xlsx', recursive=True)
    pprint.pprint(files)

    # フォルダにある測定データ（.xlsx）を読み込む
    for file in files:
        df = pd.read_excel(file, sheet_name='土壌化学性データ')
        df = df.drop(['ID', '出荷団体名', '検体番号', '採土法', '採土者', '分析依頼日', '報告日', '分析機関', '分析番号'], axis=1)
        # 欠損値の判定
        isvalid = True
        for i in range(len(df)):
            if df.loc[i].isnull().any():
                print("欠損値のある行が含まれています")
                isvalid = False
            else:
                print("データは正常です")
                df2 = df.loc[i]
                graph_titles = df2[['生産者名', '圃場名', '品目', '作型', '採土日']].values
                graph_title = '土壌化学性診断_' + '_'.join(graph_titles)
                hojyomei = df2['圃場名']
                graphset_2x2(df2, graph_title, hojyomei)
                # graphset_n2(df2, graph_title, hojyomei)
                # graphset_p(df2, graph_title, hojyomei)
                # graphset_enki(df2, graph_title, hojyomei)
                # graphset_soilpotential(df2, graph_title, hojyomei)

