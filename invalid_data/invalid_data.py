import os
from typing import Callable

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


class HardPanCursor:
    def __init__(self, value):
        if not (1 <= value <= 60):
            raise ValueError("Value must be within the range 1-60.")
        self.value = value

    def __str__(self):
        return f"圧力[kPa]{self.value}cm"


class RangeExtractor:
    def __init__(self, series: pd.Series, hard_pan_cursor: HardPanCursor):
        self.raw = series
        self.hard_pan_cursor = hard_pan_cursor
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

    def is_hard_pan(self) -> bool:
        if self.hard_pan_range:
            return self.hard_pan_range.start_pos < self.raw.index.get_loc(str(self.hard_pan_cursor))

        return False


class FillingIndexes:
    def __init__(self, part1_of_mean: int = 0, invalid_start: int = 0, invalid_end: int = 0, part2_of_mean: int = 0):
        self.part1_of_mean = part1_of_mean
        self.invalid_start = invalid_start
        self.invalid_end = invalid_end
        self.part2_of_mean = part2_of_mean

    def __str__(self):
        return (f"part1_of_mean: {self.part1_of_mean}, self.invalid_start: {self.invalid_start}, "
                f"self.invalid_end: {self.invalid_end}, part2_of_mean: {self.part2_of_mean}")


def fill(line: list[int], recur_start_position: int, func: Callable) -> list:
    """
    線内の欠損値を補間を用いて埋めます

    :param line: 線データを表す整数値のリスト
    :param recur_start_position: 再帰的な塗りつぶしに対するライン内の開始位置
    :param func: 線上で補間を行う関数
    :return: 補間を使用して欠損値を埋めた新しいリスト
    """
    idx = FillingIndexes()
    punch_in = False
    for col, value in enumerate(line[recur_start_position::]):
        if not punch_in and value == INVALID_DATA_VALUE:
            idx.part1_of_mean = recur_start_position + col - 1
            idx.invalid_start = recur_start_position + col
            punch_in = True
        if punch_in and value > INVALID_DATA_VALUE:
            idx.invalid_end = recur_start_position + col - 1
            idx.part2_of_mean = recur_start_position + col
            line = fill(func(line, idx), idx.part2_of_mean, func)
            break
    return line


def interpolation_average(line: list, idx: FillingIndexes) -> list:
    """
    与えられたlistに対する補間平均を計算します

    :param line: 補間されるべき値のリスト
    :param idx: 無効なセクションの開始と終了のインデックス、および平均値の2部分のインデックスを含むオブジェクト
    :return: 補間されたあとの line

    Example usage:
     line = [1, 2, 3, 4, 5]
     idx = FillingIndexes()
     idx.part1_of_mean = 0
     idx.invalid_start = 1
     idx.invalid_end = 3
     idx.part2_of_mean = 4
     interpolation_average(line, idx)
       [1, 2.5, 2.5, 2.5, 5]
    """
    for j in range(idx.invalid_start, idx.invalid_end + 1):
        line[j] = sum([line[idx.part1_of_mean], line[idx.part2_of_mean]]) / 2
    return line


def interpolation_linear(line: list, idx: FillingIndexes) -> list:
    """
    与えられたlistに対する線形補間を計算します

    :param line: 補間されるべき値のリスト
    :param idx: 補間されるべき値のインデックスを含むFillingIndexesクラスのオブジェクト
    :return: 補間されたあとの line
    """
    how_many_times = idx.part2_of_mean - idx.part1_of_mean + 1
    tolerance = np.linspace(line[idx.part1_of_mean], line[idx.part2_of_mean], how_many_times)
    for i, n_value in enumerate(tolerance):
        line[idx.part1_of_mean + i] = n_value
    return line


def manage_invalid_values_with_adjustment(r: RangeExtractor, output_records: list):
    # TODO: 南さんからもらう最新のcsvで処理して最後の列に追加する
    #  硬盤有無: 硬盤があるか？の 0 1 列
    #  硬盤深度: 何センチ？の情報
    if r.punch_range.is_both_not_none():
        output_records.append(fill(list(r.raw), r.punch_range.start_pos, interpolation_linear))
    else:
        output_records.append(list(r.raw))


def manage_invalid_values_without_adjustment(i, r: RangeExtractor, output_records: list):
    hard_pan_cm = r.raw.index[r.hard_pan_range.start_pos]
    if r.punch_range.is_both_none():
        error_message = f"{i + 1}行目のデータは無効なデータ値 {INVALID_DATA_VALUE} のみで構成されています。({r.is_hard_pan()}, {hard_pan_cm})"
        output_records.append([error_message])
        return
    # 両端の INVALID_DATA_VALUE を除外したスライスデータにします
    punch_range = r.raw.iloc[r.punch_range.start_pos:r.punch_range.end_pos + 1]
    for col, cell in enumerate(punch_range):
        if cell == INVALID_DATA_VALUE:
            error_message = f"{i + 1}行目のデータには無効なデータ値 {INVALID_DATA_VALUE} が含まれています({r.is_hard_pan()}, {hard_pan_cm})"
            output_records.append([error_message])
            break


def find_invalid_records(data: pd.DataFrame, apply_adjustment: bool, hard_pan_cursor: HardPanCursor,
                         output_directory: str = './output'):
    """
    指定されたデータ内で無効なレコードを見つけ、apply_adjustment が指定された場合には補正を適用します

    :param data: 検証するレコードを含むデータフレーム
    :param apply_adjustment: 無効なレコードに補正を適用するかどうか
    :param hard_pan_cursor: 50センチ `未満` で232が発生したら の位置
    :param output_directory: 出力ファイルを保存するディレクトリ
    :return: 出力レコードのリスト
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_records = [] if not apply_adjustment else [list(data.columns)]
    for i, row in data.iterrows():
        range_extractor = RangeExtractor(row, hard_pan_cursor)
        if not apply_adjustment:
            manage_invalid_values_without_adjustment(i, range_extractor, output_records)
        else:
            manage_invalid_values_with_adjustment(range_extractor, output_records)

    return output_records


if __name__ == "__main__":
    data_sample_path = 'input/キャロットFARM_soil_data-20240228.csv'
    save_path = 'output/processed_data.csv'
    hard_pan_less_than_cm = HardPanCursor(50)
    df_csv = pd.read_csv(data_sample_path, encoding='shift-jis')

    print('エラー値の補正なし版（コンソールに出力するだけ）：')
    errors = find_invalid_records(df_csv, False, hard_pan_less_than_cm)
    for error in errors:
        print(error.pop())

    os.makedirs(name='output', exist_ok=True)

    print('\nエラー値の補正あり版：')
    df = pd.DataFrame(find_invalid_records(df_csv, True, hard_pan_less_than_cm))
    try:
        df.to_csv(save_path, encoding='shift-jis', header=False, index=False)
        print(f'{save_path} に出力が完了しました')
    except PermissionError:
        print('※ファイルが使用中のため、CSV出力に失敗しました')
