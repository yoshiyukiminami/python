from unittest import TestCase
import numpy as np

from invalid_data import find_spike_point_in_line, average_fill, linear_fill

INVALID_DATA_VALUE = 232


class TestGetCursorOfSpike(TestCase):
    def test_get_cursor_of_spike_no_inverse_no_offset(self):
        result = find_spike_point_in_line([232, 232, 232, 232, 232, 300, 301, 405, 350, 400], INVALID_DATA_VALUE,
                                          (0, 9))
        self.assertEqual(5, result)

    def test_get_cursor_of_spike_inverse_no_offset(self):
        result = find_spike_point_in_line([232, 232, 232, 232, 300, 301, 405, 350, 232, 232], INVALID_DATA_VALUE,
                                          (0, 9), reverse=True)
        self.assertEqual(7, result)

    def test_get_cursor_of_spike_no_inverse_with_offset(self):
        result = find_spike_point_in_line(['属性', '属性', 232, 232, 301, 405, 232, 232, 232, np.nan], INVALID_DATA_VALUE,
                                          process_range=(2, 8))
        self.assertEqual(2, result)

    def test_get_cursor_of_spike_inverse_with_offset(self):
        result = find_spike_point_in_line(['属性', '属性', 232, 232, 301, 405, 232, 232, 232, np.nan], INVALID_DATA_VALUE,
                                          process_range=(2, 8),
                                          reverse=True)
        self.assertEqual(3, result)

    def test_get_cursor_of_spike_no_spike(self):
        result = find_spike_point_in_line([232, 232, 232, 232, 232, 232, 232, 232, 232, 232], INVALID_DATA_VALUE,
                                          process_range=(0, 9))
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
