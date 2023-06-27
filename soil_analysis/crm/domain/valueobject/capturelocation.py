import math

from soil_analysis.crm.domain.valueobject.coordinates.capturelocationcoord import CaptureLocationCoord


class CaptureLocation:
    """
    Note: 右に圃場１、左に圃場2がある状態で、それら圃場を手前から、かつ圃場の左右の真ん中から撮影したとき、撮影座標との距離の関係性は二等辺三角形になる
      それでは圃場が特定できないので、撮影した方位角（例えば圃場２）に向かって撮影座標を10m補正できれば、圃場１からは少し遠くなり、圃場２へは少し近くなる
      そんな下準備をして find_nearest_land で処理できれば、写真から圃場を特定できる
    """
    def __init__(self, longitude, latitude, azimuth):
        self._coordinates_origin = CaptureLocationCoord(longitude, latitude)
        self._coordinates = self._move(azimuth)

    def _move(self, azimuth: float, distance: float = 0.01):
        """
        緯度・経度座標を基に、指定された方位角と距離で移動した座標を計算します。

        :param azimuth: 方位角（単位: 度）
        :param distance: 移動距離（単位: キロメートル）
        :return: 移動後の座標を表す Coordinates オブジェクト
        """
        origin_longitude, origin_latitude = self._coordinates_origin.get_coordinates()

        # 角度をラジアンに変換
        azimuth_rad = math.radians(azimuth)
        # 緯度をラジアンに変換
        latitude_rad = math.radians(origin_latitude)
        # 赤道半径（地球の半径）を設定
        radius = 6371.0  # 地球の半径（キロメートル）

        # 目的地までの変位の緯度変化を計算
        delta_latitude = distance / radius * math.cos(azimuth_rad)
        # 目的地までの変位の経度変化を計算
        delta_longitude = distance / (radius * math.sin(latitude_rad)) * math.sin(azimuth_rad)

        # 目的地の緯度を計算
        destination_latitude = origin_latitude + math.degrees(delta_latitude)
        # 目的地の経度を計算
        destination_longitude = origin_longitude + math.degrees(delta_longitude)

        return CaptureLocationCoord(destination_longitude, destination_latitude)

    @property
    def corrected(self):
        return self._coordinates

    @property
    def origin(self):
        return self._coordinates_origin
