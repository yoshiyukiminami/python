from unittest import TestCase

from soil_analysis.crm.domain.valueobject.coordinates.landcoord import LandCoord
from soil_analysis.crm.domain.valueobject.land import Land


class TestLand(TestCase):
    def test_land_initialization(self):
        name = "ススムA3"
        coordinates_str = "137.6492809,34.743865 137.6494646,34.7436029 137.6489644,34.7433683 " \
                          "137.6487806,34.7436403 137.6492809,34.743865"

        # ススムA3の中心点をgooglemapで手動で手に入れた
        expected_coordinates = LandCoord("137.6491060553256,34.74361968398954")

        land = Land(name, coordinates_str)

        self.assertEqual(name, land.name)
        self.assertAlmostEqual(expected_coordinates.latitude, land.center.latitude, delta=0.0001)
        self.assertAlmostEqual(expected_coordinates.longitude, land.center.longitude, delta=0.0001)
