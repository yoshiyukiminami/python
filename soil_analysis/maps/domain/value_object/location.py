class Location:
    def __init__(self, value):
        self.lat, self.lng = self.parse_value(value)

    @staticmethod
    def parse_value(value):
        return [float(coord) for coord in value.split(',')]

    def formatted_geometry(self):
        return {
            "location": {
                "lat": self.lat,
                "lng": self.lng
            }
        }

    def formatted_center(self):
        return {
            "lat": self.lat,
            "lng": self.lng
        }
