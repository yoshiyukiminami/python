from unittest import TestCase

from soil_analysis.crm.domain.valueobject.coordinates import Coordinates


class TestCoordinates(TestCase):
    def test_init_single_coordinate(self):
        coordinates_str = "137.6489657,34.7443565"
        coordinates = Coordinates(coordinates_str)
        self.assertEqual(137.6489657, coordinates.longitude)
        self.assertEqual(34.7443565, coordinates.latitude)

    def test_init_multiple_coordinates(self):
        coordinates_str = "137.6489657,34.7443565 137.6491266,34.744123"
        coordinates = Coordinates(coordinates_str)
        self.assertEqual(137.6490462, coordinates.longitude)
        self.assertEqual(34.7442398, coordinates.latitude)
