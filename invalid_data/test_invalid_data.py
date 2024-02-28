from unittest import TestCase

import numpy as np
import pandas as pd

from invalid_data import average_fill, linear_fill, RecordValidator

INVALID_DATA_VALUE = 232


class TestRecordValidator(TestCase):
    def test_get_cursor_of_spike_no_inverse_no_offset(self):
        data = [232, 232, 232, 232, 232, 300, 301, 405, 350, 400]
        labels = ['圧力[kPa]1cm', '圧力[kPa]2cm', '圧力[kPa]3cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                  '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]9cm', '圧力[kPa]60cm']
        record_validator = RecordValidator(pd.Series(data, index=labels))
        result = record_validator.find_spike_point_in_line(list(record_validator.row), INVALID_DATA_VALUE,
                                                           record_validator.numeric_range)
        self.assertEqual(5, result)

    def test_get_cursor_of_spike_inverse_no_offset(self):
        data = [232, 232, 232, 232, 300, 301, 405, 350, 232, 232]
        labels = ['圧力[kPa]1cm', '圧力[kPa]2cm', '圧力[kPa]3cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                  '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]9cm', '圧力[kPa]60cm']
        record_validator = RecordValidator(pd.Series(data, index=labels))
        result = record_validator.find_spike_point_in_line(list(record_validator.row), INVALID_DATA_VALUE,
                                                           record_validator.numeric_range, reverse=True)
        self.assertEqual(7, result)

    def test_get_cursor_of_spike_no_inverse_with_offset(self):
        data = ['あの会社', '北海道', 232, 232, 301, 405, 232, 232, 232, np.nan]
        labels = ['取引先名', '住所', '圧力[kPa]1cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                  '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]60cm', '圧力[kPa]100cm']
        record_validator = RecordValidator(pd.Series(data, index=labels))
        result = record_validator.find_spike_point_in_line(list(record_validator.row),
                                                           INVALID_DATA_VALUE,
                                                           record_validator.numeric_range)
        self.assertEqual(2, result)

    def test_get_cursor_of_spike_inverse_with_offset(self):
        data = ['あの会社', '北海道', 232, 232, 301, 405, 232, 232, 232, np.nan]
        labels = ['取引先名', '住所', '圧力[kPa]1cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                  '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]60cm', '圧力[kPa]100cm']
        record_validator = RecordValidator(pd.Series(data, index=labels))
        result = record_validator.find_spike_point_in_line(list(record_validator.row),
                                                           INVALID_DATA_VALUE,
                                                           record_validator.numeric_range,
                                                           reverse=True)
        self.assertEqual(3, result)

    def test_get_cursor_of_spike_no_spike(self):
        data = [232, 232, 232, 232, 232, 232, 232, 232, 232, 232]
        labels = ['圧力[kPa]1cm', '圧力[kPa]2cm', '圧力[kPa]3cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                  '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]9cm', '圧力[kPa]60cm']
        record_validator = RecordValidator(pd.Series(data, index=labels))
        result = record_validator.find_spike_point_in_line(list(record_validator.row), INVALID_DATA_VALUE,
                                                           record_validator.numeric_range)
        self.assertEqual(None, result)


class TestAverageFill(TestCase):
    def test_average_fill_one_zone_232(self):
        """
        232値を含むゾーンが１つ存在するシナリオで、'average_fill'関数をテストします
        """
        data = [1334, 232, 232, 1360]
        expected = [1334, 1347.0, 1347.0, 1360]
        result = average_fill(data, INVALID_DATA_VALUE)
        self.assertEqual(expected, result)

    def test_average_fill_some_zone_232(self):
        """
        232値を含むゾーンが複数存在するシナリオで、'average_fill'関数をテストします
        """
        data = [1334, 232, 232, 1360, 232, 232, 1400]
        expected = [1334, 1347.0, 1347.0, 1360, 1380.0, 1380.0, 1400]
        result = average_fill(data, INVALID_DATA_VALUE)
        self.assertEqual(expected, result)


class TestLinearFill(TestCase):
    def test_linear_fill_one_zone_nan(self):
        """
        NaN値を含むゾーンが１つ存在するシナリオで、'linear_fill'関数をテストします

        :return: None
        """
        data = [2, 10, np.nan, np.nan, np.nan, 5]
        expected = [2, 10.0, 8.75, 7.5, 6.25, 5.0]
        self.assertEqual(expected, linear_fill(data))

    def test_linear_fill_some_zone_nan(self):
        """
        NaN値を含むゾーンが複数存在するシナリオで、'linear_fill'関数をテストします

        :return: None
        """
        data = [2, 10, np.nan, np.nan, np.nan, 5, np.nan, np.nan, 2]
        expected = [2, 10.0, 8.75, 7.5, 6.25, 5.0, 4, 3, 2]
        self.assertEqual(expected, linear_fill(data))
