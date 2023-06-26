from unittest import TestCase

from soil_analysis.crm.domain.valueobject.coordinates.capturelocationcoord import CaptureLocationCoord
from soil_analysis.crm.domain.valueobject.coordinates.googlemapcoord import GoogleMapCoord
from soil_analysis.crm.domain.valueobject.coordinates.xarviocoord import XarvioCoord


class TestCoordinates(TestCase):
    def test_xarvio_coord_get_coordinates(self):
        coordinates_str = "137.6489657,34.7443565 137.6491266,34.744123"
        xarvio_coord = XarvioCoord(coordinates_str)
        self.assertEqual((137.6490462, 34.7442398), xarvio_coord.get_coordinates())

    def test_xarvio_coord_to_googlemapcoord(self):
        coordinates_str = "137.6489657,34.7443565 137.6491266,34.744123"
        xarvio_coord = XarvioCoord(coordinates_str)
        googlemap_coord = xarvio_coord.to_googlemapcoord()
        self.assertEqual((34.7442398, 137.6490462), googlemap_coord.get_coordinates())

    def test_googlemap_coord_get_coordinates(self):
        googlemap_coord = GoogleMapCoord(34.7443565, 137.6489657)
        self.assertEqual((34.7443565, 137.6489657), googlemap_coord.get_coordinates())

    def test_capturelocation_coord_get_coordinates(self):
        capturelocation_coord = CaptureLocationCoord(34.7443565, 137.6489657)
        self.assertEqual((34.7443565, 137.6489657), capturelocation_coord.get_coordinates())
