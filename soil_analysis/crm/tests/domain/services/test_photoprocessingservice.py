from unittest import TestCase

from soil_analysis.crm.domain.services.photoprocessingservice import PhotoProcessingService
from soil_analysis.crm.domain.valueobject.coordinates.capturelocationcoord import CaptureLocationCoord
from soil_analysis.crm.domain.valueobject.coordinates.landcoord import LandCoord


class TestPhotoProcessingService(TestCase):
    def test_calculate_distance(self):
        coord1 = CaptureLocationCoord(137.6492809, 34.743865)  # ススムA3撮影座標
        coord2 = LandCoord("137.6487935,34.744671")  # ススムA3撮影座標から100mの場所（Landで代用）
        expected_distance = 100.0  # 期待される距離（100メートル）

        distance = PhotoProcessingService.calculate_distance(coord1, coord2)
        self.assertAlmostEqual(expected_distance, distance, delta=0.1)  # 許容誤差を指定
