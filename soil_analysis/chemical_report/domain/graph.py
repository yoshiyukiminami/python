import matplotlib.pyplot as plt
import base64
from io import BytesIO


def output_graph():
    """
    プロットしたグラフを画像データとして出力するための関数
    :return:
    """
    buffer = BytesIO()                  # バイナリI/O(画像や音声データを取り扱う際に利用)
    plt.savefig(buffer, format="png")   # png形式の画像データを取り扱う
    buffer.seek(0)                      # ストリーム先頭のoffset byteに変更
    img = buffer.getvalue()             # バッファの全内容を含むbytes
    graph = base64.b64encode(img)       # 画像ファイルをbase64でエンコード
    graph = graph.decode("utf-8")       # デコードして文字列から画像に変換
    buffer.close()

    return graph


def plot_graph(title, x, y):
    """
    グラフをプロットするための関数
    :param title:
    :param x:
    :param y:
    :return:
    """
    plt.rcParams["font.family"] = "Meiryo"
    plt.switch_backend("AGG")       # スクリプトを出力させない
    plt.figure(figsize=(10, 5))     # グラフサイズ
    plt.barh(x, y)                  # グラフ作成
    plt.xticks(rotation=45)         # X軸値を45度傾けて表示
    plt.title(title)                # グラフタイトル
    graph = output_graph()          # グラフプロット

    return graph
