# Step-1 soil_chemical_propertiesフォルダにある測定データ（xlsx）を読み込む
# Step-2 土壌化学性分析データを抽出し、グラフ表示用のDATAFRAMEに取り込む
# Step-3 グラフ化する
import pandas as pd
import numpy as np
import datetime
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

def graphset_N(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '窒素関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_N = df2.iloc[[5, 17, 18, 26, 27]]
    # データを換算するための基準値設定
    dataset_N = {'EC(mS/cm)': 0.2, 'NH4-N(mg/100g)': 1.5, 'NO3-N(mg/100g)': 3.5, '無機態窒素': 15, 'NH4/無機態窒素': 0.6}
    # df_Nの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_N):
        x = df_N[j] / dataset_N[j]
        df_N[j] = x
    df_N2 = pd.DataFrame(df_N)
    # print(df_N)
    # 窒素に関連する土壌化学性項目グラフを生成・保存
    fig = go.Figure()
    for n, m in df_N2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー
        x = m.values
        if x >= 1:
            color = 'red'
        else:
            color = 'grey'
        y = [n]
        s1 = df_N[n]
        print(s1)
        print('==')
        s2 = dataset_N[n]
        print(s2)
        print('===')
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


def graphset_P(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = 'リン酸関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_P = df2.iloc[[15, 16]]
    # データを換算するための基準値設定
    dataset_P = {'P2O5(mg/100g)': 50, 'リン吸(mg/100g)': 700}
    # df_Pの数値を基準値で除算してパーセントに変換
    for k, j in enumerate(dataset_P):
        x = df_P[j] / dataset_P[j]
        df_P[j] = x
    df_P2 = pd.DataFrame(df_P)
    print(df_P2)
    # リン酸に関連する土壌化学性項目グラフを生成・保存
    fig = plt.figure()
    ax = fig.add_subplot()
    for n, m in df_P2.iterrows():
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー
        x = m.values
        if x >= 1:
            color = 'red'
        else:
            color = 'grey'
        y = [n]
        print(y)
        print(color)
        ax.barh(y, x, color=color, height=0.5, align='center', label=hojyomei)
        ax.set_title(title, size=11)
        ax.set_xlabel('飽和度（基準値100％）', size=11)
        ax.set_ylabel('測定項目', size=11)
        ax.set_xlim(0, 3)
        # ax.grid(axis='x', linestyle='dotted', color='r')
        ax.set_yticks([])
        plt.text(x/len(df_P2), y, "({} : {})".format(y, x), ha='center', color='white', size=11)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        # handler1, label1 = ax1.get_legend_handles_labels()
        # ax1.legend(handler1, label1, borderaxespad=0, loc='center right')
    ax.axvline(1, linestyle='dotted', color='red')
    ax.invert_yaxis()
    fig.savefig('リン酸関連グラフ_' + title + '.jpeg')


def graphset_Enki(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '塩基類関連_' + '_'.join(graph_title)


def graphset_Soilpotential(df2, graph_title, hojyomei):
    # グラフのタイトルを生成する
    title = '土壌ポテンシャル関連_' + '_'.join(graph_title)


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
                # graphset_N(df2, graph_title, hojyomei)
                graphset_P(df2, graph_title, hojyomei)
                # graphset_Enki(df2, graph_title, hojyomei)
                # graphset_Soilpotential(df2, graph_title, hojyomei)

