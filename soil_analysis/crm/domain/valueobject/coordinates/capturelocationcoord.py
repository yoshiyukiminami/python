from typing import Tuple

from soil_analysis.crm.domain.valueobject.coordinates.coordinates import Coordinates
from soil_analysis.crm.domain.valueobject.coordinates.googlemapcoord import GoogleMapCoord


class CaptureLocationCoord(Coordinates):
    def __init__(self, longitude: float, latitude: float):
        """
        撮影座標 は 経度緯度(lng, lat) で作成する
        """
        self.longitude = longitude
        self.latitude = latitude

    def get_coordinates(self) -> Tuple[float, float]:
        """
        :return: longitude, latitude
        """
        return self.longitude, self.latitude

    def to_googlemapcoord(self) -> GoogleMapCoord:
        return GoogleMapCoord(self.latitude, self.longitude)
