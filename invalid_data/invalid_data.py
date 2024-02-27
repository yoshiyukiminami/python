import os

import numpy as np
import pandas as pd


def iterate_and_find_exceeded_threshold_in_line(line_slice: list, threshold: int, start_position: int,
                                                direction: int) -> int | None:
    """
    line_sliceの中で与えられた閾値を超える最初の要素のインデックスを取得

    :param line_slice: 反復処理を行う行のスライス
    :param threshold: 閾値（通常は 232 ）
    :param start_position: 結果となるインデックスに追加されるオフセット
    :param direction: The direction in which to iterate (-1 for reverse, 1 for forward).
    :return: The index of the first element that exceeds the threshold, or None if not found.
    """
    for i, value in enumerate(line_slice):
        if value > threshold:
            return start_position + (i * direction)
    return None


def find_spike_point_in_line(line: list, threshold: int, process_range: tuple, reverse: bool = False) -> int:
    """
    指定した範囲内のデータ（行）を順（または逆順）に調べ、閾値（threshold）を超える値が見つかった最初の位置を返す
    :param line: データの行
    :param threshold: 値がこれを超えたら"spike"とみなす
    :param process_range: 調査の開始位置と終了位置
    :param reverse: このフラグがTrueならば逆順にデータを調査する
    :return: 閾値を超えた最初の位置
    """
    direction = 1 if not reverse else -1
    from_index, to_index = process_range if not reverse else reversed(process_range)
    line_slice = line[from_index:to_index:direction]
    exceeded_index = iterate_and_find_exceeded_threshold_in_line(line_slice, threshold, from_index, direction)

    # 閾値を超える値が見つからなかった場合、終了位置（to_index）を返す
    return to_index if exceeded_index is None else exceeded_index


def average_fill(line: list, threshold: int, start_position: int = 0) -> list:
    """
    補完開始位置と終了位置を認識して、返し縫いのように平均値で埋めていく
    :param line: 補正される対象（1行分のデータ）
    :param threshold: スパイク判定基準
    :param start_position: カーソルの初期位置（例：100列処理するうち20列目から開始に19を指定）
    :return: 修正後の line
    """
    if start_position != len(line):
        idx = {
            'mean1': 0,  # 平均の材料1
            'punch_in': 0,
            'punch_out': 0,
            'mean2': 0  # 平均の材料2
        }
        punch_in = False
        for col, value in enumerate(line[start_position::]):
            if not punch_in and value == threshold:
                idx["mean1"] = start_position + col - 1
                idx["punch_in"] = start_position + col
                punch_in = True
            if punch_in and value > threshold:
                idx["punch_out"] = start_position + col - 1
                idx["mean2"] = start_position + col
                for j in range(idx["punch_in"], idx["punch_out"] + 1):
                    line[j] = sum([line[idx["mean1"]], line[idx["mean2"]]]) / 2
                line = average_fill(line, threshold, idx["mean2"])
                break

    return line


def linear_fill(line: list, start_position: int = 0) -> list:
    """
    補完開始位置と終了位置を認識して、返し縫いのように線形回帰で埋めていく
    :param line: 補正される対象（1行分のデータ）
    :param start_position: カーソルの初期位置（例：100列処理するうち20列目から開始に19を指定）
    :return: 修正後の line
    """
    if start_position != len(line):
        idx = {
            'mean1': 0,  # 平均の材料1
            'punch_in': 0,
            'punch_out': 0,
            'mean2': 0  # 平均の材料2
        }
        punch_in = False
        for col, value in enumerate(line[start_position::]):
            if not punch_in and np.isnan(value):
                idx["mean1"] = start_position + col - 1
                idx["punch_in"] = start_position + col
                punch_in = True
            if punch_in and not np.isnan(value):
                idx["punch_out"] = start_position + col - 1
                idx["mean2"] = start_position + col
                how_many_times = max(idx["mean1"], idx["mean2"]) - min(idx["mean1"], idx["mean2"]) + 1
                tolerance = np.linspace(line[idx["mean1"]], line[idx["mean2"]], how_many_times)
                for i, n_value in enumerate(tolerance):
                    line[idx["mean1"] + i] = n_value
                line = linear_fill(line, idx["mean2"])
                break

    return line


def find_invalid_data(file_path: str, apply_adjustment: bool):
    """
    shift-jisを前提としたcsvを読み込み、不正値（under_threshold）を含む行をlistで返す\n
    step1: 深度60cmからマイナス方向に、232を初めて超える列までを1行あたりの処理範囲とする\n
    step2: 深度1cmからプラス方向に、232を初めて超える列以降の列を1行あたりの処理範囲とする\n
    step3-A: 定まった処理範囲のなかで232が見つかったらエラー行情報として返却する\n
    step3-B: 定まった処理範囲のなかで232が見つかったら両サイドの平均値で埋める（1行の中で複数発生することもある）\n
    :param file_path: CSVパス
    :param apply_adjustment: 無効値の補正を行う場合は True にする
    :return: apply_adjustment が False の場合はエラーリストを、Trueの場合は補正済みのデータを返す
    """
    under_threshold = 232
    df_csv = pd.read_csv(file_path, encoding='shift-jis')

    # output フォルダがなければ作成
    os.makedirs(name='./output', exist_ok=True)

    records = [] if not apply_adjustment else [list(df_csv.columns)]
    for i, line in enumerate(df_csv.itertuples(index=False)):
        offset = (df_csv.columns.get_loc('圧力[kPa]1cm'), df_csv.columns.get_loc('圧力[kPa]60cm'))
        first_col_in_a_line = find_spike_point_in_line(line, under_threshold, offset, False)
        end_col_in_a_line = find_spike_point_in_line(line, under_threshold, offset, True)
        if not apply_adjustment:
            line = line[first_col_in_a_line:end_col_in_a_line + 1]  # slice の end は "未満" なので注意する
            if len(line) == 0:
                records.append([str(i + 1) + f"行目のデータは無効なデータ値 {under_threshold} のみで構成されています。確認してください"])
                continue
            for col, cell in enumerate(line):
                if cell == under_threshold:
                    records.append([str(i + 1) + f"行目のデータは無効なデータ値 {under_threshold} が含まれています"])
                    break
        else:
            records.append(average_fill(list(line), under_threshold, first_col_in_a_line))

    return records


if __name__ == "__main__":
    print('エラー値調整なし版：')
    errors = find_invalid_data('data_sample_error-disp-on.csv', apply_adjustment=False)
    for error in errors:
        print(error.pop())

    print('エラー値調整あり版：')
    df = pd.DataFrame(find_invalid_data('data_sample_error-disp-on.csv', apply_adjustment=True))
    try:
        df.to_csv('output/processed_data.csv', encoding='shift-jis', header=False, index=False)
        print('output/processed_data.csv に出力が完了しました')
    except PermissionError:
        print('※ファイルが使用中のため、CSV出力に失敗しました')
