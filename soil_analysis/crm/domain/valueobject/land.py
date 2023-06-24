from soil_analysis.crm.domain.valueobject.coordinates import Coordinates


class Land:
    def __init__(self, name, coordinates_str):
        self.name = name
        self.center = Coordinates(coordinates_str)
