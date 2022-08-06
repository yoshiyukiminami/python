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

def graphset_N(df2):
    # print(df2)
    # グラフのタイトルを生成する
    graph_title = df2[['生産者名', '圃場名', '品目', '作型', '採土日']].values
    title = '窒素関連_' + '_'.join(graph_title)
    # df2からグラフに必要な項目のみ分離
    df_N = df2.iloc[[5, 17, 18, 26, 27]]
    # データを換算するための基準値設定
    dataset_N = {'EC(mS/cm)': 0.2, 'NH4-N(mg/100g)': 1.5, 'NO3-N(mg/100g)': 3.5, '無機態窒素': 15, 'NH4/無機態窒素': 0.6}
    # df_Nの数値を基準値で除算してパーセントに変換
    for k in dataset_N:
        x = df_N[k] / dataset_N[k]
        df_N[k] = x
    print(df_N)
    # 窒素に関連する土壌化学性項目グラフを生成・保存
    fig = go.Figure()
    for n, m in enumerate(df_N):
        # 計算値が100％以上の時にBAR色を赤、100％未満はグレー
        if m >= 1:
            color = 'red'
        else:
            color = 'grey'
        print(color)
        print(n, m)
        y = df_N.iloc[n]
        print(y, type(y))
        # 項目毎に計算値を系列追加
        fig.add_trace(go.Bar(y=y,
                             x=np.array(m),
                             name=df_N.iloc[n],
                             width=0.1,
                             marker_color=color,
                             showlegend=False,
                             # hovertext='飽和度:%{x}, 測定項目:%{k}',
                             orientation='h')
                      )
    fig.update_layout(title=dict(text=title,
                                 font=dict(size=11, color='black'),
                                 xref='paper',
                                 x=0.01,
                                 y=0.85,
                                 xanchor='left'
                                 ),
                      # yaxis=dict(title='測定項目', range=(0.5, koumoku+0.5)),
                      yaxis=dict(title='測定項目'),
                      xaxis=dict(title='飽和度（基準値100％）', range=(0, 2), tickformat='%'),
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

def graphset_enki(df2):
    print(df2)


def graphset_soilpotential(df2):
    print(df2)


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
                graphset_N(df2)
                # graphset_enki(df2)
                # graphset_soilpotential(df2)

