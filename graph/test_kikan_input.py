from unittest import TestCase

from graph.kikan_input import check_valid_date1, check_valid_date2, check_valid_date3


class Test1(TestCase):
    def test_check_valid_date1(self):
        self.assertEqual(2021, check_valid_date1())


class Test2(TestCase):
    def test_check_valid_date2(self):
        self.assertEqual(2022, check_valid_date2())


class Test3(TestCase):
    def test_check_valid_date3(self):
        self.assertEqual(10, check_valid_date3())
