from unittest import TestCase

import numpy as np
import pandas as pd

from invalid_data import average_fill, linear_fill, RangeExtractor, HardPanCursor

INVALID_DATA_VALUE = 232
NUMERIC_RANGE_LABELS = ['圧力[kPa]1cm', '圧力[kPa]2cm', '圧力[kPa]3cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                        '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]9cm', '圧力[kPa]60cm']
FULL_RANGE_LABELS = ['取引先名', '住所', '圧力[kPa]1cm', '圧力[kPa]4cm', '圧力[kPa]5cm', '圧力[kPa]6cm',
                     '圧力[kPa]7cm', '圧力[kPa]8cm', '圧力[kPa]60cm', '圧力[kPa]100cm']


class TestRecordValidator(TestCase):
    def setUp(self):
        self.hard_pan_less_than_cm = HardPanCursor(50)

    def test_get_cursor_of_spike_no_reverse_no_offset_with_invalid_value_on_both(self):
        data = [232, 350, 405, 301, 300, 232, 232, 232, 232, 232]
        range_extractor = RangeExtractor(pd.Series(data, index=NUMERIC_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(1, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE))
        self.assertEqual(0, range_extractor.numeric_range.start_pos)
        self.assertEqual(10, range_extractor.numeric_range.length)
        self.assertEqual(1, range_extractor.punch_range.start_pos)
        self.assertEqual(4, range_extractor.punch_range.length)
        self.assertEqual(5, range_extractor.hard_pan_range.start_pos)
        self.assertEqual(5, range_extractor.hard_pan_range.length)

    def test_get_cursor_of_spike_no_reverse_no_offset_with_invalid_value_on_left(self):
        data = [232, 232, 232, 232, 232, 300, 301, 405, 350, 400]
        range_extractor = RangeExtractor(pd.Series(data, index=NUMERIC_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(0, range_extractor.numeric_range.start_pos)
        self.assertEqual(10, range_extractor.numeric_range.length)
        self.assertEqual(5, range_extractor.punch_range.start_pos)
        self.assertEqual(5, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE))
        self.assertEqual(5, range_extractor.punch_range.length)
        self.assertIsNone(range_extractor.hard_pan_range)

    def test_get_cursor_of_spike_no_inverse_no_offset_with_invalid_value_on_right(self):
        data = [400, 350, 405, 301, 300, 232, 232, 232, 232, 232]
        range_extractor = RangeExtractor(pd.Series(data, index=NUMERIC_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(0, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE))
        self.assertEqual(0, range_extractor.numeric_range.start_pos)
        self.assertEqual(10, range_extractor.numeric_range.length)
        self.assertEqual(0, range_extractor.punch_range.start_pos)
        self.assertEqual(5, range_extractor.punch_range.length)
        self.assertEqual(5, range_extractor.hard_pan_range.start_pos)
        self.assertEqual(5, range_extractor.hard_pan_range.length)

    def test_get_cursor_of_spike_reverse_no_offset(self):
        data = [232, 232, 232, 232, 300, 301, 405, 350, 232, 232]
        range_extractor = RangeExtractor(pd.Series(data, index=NUMERIC_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(7, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE, reverse=True))
        self.assertEqual(0, range_extractor.numeric_range.start_pos)
        self.assertEqual(10, range_extractor.numeric_range.length)
        self.assertEqual(4, range_extractor.punch_range.start_pos)
        self.assertEqual(4, range_extractor.punch_range.length)
        self.assertEqual(8, range_extractor.hard_pan_range.start_pos)
        self.assertEqual(2, range_extractor.hard_pan_range.length)

    def test_get_cursor_of_spike_no_reverse_with_offset(self):
        data = ['あの会社', '北海道', 232, 232, 301, 405, 232, 232, 232, np.nan]
        range_extractor = RangeExtractor(pd.Series(data, index=FULL_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(2, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE))
        self.assertEqual(2, range_extractor.numeric_range.start_pos)
        self.assertEqual(7, range_extractor.numeric_range.length)
        self.assertEqual(4, range_extractor.punch_range.start_pos)
        self.assertEqual(2, range_extractor.punch_range.length)
        self.assertEqual(6, range_extractor.hard_pan_range.start_pos)
        self.assertEqual(3, range_extractor.hard_pan_range.length)

    def test_get_cursor_of_spike_reverse_with_offset(self):
        data = ['あの会社', '北海道', 232, 232, 301, 405, 232, 232, 232, np.nan]
        range_extractor = RangeExtractor(pd.Series(data, index=FULL_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(3, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE, reverse=True))
        self.assertEqual(2, range_extractor.numeric_range.start_pos)
        self.assertEqual(7, range_extractor.numeric_range.length)
        self.assertEqual(4, range_extractor.punch_range.start_pos)
        self.assertEqual(2, range_extractor.punch_range.length)
        self.assertEqual(6, range_extractor.hard_pan_range.start_pos)
        self.assertEqual(3, range_extractor.hard_pan_range.length)

    def test_get_cursor_of_spike_no_spike(self):
        data = [232, 232, 232, 232, 232, 232, 232, 232, 232, 232]
        range_extractor = RangeExtractor(pd.Series(data, index=NUMERIC_RANGE_LABELS), self.hard_pan_less_than_cm)
        self.assertEqual(None, range_extractor.find_spike_point_in_line(INVALID_DATA_VALUE))
        self.assertEqual(0, range_extractor.numeric_range.start_pos)
        self.assertEqual(10, range_extractor.numeric_range.length)
        self.assertEqual(None, range_extractor.punch_range.start_pos)
        self.assertEqual(None, range_extractor.punch_range.length)
        self.assertEqual(0, range_extractor.hard_pan_range.start_pos)
        self.assertEqual(10, range_extractor.hard_pan_range.length)


class TestAverageFill(TestCase):
    def test_average_fill_one_zone_232(self):
        """
        232値を含むゾーンが１つ存在するシナリオで、'average_fill'関数をテストします
        """
        data = [1334, 232, 232, 1360]
        expected = [1334, 1347.0, 1347.0, 1360]
        result = average_fill(data)
        self.assertEqual(expected, result)

    def test_average_fill_some_zone_232(self):
        """
        232値を含むゾーンが複数存在するシナリオで、'average_fill'関数をテストします
        """
        data = [1334, 232, 232, 1360, 232, 232, 1400]
        expected = [1334, 1347.0, 1347.0, 1360, 1380.0, 1380.0, 1400]
        result = average_fill(data)
        self.assertEqual(expected, result)


class TestLinearFill(TestCase):
    def test_linear_fill_one_zone_nan(self):
        """
        232値を含むゾーンが１つ存在するシナリオで、'linear_fill'関数をテストします

        :return: None
        """
        data = [1334, 232, 232, 1364]
        expected = [1334.0, 1344.0, 1354.0, 1364.0]
        self.assertEqual(expected, linear_fill(data))

    def test_linear_fill_some_zone_nan(self):
        """
        232値を含むゾーンが複数存在するシナリオで、'linear_fill'関数をテストします

        :return: None
        """
        data = [1334, 232, 232, 1364, 232, 232, 1406]
        expected = [1334.0, 1344.0, 1354.0, 1364.0, 1378.0, 1392.0, 1406.0]
        self.assertEqual(expected, linear_fill(data))


class TestHardPanCursor(TestCase):
    def test_constructor(self):
        self.assertEqual(HardPanCursor(30).value, 30)
        self.assertEqual(HardPanCursor(1).value, 1)
        self.assertEqual(HardPanCursor(60).value, 60)

    def test_constructor_value_out_of_range(self):
        with self.assertRaises(ValueError):
            HardPanCursor(-1)
            HardPanCursor(0)
            HardPanCursor(61)

    def test_str_method(self):
        cursor = HardPanCursor(30)
        self.assertEqual(str(cursor), "圧力[kPa]30cm")
