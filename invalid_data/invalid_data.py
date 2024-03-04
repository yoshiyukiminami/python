import os

import numpy as np
import pandas as pd

INVALID_DATA_VALUE = 232


class DataRange:
    def __init__(self, start_pos: int, end_pos: int):
        self.start_pos = start_pos
        self.end_pos = end_pos
        if self.is_both_not_none():
            self.length = self.end_pos - self.start_pos + 1
        else:
            self.length = None

    def is_both_none(self):
        return self.start_pos is None and self.end_pos is None

    def is_both_not_none(self):
        return self.start_pos is not None and self.end_pos is not None


class NumericRange(DataRange):
    def __str__(self):
        return f"NumericRange(start={self.start_pos}, end={self.end_pos}, length={self.length})"


class PunchRange(DataRange):
    def __str__(self):
        return f"PunchRange(start={self.start_pos}, end={self.end_pos}, length={self.length})"


class HardPanRange(DataRange):
    def __str__(self):
        return f"HardPanRange(start={self.start_pos}, end={self.end_pos}, length={self.length})"


class RangeExtractor:
    def __init__(self, series: pd.Series):
        self.raw = series
        self.numeric_range = None
        self.punch_range = None
        self.hard_pan_range = None
        self.extract_data_ranges()

    def extract_data_ranges(self):
        self.numeric_range = NumericRange(self.raw.index.get_loc('圧力[kPa]1cm'),
                                          self.raw.index.get_loc('圧力[kPa]60cm'))
        intercept = self.raw.index.get_loc('圧力[kPa]1cm')
        spike_point_start = self.find_spike_point_in_line(INVALID_DATA_VALUE, False)
        spike_point_end = self.find_spike_point_in_line(INVALID_DATA_VALUE, True)
        if spike_point_start is not None:
            spike_point_start += intercept
        if spike_point_end is not None:
            spike_point_end += intercept
        self.punch_range = PunchRange(spike_point_start, spike_point_end)

        if not self.punch_range.is_both_none():
            if self.punch_range.end_pos < self.numeric_range.end_pos:
                self.hard_pan_range = HardPanRange(self.punch_range.end_pos + 1, self.numeric_range.end_pos)
        else:
            self.hard_pan_range = self.numeric_range

    def find_spike_point_in_line(self,  threshold: int, reverse: bool = False) -> int | None:
        """
        指定した範囲内のデータ（行）を順（または逆順）に調べ、閾値（threshold）を超える値が見つかった最初の位置を返す
        :param threshold: 値がこれを超えたら"spike"とみなす
        :param reverse: このフラグがTrueならば逆順にデータを調査する
        :return: 閾値を超えた最初の位置
        """
        line_slice = self.raw.iloc[self.numeric_range.start_pos:self.numeric_range.end_pos + 1]

        if reverse:
            line_slice = line_slice[::-1]

        exceeded_index = self.iterate_and_find_exceeded_threshold_in_line(line_slice, threshold)

        if reverse and exceeded_index is not None:
            exceeded_index = len(line_slice) - exceeded_index - 1

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


class FillingIndexes:
    def __init__(self, part1_of_mean: int = 0, invalid_start: int = 0, invalid_end: int = 0, part2_of_mean: int = 0):
        self.part1_of_mean = part1_of_mean
        self.invalid_start = invalid_start
        self.invalid_end = invalid_end
        self.part2_of_mean = part2_of_mean


def average_fill(line: list, threshold: int, start_position: int = 0) -> list:
    """
    :param line: 数値のリストで表現されたデータ行
    :param threshold: 無効な値を決定するために使用する閾値
    :param start_position: 無効な値のチェックを開始する行の開始位置
    :return: 無効な値が周りの有効な値の平均で置き換えられ、修正された数値のリスト

    このメソッドは、数値のリストとして表現されたデータ行を取り、無効な値（閾値を超える値）を周囲の有効な値の平均で置き換えます。閾値は値が無効であるかどうかを判断するために使用されます。
    start_positionが指定されている場合、その行のインデックスから無効な値のチェックを開始します。

    このメソッドは、行内の複数の無効な値を処理するために再帰を使用します。無効な値が見つかると、メソッドは前後の有効な値の平均を計算し、
    その無効な値を計算した平均で置き換えます。次に、それ自体を再帰的に呼び出し、置き換えた値のインデックスから開始して、さらに無効な値をチェックします。
    このメソッドは、すべての無効な値がその平均で置き換えられ、修正された数値のリストを返します。

    Example usage:
        line = [1334, 232, 232, 1360]
        threshold = 232
        result = average_fill(line, threshold)
        print(result)  # Output: [1334, 1347.0, 1347.0, 1360]
    """
    if start_position is not None:
        idx = FillingIndexes()
        punch_in = False
        for col, value in enumerate(line[start_position::]):
            if not punch_in and value == threshold:
                idx.part1_of_mean = start_position + col - 1
                idx.invalid_start = start_position + col
                punch_in = True
            if punch_in and value > threshold:
                idx.invalid_end = start_position + col - 1
                idx.part2_of_mean = start_position + col
                for j in range(idx.invalid_start, idx.invalid_end + 1):
                    line[j] = sum([line[idx.part1_of_mean], line[idx.part2_of_mean]]) / 2
                line = average_fill(line, threshold, idx.part2_of_mean)
                break

    return line


def linear_fill(line: list, start_position: int = 0) -> list:
    """
    指定された行にある欠損値を線形補間を使用して埋めます

    :param line: 欠損値を埋める対象の行
    :param start_position: 欠損値の補間を開始する位置（再帰的に変わる）
    :return: 線形補間を用いて欠損値が補完された行
    """
    if start_position is not None:
        idx = FillingIndexes()
        punch_in = False
        for col, value in enumerate(line[start_position::]):
            if not punch_in and np.isnan(value):
                idx.part1_of_mean = start_position + col - 1
                idx.invalid_start = start_position + col
                punch_in = True
            if punch_in and not np.isnan(value):
                idx.invalid_end = start_position + col - 1
                idx.part2_of_mean = start_position + col
                how_many_times = idx.part2_of_mean - idx.part1_of_mean + 1
                tolerance = np.linspace(line[idx.part1_of_mean], line[idx.part2_of_mean], how_many_times)
                for i, n_value in enumerate(tolerance):
                    line[idx.part1_of_mean + i] = n_value
                line = linear_fill(line, idx.part2_of_mean)
                break

    return line


def manage_invalid_values_with_adjustment(series: pd.Series, range_extractor: RangeExtractor, output_records: list):
    if range_extractor.punch_range.is_both_not_none():
        # TODO: ここはいまで average_fill を実行するので process.type みたいなので選択できるといいと思う
        start_pos = range_extractor.numeric_range.start_pos + range_extractor.punch_range.start_pos
        output_records.append(average_fill(list(series), INVALID_DATA_VALUE, start_pos))
    else:
        output_records.append(list(series))  # このケースは「すべて232」のケース


def manage_invalid_values_without_adjustment(i, series: pd.Series, range_extractor: RangeExtractor,
                                             output_records: list):
    if range_extractor.punch_range.start_pos == range_extractor.punch_range.end_pos is None:
        error_message = f"{i + 1}行目のデータは無効なデータ値 {INVALID_DATA_VALUE} のみで構成されています。確認してください"
        output_records.append([error_message])
        return
    # 両端の INVALID_DATA_VALUE を除外したスライスデータにします
    line = series[range_extractor.punch_range.start_pos:range_extractor.punch_range.end_pos + 1]
    for col, cell in enumerate(line):
        if cell == INVALID_DATA_VALUE:
            error_message = f"{i + 1}行目のデータには無効なデータ値 {INVALID_DATA_VALUE} が含まれています"
            output_records.append([error_message])
            break


def find_invalid_records(data: pd.DataFrame, apply_adjustment: bool, output_directory: str = './output'):
    """
    指定されたデータ内で無効なレコードを見つけ、apply_adjustment が指定された場合には補正を適用します

    :param data: 検証するレコードを含むデータフレーム
    :param apply_adjustment: 無効なレコードに補正を適用するかどうか
    :param output_directory: 出力ファイルを保存するディレクトリ
    :return: 出力レコードのリスト
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_records = [] if not apply_adjustment else [list(data.columns)]
    for i, row in data.iterrows():
        range_extractor = RangeExtractor(row)
        if not apply_adjustment:
            manage_invalid_values_without_adjustment(i, row, range_extractor, output_records)
        else:
            manage_invalid_values_with_adjustment(row, range_extractor, output_records)

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
