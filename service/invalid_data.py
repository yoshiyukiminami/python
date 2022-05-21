import os
import pandas as pd


def get_cursor_of_spike(line: list, threshold: int, offset: tuple = None, inverse: bool = False) -> int:
    """
    list に対して direction 方向にloopして、 threshold を初めて超える列番号を返却
    :param offset: カーソルの初期位置（例：100列処理するうち20列目から開始に19を指定）
    :param line: スパイク検査される対象（1行分のデータ）
    :param threshold: スパイク判定基準
    :param inverse: 逆方向から見る場合に True にする
    :return: threshold を初めて超える列番号
    """
    direction = 1 if not inverse else -1
    adjusted_start_cursor = offset[0] if not inverse else offset[1]
    adjusted_end_cursor = offset[1] if not inverse else offset[0]
    for i, value in enumerate(line[adjusted_start_cursor:adjusted_end_cursor:direction]):
        if value > threshold:
            return adjusted_start_cursor + (i * direction)

    return adjusted_end_cursor


def back_stitch(line: list, threshold: int, offset: int = 0) -> list:
    """
    返し縫いのように平均値で埋めていく
    :param line: 補正される対象（1行分のデータ）
    :param threshold: スパイク判定基準
    :param offset: カーソルの初期位置（例：100列処理するうち20列目から開始に19を指定）
    :return: 修正後の line
    """
    if offset != len(line):
        idx = {}  # [平均材料1, 修正パンチイン, 修正パンチアウト, 平均材料2]
        punch_in = False
        for col, value in enumerate(line[offset::]):
            if not punch_in and value == threshold:
                idx["mean1"] = offset + col - 1
                idx["punch_in"] = offset + col
                punch_in = True
            if punch_in and value > threshold:
                idx["punch_out"] = offset + col - 1
                idx["mean2"] = offset + col
                for j in range(idx["punch_in"], idx["punch_out"] + 1):
                    line[j] = sum([line[idx["mean1"]], line[idx["mean2"]]]) / 2
                line = back_stitch(line, threshold, idx["mean2"])
                break

    return line


def find_invalid_data(file_path: str, adjustment: bool):
    """
    shift-jisを前提としたcsvを読み込み、不正値（under_threshold）を含む行をlistで返す\n
    step1: 深度60cmからマイナス方向に、232を初めて超える列までを1行あたりの処理範囲とする\n
    step2: 深度1cmからプラス方向に、232を初めて超える列以降の列を1行あたりの処理範囲とする\n
    step3-A: 定まった処理範囲のなかで232が見つかったらエラー行情報として返却する\n
    step3-B: 定まった処理範囲のなかで232が見つかったら両サイドの平均値で埋める（1行の中で複数発生することもある）\n
    :param file_path: CSVパス
    :param adjustment: 無効値の補正を行う場合はTrueにする
    :return: adjustment が False の場合はエラーリストを、Trueの場合は補正後のデータを返す
    """
    under_threshold = 232
    df_csv = pd.read_csv(file_path, encoding='shift-jis')

    # output フォルダがなければ作成
    os.makedirs(name='./output', exist_ok=True)

    records = [] if not adjustment else [list(df_csv.columns)]
    for i, line in enumerate(df_csv.itertuples(index=False)):
        offset = (df_csv.columns.get_loc('圧力[kPa]1cm'), df_csv.columns.get_loc('圧力[kPa]60cm'))
        first_col_in_a_line = get_cursor_of_spike(line, under_threshold, offset, False)
        end_col_in_a_line = get_cursor_of_spike(line, under_threshold, offset, True)
        if not adjustment:
            line = line[first_col_in_a_line:end_col_in_a_line + 1]  # slice の end は "未満" なので注意する
            if len(line) == 0:
                records.append([str(i + 1) + f"行目のデータは無効なデータ値 {under_threshold} のみで構成されています。確認してください"])
            for col, cell in enumerate(line):
                if cell == under_threshold:
                    records.append([str(i + 1) + f"行目のデータは無効なデータ値 {under_threshold} が含まれています"])
                    break
        else:
            records.append(back_stitch(list(line), under_threshold, first_col_in_a_line))

    return records


if __name__ == "__main__":
    print('エラー値調整なし版：')
    errors = find_invalid_data('data_sample_error-disp-on.csv', adjustment=False)
    for error in errors:
        print(error)

    print('エラー値調整あり版：')
    df = pd.DataFrame(find_invalid_data('data_sample_error-disp-on.csv', adjustment=True))
    try:
        df.to_csv('output/processed_data.csv', encoding='shift-jis', header=False, index=False)
        print('output/processed_data.csv に出力が完了しました')
    except PermissionError:
        print('※ファイルが使用中のため、CSV出力に失敗しました')
