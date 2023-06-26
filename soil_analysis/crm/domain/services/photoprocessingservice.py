from haversine import haversine, Unit

from soil_analysis.crm.domain.valueobject.coordinates.capturelocationcoord import CaptureLocationCoord
from soil_analysis.crm.domain.valueobject.coordinates.landcoord import LandCoord


class PhotoProcessingService:
    @staticmethod
    def calculate_distance(coord1: CaptureLocationCoord, coord2: LandCoord, unit: str = Unit.METERS) -> float:
        """
        他の座標との距離を計算します。
        xarvio は 経度緯度(lng,lat) をエクスポートする
        haversineライブラリは 緯度経度(lat,lng) を2セット受け入れて距離を測る
        そのため、haversineライブラリを使うタイミングでタプルを逆にしている

        :param coord1: 座標1
        :param coord2: 座標2
        :param unit: 距離の単位（'km'、'miles'、'm'など）
        :return: 距離（単位に応じた値）
        """
        return haversine(
            coord1.to_googlemapcoord().get_coordinates(),
            coord2.to_googlemapcoord().get_coordinates(),
            unit=unit)
