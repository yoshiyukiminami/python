from unittest import TestCase

from graph.kikan_input import check_input_start_year, check_input_start_month


class Test1(TestCase):
    def test_check_input_start_year(self):
        self.assertEqual(2002, check_input_start_year())


class Test2(TestCase):
    def test_check_input_start_month(self):
        self.assertEqual(12, check_input_start_month())


