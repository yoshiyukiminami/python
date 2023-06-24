from haversine import haversine, Unit

from soil_analysis.crm.domain.valueobject.coordinates import Coordinates


class PhotoProcessingService:
    @staticmethod
    def calculate_distance(coord1: Coordinates, coord2: Coordinates, unit: str = Unit.METERS) -> float:
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
        return haversine(coord1.get_lat_lng(), coord2.get_lat_lng(), unit=unit)
