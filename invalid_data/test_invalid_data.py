from unittest import TestCase
import numpy as np

from invalid_data import back_stitch2


class Test(TestCase):
    def test_back_stitch_one_zone_nan(self):
        data = [2, 10, np.nan, np.nan, np.nan, 5]
        expected_value = [2, 10.0, 8.75, 7.5, 6.25, 5.0]
        self.assertEqual(back_stitch2(data), expected_value)

    def test_back_stitch_some_zone_nan(self):
        data = [2, 10, np.nan, np.nan, np.nan, 5, np.nan, np.nan, 2]
        expected_value = [2, 10.0, 8.75, 7.5, 6.25, 5.0, 4, 3, 2]
        self.assertEqual(back_stitch2(data), expected_value)
