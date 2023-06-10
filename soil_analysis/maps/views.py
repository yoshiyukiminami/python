import json

from django.views.generic import TemplateView

from .domain.value_object.location import Location
from .models import PinCollection


class HomeView(TemplateView):
    TOKYO_TOWER_COORDINATES = "35.65861,139.745447"
    DISPLAY_RADIUS = 1500

    template_name = 'maps/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pins = PinCollection.objects.all()
        center_location = self.calculate_center_location(pins)

        formatted_pins = []
        for pin in pins:
            location = Location(pin.latlng)
            formatted_pins.append({
                "geometry": location.formatted_geometry(),
                "radius": HomeView.DISPLAY_RADIUS,
                "shop_name": pin.name,
                "place_id": pin.place_id
            })

        location_pins = {
            "center": center_location.formatted_center(),
            "formatted_pins": formatted_pins
        }
        context['location_pins'] = json.dumps(location_pins, ensure_ascii=False)

        return context

    @staticmethod
    def calculate_center_location(pins):
        lat_sum = 0.0
        lng_sum = 0.0
        count = 0

        for pin in pins:
            location = Location(pin.latlng)
            lat, lng = location.parse_value(pin.latlng)
            lat_sum += lat
            lng_sum += lng
            count += 1

        try:
            avg_lat = lat_sum / count
            avg_lng = lng_sum / count
            center_location = Location(f"{avg_lat},{avg_lng}")
        except ZeroDivisionError:
            # Use Tokyo Tower coordinates as default when there are no pins
            center_location = Location(HomeView.TOKYO_TOWER_COORDINATES)

        return center_location
