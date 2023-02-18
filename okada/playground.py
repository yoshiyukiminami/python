import re

import pandas as pd
from dateutil.relativedelta import relativedelta


def patch_the_month(target_df: pd.DataFrame) -> pd.DataFrame:
    """
    1~3月に12を加算することで、年またぎに対応した並びにすることができる
    4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

    :param target_df: 任意のデータフレーム
    :rtype: DataFrame
    """
    target_df['年月日'] = pd.to_datetime(target_df['年月日'])
    target_df['月日'] = [f"{re.sub('^0[1-3]', f'{12 + int(x[:2])}', x)}" for x in target_df['年月日'].dt.strftime('%m-%d')]
    target_df['年度'] = [(x - relativedelta(months=3)).strftime('%Y') for x in target_df['年月日']]

    return target_df


if __name__ == "__main__":
    # read csv and edit ymd
    df = pd.read_csv('data.csv', encoding='shift-jis')

    # pivot table
    df_slice_perspective = pd.pivot_table(patch_the_month(df), index=['観測地点', '月日'], columns='年度', values='平均気温')
    df_slice_perspective.to_csv('output/pivot.csv')
