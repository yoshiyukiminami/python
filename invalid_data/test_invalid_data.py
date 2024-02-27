from unittest import TestCase
import numpy as np

from invalid_data import find_spike_point_in_line, average_fill, linear_fill


class TestGetCursorOfSpike(TestCase):
    def test_get_cursor_of_spike_no_inverse_no_offset(self):
        result = find_spike_point_in_line([0, 1, 2, 3, 4, 5, 5, 7, 8, 9], 4, (0, 9))
        self.assertEqual(5, result)

    def test_get_cursor_of_spike_inverse_no_offset(self):
        result = find_spike_point_in_line([1, 2, 3, 4, 5, 7, 6, 5, 4, 3], 4, (0, 9), reverse=True)
        self.assertEqual(7, result)

    def test_get_cursor_of_spike_no_inverse_with_offset(self):
        result = find_spike_point_in_line(['属性', '属性', 3, 4, 5, 5, 4, 3, 2, '属性'], 4, process_range=(2, 8))
        self.assertEqual(2, result)

    def test_get_cursor_of_spike_inverse_with_offset(self):
        result = find_spike_point_in_line(['属性', '属性', 3, 4, 5, 5, 4, 3, 2, '属性'], 4, process_range=(2, 8), reverse=True)
        self.assertEqual(3, result)

    def test_get_cursor_of_spike_no_spike(self):
        result = find_spike_point_in_line([1, 2, 3, 4, 5, 5, 4, 3, 2, 1], 6, (0, 9))
        self.assertEqual(None, result)


class TestAverageFill(TestCase):
    def test_average_fill_normal(self):
        """
        通常のケースでの'average_fill'のテスト
        """
        data = [1334, 232, 232, 1360]
        threshold = 232
        expected = [1334, 1347, 1347, 1360]
        result = average_fill(data, threshold)
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
