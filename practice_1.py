import pandas as pd

# サンプルのDataFrameを作成
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['a', 'b', 'c'],
    'C': [True, False, True]
})
print(df)

# DataFrameをネストした辞書に変換する関数を定義
def df_to_dict(df):
    return {col: df[col].to_list() for col in df.columns}

# DataFrameをネストした辞書に変換
nested_dict = {'data': df_to_dict(df)}

# 結果を表示
print(nested_dict)
