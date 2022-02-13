import datetime
import time

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas as pd

# place_codeA = [14, 21, 23, 31, 32, 33, 35, 34, 36, 54, 56, 55, 48, 41, 57, 42, 43, 40, 52, 51, 49,
#                45, 53, 50, 46, 68,
#                69, 61, 60, 67, 66, 63, 65, 64, 73, 72, 74, 71, 81, 82, 85, 83, 84, 86, 88, 87]
# place_codeB = [47412, 47423, 47430, 47575, 47582, 47584, 47588, 47590, 47595, 47604, 47605, 47607,
#                47610, 47615, 47616,
#                47624, 47626, 47629, 47632, 47636, 47638, 47648, 47651, 47656, 47670, 47741, 47746,
#                47759, 47761, 47765,
#                47768, 47770, 47777, 47780, 47887, 47891, 47893, 47895, 47762, 47807, 47813, 47815,
#                47817, 47819, 47827,
#                47830]
place_codeA = [50]
place_codeB = [1335]
# place_name = ["札幌", "室蘭", "函館", "青森", "秋田", "盛岡", "山形", "仙台", "福島", "新潟", "金沢", "富山", "長野", "宇都宮",
#               "福井", "前橋", "熊谷",
#               "水戸", "岐阜", "名古屋", "甲府", "銚子", "津", "静岡", "横浜", "松江", "鳥取", "京都", "彦根", "広島", "岡山",
#               "神戸", "和歌山", "奈良",
#               "松山", "高松", "高知", "徳島", "下関", "福岡", "佐賀", "大分", "長崎", "熊本", "鹿児島", "宮崎"]
place_name = ["菊川牧之原"]

# URLで年と月ごとの設定ができるので%sで指定した英数字を埋め込めるようにします。
base_url = "https://www.data.jma.go.jp/obd/stats/etrn/view/daily_a1.php?" \
           "prec_no=%s&block_no=%s&year=%s&month=%s&day=1&view=p1"


def str2float(_str) -> float:
    """
    取ったデータをfloat型に変えるやつ。(データが取れなかったとき気象庁は"/"を埋め込んでいるから0に変える)
    @param _str:
    @return:
    """
    try:
        return float(_str)
    except ValueError:
        return 0.0


if __name__ == "__main__":
    # 都市を網羅します
    All_list = {
        'ymd': [],
        'pref_no': [],
        'chiku_no': [],
        'kousuiryo': [],
        'kion_ave': [],
        'fuusoku': [],
        'nissyo': []
    }
    for idx, place in enumerate(place_name):
        # 最終的にデータを集めるリスト (下に書いてある初期値は一行目。つまり、ヘッダー。)
        print(place)
        index = place_name.index(place)
        # 今日の年月を所得して
        year = datetime.date.today().year
        month = datetime.date.today().month
        r = requests.get(base_url % (place_codeA[index], place_codeB[index], year, month))
        r.encoding = r.apparent_encoding
        # まずはサイトごとスクレイピング
        soup = BeautifulSoup(r.text, 'html.parser')
        # findAllで条件に一致するものをすべて抜き出します。
        # 今回の条件はtrタグでclassがmtxになってるものです。
        rows = soup.findAll('tr', class_='mtx')

        # 表の最初の1~4行目はカラム情報なのでスライスする。(indexだから初めは0だよ)
        rows = rows[3:]
        # 1日〜最終日までの１行を網羅し、取得します。
        for row in rows:
            # 今度はtrのなかのtdをすべて抜き出します
            data = row.findAll('td')
            yesterday = datetime.datetime.now() - datetime.timedelta(1)
            if int(data[0].string) == int(yesterday.day):
                # １行の中には様々なデータがあるので全部取り出す。
                All_list['ymd'].append(str(year) + "-" + str(month) + "-" + str(data[0].string))
                All_list['pref_no'].append(place_codeA)
                All_list['chiku_no'].append(place_codeB)
                # All_list['kiatsu_riku'].append(str2float(data[1].string))
                # All_list['kiatsu_umi'].append(str2float(data[2].string))
                All_list['kousuiryo'].append(str2float(data[1].string))
                All_list['kion_ave'].append(str2float(data[4].string))
                # All_list['shitsudo_ave'].append(str2float(data[9].string))
                All_list['fuusoku'].append(str2float(data[7].string))
                All_list['nissyo'].append(str2float(data[13].string))
        time.sleep(4)  # 待機処理4秒
        df = pd.DataFrame(All_list)
        print(df)
        # mysql
        con_str = 'mysql+mysqldb://python:python123@127.0.0.1/db?charset=utf8&use_unicode=1'
        con = create_engine(con_str, echo=False).connect()
        df.to_sql('sample_1_temperature', con, if_exists='append', index=None)
