# Step-1 soil_chemical_propertiesフォルダにある測定データ（xlsx）を読み込む
# Step-2 土壌化学性分析データを抽出し、グラフ表示用のDATAFRAMEに取り込む
# Step-3 グラフ化する
import pandas as pd
import glob
import os
import pprint
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt

# 【下準備】日本語対応
plt.rcParams['font.family'] = 'Meiryo'
# 【グラフ下準備】グラフサイズを統一
plt.figure(figsize=[5, 5])

def graphset_n(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '窒素関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_n = df2.iloc[[5, 17, 18, 26, 27]]
    # データを換算するための基準値設定
    dataset_n = {'EC(mS/cm)': 0.2, 'NH4-N(mg/100g)': 1.5, 'NO3-N(mg/100g)': 3.5, '無機態窒素': 15,
                 'NH4/無機態窒素': 0.6
                 }
    # df_nの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_n):
        x = df_n[j] / dataset_n[j]
        df_n[j] = x
    df_n2 = pd.DataFrame(df_n)
    # 窒素に関連する土壌化学性項目グラフを生成・保存
    fig = go.Figure()
    for n, m in df_n2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー
        x = m.values
        if x >= 1:
            color = 'red'
        else:
            color = 'grey'
        y = [n]
        s1 = df_n[n]
        s2 = dataset_n[n]
        # 項目毎に計算値を系列追加
        fig.add_trace(go.Bar(y=y,
                             x=x,
                             name=hojyomei,
                             width=0.7,
                             marker_color=color,
                             showlegend=False,
                             # hovertext='測定値:%{s1}, 基準値:%{s2}',
                             orientation='h')
                      )
    fig.update_layout(title=dict(text=title,
                                 font=dict(size=11, color='black'),
                                 xref='paper',
                                 x=0.01,
                                 y=0.85,
                                 xanchor='left'
                                 ),
                      yaxis=dict(title='測定項目'),
                      xaxis=dict(title='飽和度（基準値100％）', range=(0, 3), tickformat='%'),
                      width=500,
                      height=500,
                      plot_bgcolor='white'
                      )
    fig.layout.xaxis.tickformat = ',.0%'
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', color='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black', color='black')
    fig.update_layout(hovermode='closest')
    # filedir = 'C:/Users/minam/Desktop/soil_chemical_graph/'
    # fig_name = 'soil_chemical_graph1_' + hojyomei + '_' + sokuteibi + '.jpeg'
    # fig_name2 = filedir + fig_name
    # print(fig_name2)
    # # fig.write_image(fig_name2)
    fig.show()


def graphset_n2(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '窒素関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_n = df2.iloc[[5, 17, 18, 26, 27]]
    # データを換算するための基準値設定
    dataset_nh = {'EC(mS/cm)': 0.2, 'NH4-N(mg/100g)': 1.5, 'NO3-N(mg/100g)': 3.5, '無機態窒素': 15, 'NH4/無機態窒素': 0.6}
    dataset_nl = {'EC(mS/cm)': 0.05, 'NH4-N(mg/100g)': 0.2, 'NO3-N(mg/100g)': 0.7, '無機態窒素': 4, 'NH4/無機態窒素': 0.1}
    # df_nの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_nh):
        x = df_n[j] / dataset_nh[j]
        df_n[j] = x
    df_n2 = pd.DataFrame(df_n)
    # 窒素に関連する土壌化学性項目グラフを生成・保存
    fig = plt.figure()
    ax = fig.add_subplot()
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
        ax.barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        ax.set_title(title, size=11)
        ax.set_xlabel('飽和度（基準値100％）', size=11)
        ax.set_ylabel('測定項目', size=11)
        ax.set_xlim(0, 3)
        ax.set_yticks([])
        plt.text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=11)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.axvline(1, linestyle='dotted', color='red')
    ax.invert_yaxis()
    filedir = 'C:/Users/minam/Desktop/soil_chemical_graph/'
    filename = filedir + '窒素関連グラフ_' + title + '.jpeg'
    fig.savefig(filename)
    # fig.savefig('窒素関連グラフ_' + title + '.jpeg')


def graphset_p(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = 'リン酸関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_p = df2.iloc[[15, 16]]
    # データを換算するための基準値設定
    dataset_ph = {'P2O5(mg/100g)': 50, 'リン吸(mg/100g)': 700}
    dataset_pl = {'P2O5(mg/100g)': 10, 'リン吸(mg/100g)': 2000}
    # df_pの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_ph):
        x = df_p[j] / dataset_ph[j]
        df_p[j] = x
    df_p2 = pd.DataFrame(df_p)
    # リン酸に関連する土壌化学性項目グラフを生成・保存
    fig = plt.figure()
    ax = fig.add_subplot()
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
        ax.barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        ax.set_title(title, size=11)
        ax.set_xlabel('飽和度（基準値100％）', size=11)
        ax.set_ylabel('測定項目', size=11)
        ax.set_xlim(0, 3)
        ax.set_yticks([])
        plt.text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=11)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.axvline(1, linestyle='dotted', color='red')
    ax.invert_yaxis()
    filedir = 'C:/Users/minam/Desktop/soil_chemical_graph/'
    filename = filedir + 'リン酸関連グラフ_' + title + '.jpeg'
    fig.savefig(filename)
    # fig.savefig('リン酸関連グラフ_' + title + '.jpeg')


def graphset_enki(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '塩基類関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_enki = df2.iloc[[6, 8, 9, 10, 14, 21, 22]]
    # データを換算するための基準値設定
    dataset_enkih = {'ｐH': 6.5, 'CaO(mg/100g)': 400, 'MgO(mg/100g)': 70, 'K2O(mg/100g)': 40,
                    '塩基飽和度(%)': 0.8, 'CaO/MgO': 8, 'MgO/K₂O': 6
                     }
    dataset_enkil = {'ｐH': 6, 'CaO(mg/100g)': 200, 'MgO(mg/100g)': 25, 'K2O(mg/100g)': 15,
                     '塩基飽和度(%)': 0.5, 'CaO/MgO': 5, 'MgO/K₂O': 3
                     }
    # df_enkiの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_enkih):
        x = df_enki[j] / dataset_enkih[j]
        df_enki[j] = x
    df_enki2 = pd.DataFrame(df_enki)
    # 塩基類に関連する土壌化学性項目グラフを生成・保存
    fig = plt.figure()
    ax = fig.add_subplot()
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
        ax.barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        ax.set_title(title, size=11)
        ax.set_xlabel('飽和度（基準値100％）', size=11)
        ax.set_ylabel('測定項目', size=11)
        ax.set_xlim(0, 3)
        ax.set_yticks([])
        plt.text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=11)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.axvline(1, linestyle='dotted', color='red')
    ax.invert_yaxis()
    filedir = 'C:/Users/minam/Desktop/soil_chemical_graph/'
    filename = filedir + '塩基類関連グラフ_' + title + '.jpeg'
    fig.savefig(filename)
    # fig.savefig('塩基類関連グラフ_' + title + '.jpeg')


def graphset_soilpotential(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '土壌ポテンシャル関連_' + '_'.join(graph_title)
    df_soil = df2.iloc[[7, 19, 20]]
    # データを換算するための基準値設定
    dataset_soilh = {'CEC(meq/100g)': 40, '腐植(%)': 0.08, '仮比重': 1}
    dataset_soill = {'CEC(meq/100g)': 12, '腐植(%)': 0.03, '仮比重': 0.6}
    # df_soilの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_soilh):
        x = df_soil[j] / dataset_soilh[j]
        df_soil[j] = x
    df_soil2 = pd.DataFrame(df_soil)
    # 土壌ポテンシャルに関連する土壌化学性項目グラフを生成・保存
    fig = plt.figure()
    ax = fig.add_subplot()
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
        ax.barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        ax.set_title(title, size=11)
        ax.set_xlabel('飽和度（基準値100％）', size=11)
        ax.set_ylabel('測定項目', size=11)
        ax.set_xlim(0, 3)
        ax.set_yticks([])
        plt.text(x_text, y, "{}".format(y), ha='left', va='center', color=t_color, size=11)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.axvline(1, linestyle='dotted', color='red')
    ax.invert_yaxis()
    filedir = 'C:/Users/minam/Desktop/soil_chemical_graph/'
    filename = filedir + '土壌ポテンシャル関連グラフ_' + title + '.jpeg'
    fig.savefig(filename)
    # fig.savefig('土壌ポテンシャル関連グラフ_' + title + '.jpeg')


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
                graph_title = df2[['生産者名', '圃場名', '品目', '作型', '採土日']].values
                hojyomei = df2['圃場名']
                print(graph_title, hojyomei)
                # graphset_n(df2, graph_title, hojyomei)
                graphset_n2(df2, graph_title, hojyomei)
                graphset_p(df2, graph_title, hojyomei)
                graphset_enki(df2, graph_title, hojyomei)
                graphset_soilpotential(df2, graph_title, hojyomei)

