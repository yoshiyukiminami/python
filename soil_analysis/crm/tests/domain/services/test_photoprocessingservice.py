from unittest import TestCase

from soil_analysis.crm.domain.services.photoprocessingservice import PhotoProcessingService
from soil_analysis.crm.domain.valueobject.coords.capturelocationcoords import CaptureLocationCoords
from soil_analysis.crm.domain.valueobject.coords.landcoords import LandCoords


class TestPhotoProcessingService(TestCase):
    def test_calculate_distance(self):
        coords1 = CaptureLocationCoords(137.6492809, 34.743865)  # ススムA3撮影座標
        coords2 = LandCoords("137.6487935,34.744671")  # ススムA3撮影座標から100mの場所（Landで代用）
        expected_distance = 100.0  # 期待される距離（100メートル）

        distance = PhotoProcessingService.calculate_distance(coords1, coords2)
        self.assertAlmostEqual(expected_distance, distance, delta=0.1)  # 許容誤差を指定
