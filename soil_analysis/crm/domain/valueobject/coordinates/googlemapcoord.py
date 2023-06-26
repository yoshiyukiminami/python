from typing import Tuple

from soil_analysis.crm.domain.valueobject.coordinates.coordinates import Coordinates


class GoogleMapCoord(Coordinates):
    def __init__(self, latitude: float, longitude: float):
        """
        googlemap は 緯度経度(lat, lng) で作成する
        """
        self.latitude = latitude
        self.longitude = longitude

    def get_coordinates(self) -> Tuple[float, float]:
        """
        :return: latitude, longitude
        """
        return self.latitude, self.longitude
