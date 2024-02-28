import os

import numpy as np
import pandas as pd

INVALID_DATA_VALUE = 232


class DataRange:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos


class NumericRange(DataRange):
    def __str__(self):
        return f"NumericRange(start={self.start_pos}, end={self.end_pos})"


class PunchRange(DataRange):
    def __str__(self):
        return f"PunchRange(start={self.start_pos}, end={self.end_pos})"


class RecordValidator:
    def __init__(self, row: pd.Series):
        self.raw = row
        self.numeric_range = None
        self.punch_range = None
        self.extract_data_ranges()

    def extract_data_ranges(self):
        self.numeric_range = NumericRange(self.raw.index.get_loc('圧力[kPa]1cm'),
                                          self.raw.index.get_loc('圧力[kPa]60cm'))
        self.punch_range = PunchRange(
            self.find_spike_point_in_line(list(self.raw), INVALID_DATA_VALUE, self.numeric_range, False),
            self.find_spike_point_in_line(list(self.raw), INVALID_DATA_VALUE, self.numeric_range, True)
        )

    def find_spike_point_in_line(self, line: list, threshold: int, process_range: NumericRange,
                                 reverse: bool = False) -> int | None:
        """
        指定した範囲内のデータ（行）を順（または逆順）に調べ、閾値（threshold）を超える値が見つかった最初の位置を返す
        :param line: データの行
        :param threshold: 値がこれを超えたら"spike"とみなす
        :param process_range: 調査の開始位置と終了位置
        :param reverse: このフラグがTrueならば逆順にデータを調査する
        :return: 閾値を超えた最初の位置
        """
        line_slice = line[process_range.start_pos:process_range.end_pos]

        if reverse:
            line_slice = line_slice[::-1]  # Only reverse the slice if needed

        exceeded_index = self.iterate_and_find_exceeded_threshold_in_line(line_slice, threshold)

        if reverse and exceeded_index is not None:
            exceeded_index = len(line_slice) - exceeded_index - 1  # Adjust index if reversed

        return exceeded_index

    @staticmethod
    def iterate_and_find_exceeded_threshold_in_line(line_slice: list, threshold: int) -> int | None:
        """
        データ（行）を順に調べ、閾値（threshold）を超える値が見つかった最初の位置を返す。
        :param line_slice: データの行 (スライス)。
        :param threshold: 値がこれを超えたら"spike"と見なす。
        :return: 閾値を超えた最初の位置。
        """
        for i, value in enumerate(line_slice):
            if value > threshold:
                return i
        return None


def average_fill(line: list, threshold: int, start_position: int = 0) -> list:
    """
    補完開始位置と終了位置を認識して、返し縫いのように平均値で埋めていく
    :param line: 補正される対象（1行分のデータ）
    :param threshold: スパイク判定基準
    :param start_position: カーソルの初期位置（例：100列処理するうち20列目から開始に19を指定）
    :return: 修正後の line
    """
    if start_position is not None:
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
    if start_position is not None:
        # TODO: リソース（クラス化）にして型安全にしたいね
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


def manage_invalid_values_with_adjustment(line, record_validator: RecordValidator, records):
    if record_validator.punch_range.start_pos is not None:
        # TODO: ここはいま average_fill しかできないので process.type みたいなので選択できるといいと思う
        start_pos = record_validator.numeric_range.start_pos + record_validator.punch_range.start_pos
        records.append(average_fill(list(line), INVALID_DATA_VALUE, start_pos))
    else:
        records.append(list(line))  # このケースは「すべて232」のケース


def manage_invalid_values_without_adjustment(i, line, record_validator: RecordValidator, records):
    if record_validator.punch_range.start_pos == record_validator.punch_range.end_pos is None:
        records.append([
            str(i + 1) + f"行目のデータは無効なデータ値 {INVALID_DATA_VALUE} のみで構成されています。確認してください"])
        return
    # 両端の INVALID_DATA_VALUE を除外したスライスデータにします
    line = line[record_validator.punch_range.start_pos:record_validator.punch_range.end_pos + 1]
    for col, cell in enumerate(line):
        if cell == INVALID_DATA_VALUE:
            records.append([str(i + 1) + f"行目のデータは無効なデータ値 {INVALID_DATA_VALUE} が含まれています"])
            break


def find_invalid_records(data: pd.DataFrame, apply_adjustment: bool, output_directory: str = './output'):
    """
    TODO: find_invalid_records は manage_... のふたつをクラス化してカプセル化できると思う
    この関数は 'shift-jis' でエンコードされたCSVファイルを読み込み、INVALID_DATA_VALUEを含む無効な行をチェックします。
    これらが見つかった場合、それらをリストとして返します。 apply_adjustment フラグが設定されている場合、
    この関数は見つかった任意の無効な値を、隣接する値の平均で置き換えます。

    :param data: CSVから読み込まれた DataFrame
    :param apply_adjustment: True の場合、無効な値に対して補正が行われます
    :param output_directory: 出力ファイルが保存されるディレクトリ
    :return: apply_adjustmentがFalseの場合、無効な行のリストを返します。それ以外の場合、補正された値を持つ DataFrame を返します
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_records = [] if not apply_adjustment else [list(data.columns)]
    for i, row in data.iterrows():
        record_validator = RecordValidator(row)
        if not apply_adjustment:
            manage_invalid_values_without_adjustment(i, row, record_validator, output_records)
        else:
            manage_invalid_values_with_adjustment(row, record_validator, output_records)

    return output_records


if __name__ == "__main__":
    data_sample_path = 'data_sample_error-disp-on.csv'
    save_path = 'output/processed_data.csv'
    df_csv = pd.read_csv(data_sample_path, encoding='shift-jis')

    print('エラー値の補正なし版（コンソールに出力するだけ）：')
    errors = find_invalid_records(df_csv, apply_adjustment=False)
    for error in errors:
        print(error.pop())

    os.makedirs(name='output', exist_ok=True)

    print('\nエラー値の補正あり版：')
    df = pd.DataFrame(find_invalid_records(df_csv, apply_adjustment=True))
    try:
        df.to_csv(save_path, encoding='shift-jis', header=False, index=False)
        print(f'{save_path} に出力が完了しました')
    except PermissionError:
        print('※ファイルが使用中のため、CSV出力に失敗しました')
