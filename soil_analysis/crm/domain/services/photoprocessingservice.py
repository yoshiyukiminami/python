from haversine import haversine, Unit

from soil_analysis.crm.domain.valueobject.capturelocation import CaptureLocation
from soil_analysis.crm.domain.valueobject.coords.capturelocationcoords import CaptureLocationCoords
from soil_analysis.crm.domain.valueobject.coords.landcoords import LandCoords
from soil_analysis.crm.domain.valueobject.land import Land
from soil_analysis.crm.domain.valueobject.landcandidates import LandCandidates


class PhotoProcessingService:
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
