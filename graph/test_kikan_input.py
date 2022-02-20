from unittest import TestCase

from graph.kikan_input import check_input_kikan_start_day, check_input_kikan_start_month, \
    check_input_kikan_start_year, check_input_kako_compare_kikan, check_input_kikan_stop_year, \
    check_input_kikan_stop_month, check_input_kikan_stop_day


class Test(TestCase):
    def test_check_input_kikan_start_year(self):
        self.assertEqual(2021, check_input_kikan_start_year())


class Test2(TestCase):
    def test_check_input_kikan_start_month(self):
        self.assertEqual(1, check_input_kikan_start_month())


class Test3(TestCase):
    def test_check_input_kikan_start_day(self):
        self.assertEqual(10, check_input_kikan_start_day())


class Test4(TestCase):
    def test_check_input_kikan_stop_year(self):
        self.assertEqual(2022, check_input_kikan_stop_year())


class Test5(TestCase):
    def test_check_input_kikan_stop_month(self):
        self.assertEqual(2, check_input_kikan_stop_month())


class Test7(TestCase):
    def test_check_input_kako_compare_kikan(self):
        self.assertEqual(10, check_input_kako_compare_kikan())


class Test6(TestCase):
    def test_check_input_kikan_stop_day(self):
        self.assertEqual(28, check_input_kikan_stop_day())
