from fastkml import kml

from soil_analysis.crm.domain.valueobject.land import Land
from soil_analysis.crm.domain.valueobject.landcandidates import LandCandidates


class LandCandidateService:
    KML_DOCUMENT = 0
    KML_POLYGON = 0
    KML_LNG = 0
    KML_LAT = 1

    def parse_kml(self, kml_str):
        """
        KML形式の文字列を解析してLandCandidatesオブジェクトを作成します。

        Args:
            kml_str (str): KML形式の文字列データ。

        Returns:
            LandCandidates: 解析されたLandCandidatesオブジェクト。

        Raises:
            ValueError: 不正なKML形式の文字列が指定された場合に発生します。
        """
        land_candidates = LandCandidates()

        try:
            kml_doc = kml.KML()
            kml_doc.from_string(kml_str)
            kml_document = list(kml_doc.features())[self.KML_DOCUMENT]

            for placemark in kml_document.features():
                placemark_object = placemark.geometry
                name = placemark.name
                coordinates_str = self._convert_coordinates_str(placemark_object.geoms[self.KML_POLYGON].exterior.coords)
                land_candidate = Land(name, coordinates_str)
                land_candidates.add(land_candidate)

            return land_candidates
        except ValueError as e:
            raise ValueError("Invalid KML format") from e

    def _convert_coordinates_str(self, coords):
        """
        座標のリストを文字列表現に変換します。

        Args:
            coords (list): 座標のリスト。各座標はタプルとして表されます。

        Returns:
            str: 座標の文字列表現。
        """
        return ' '.join([f"{coord[self.KML_LNG]},{coord[self.KML_LAT]}" for coord in coords])
