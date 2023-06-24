from unittest import TestCase

from soil_analysis.crm.domain.services.photoprocessingservice import PhotoProcessingService
from soil_analysis.crm.domain.valueobject.coordinates import Coordinates


class TestPhotoProcessingService(TestCase):
    def test_calculate_distance(self):
        coord1 = Coordinates("137.6492809,34.743865")  # ススムA3
        coord2 = Coordinates("137.6487935,34.744671")  # ススムA3から100mの場所
        expected_distance = 100.0  # 期待される距離（100メートル）

        distance = PhotoProcessingService.calculate_distance(coord1, coord2)
        self.assertAlmostEqual(expected_distance, distance, delta=0.1)  # 許容誤差を指定

    def test_calculate_midpoint(self):
        coord1 = Coordinates("137.6492809,34.743865")  # ススムA3
        coord2 = Coordinates("137.6487935,34.744671")  # ススムA3から100mの場所
        expected_coordinates = Coordinates("137.649039918463,34.744296001971506")   # 期待される距離（50メートル）

        midpoint = PhotoProcessingService.calculate_midpoint(coord1, coord2)
        self.assertAlmostEqual(expected_coordinates.longitude, midpoint.longitude, delta=0.1)  # 許容誤差を指定
        self.assertAlmostEqual(expected_coordinates.latitude, midpoint.latitude, delta=0.1)  # 許容誤差を指定
