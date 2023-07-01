from haversine import haversine, Unit

from soil_analysis.crm.domain.valueobject.capturelocation import CaptureLocation
from soil_analysis.crm.domain.valueobject.coords.capturelocationcoords import CaptureLocationCoords
from soil_analysis.crm.domain.valueobject.coords.landcoords import LandCoords
from soil_analysis.crm.domain.valueobject.land import Land
from soil_analysis.crm.domain.valueobject.landcandidates import LandCandidates


class PhotoProcessingService:
    def find_nearest_land(self, photo_coords: CaptureLocation, kml_land_candidates: LandCandidates) -> Land:
        """
        n個圃場の距離をそれぞれ調べていちばん距離の近い圃場を特定します
        :param photo_coords:
        :param kml_land_candidates:
        :return:
        """
        min_distance = float('inf')
        nearest_land = None

        for land in kml_land_candidates.list():
            distance = self.calculate_distance(photo_coords.corrected, land.center)
            if distance < min_distance:
                min_distance = distance
                nearest_land = land

        return nearest_land

    @staticmethod
    def calculate_distance(coords1: CaptureLocationCoords, coords2: LandCoords, unit: str = Unit.METERS) -> float:
        """
        他の座標との距離を計算します。
        xarvio は 経度緯度(lng,lat) をエクスポートする
        haversineライブラリは 緯度経度(lat,lng) を2セット受け入れて距離を測る
        そのため、haversineライブラリを使うタイミングでタプルを逆にしている

        :param coords1: 座標1
        :param coords2: 座標2
        :param unit: 距離の単位（'km'、'miles'、'm'など）
        :return: 距離（単位に応じた値）
        """
        return haversine(
            coords1.to_googlemapcoords().get_coords(),
            coords2.to_googlemapcoords().get_coords(),
            unit=unit)
