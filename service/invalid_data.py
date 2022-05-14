import pandas as pd


def find_invalid_data(file_path: str, depth: dict) -> list:
    """
    shift-jisを前提としたcsvを読み込み、不正値（under_threshold）を含む行をlistで返す
    :param file_path: CSVのフルパス
    :param depth: チェックする深さの from to
    :return:
    """
    under_threshold = 232
    df_csv = pd.read_csv(file_path, encoding='shift-jis')
    df = df_csv.loc[:, f'圧力[kPa]{depth["from"]}cm':f'圧力[kPa]{depth["to"]}cm']

    error_bug = []
    for line in df.itertuples():
        for element in line:
            if element == under_threshold:
                error_bug.append(str(line[0]+1) + "行目のデータは無効なデータ値が含まれています")
                break

    return error_bug


if __name__ == "__main__":
    errors = find_invalid_data('data_sample_error-disp-on.csv', {"from": 10, "to": 50})
    for error in errors:
        print(error)
