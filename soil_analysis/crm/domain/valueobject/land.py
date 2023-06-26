from soil_analysis.crm.domain.valueobject.coordinates.landcoord import LandCoord


class Land:
    def __init__(self, name, coordinates_str):
        self.name = name
        self.center = LandCoord(coordinates_str)
