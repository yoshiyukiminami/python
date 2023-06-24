from typing import Tuple


class Coordinates:
    def __init__(self, coordinates_str: str):
        """
        xarvio は 経度緯度(lng,lat) を4以上のタプルをspaceで区切ってエクスポートするのでxarvioベースで作成する
        検証で googlemap を検索するときは 緯度経度(lat,lng) で検索しないといけない
        See Also: https://developers.google.com/kml/documentation/kmlreference?hl=ja#coordinates
        """
        coordinates = coordinates_str.split()
        coordinates = list(set(coordinates))  # 始点と終点の座標が一致するため、重複を排除する
        self.latitude_sum = 0.0
        self.longitude_sum = 0.0
        self.num_points = len(coordinates)
        for coordinate in coordinates:
            lng, lat = coordinate.split(',')
            self.longitude_sum += float(lng)
            self.latitude_sum += float(lat)
        self.longitude = round(self.longitude_sum / self.num_points, 7)
        self.latitude = round(self.latitude_sum / self.num_points, 7)

    def get_lng_lat(self) -> Tuple[float, float]:
        return self.longitude, self.latitude

    def get_lat_lng(self) -> Tuple[float, float]:
        return self.latitude, self.longitude
