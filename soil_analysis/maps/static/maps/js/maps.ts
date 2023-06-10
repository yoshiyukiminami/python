interface Location {
  lat: number;
  lng: number;
}
interface Pin {
  geometry: {
    location: Location;
  };
  name: string;
}
interface Pins {
  center: Location;
  formatted_pins: Pin[];
}

// values assigned in base.html
declare const locationPins: Pins;

function initMap(): void {
    const mapOptions = {
        center: new google.maps.LatLng(locationPins.center.lat, locationPins.center.lng),
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        keyboardShortcuts: false,
        streetViewControl: false,
        fullscreenControl: false,
        scrollwheel: false
    };

    try {
        const map = new google.maps.Map(document.getElementById("map_canvas") as HTMLElement, mapOptions);
        addPinsToMap(map, locationPins.formatted_pins);
        addPinsToMapPolygon(map, locationPins.formatted_pins);
    } catch (error) {
        console.error('JSON parsing error:', error);
    }
}

function addPinsToMap(map: google.maps.Map, pins: Pin[]): void {
  pins.forEach((pin) => {
      const location: Location = pin.geometry.location;
      const latLng = new google.maps.LatLng(location.lat, location.lng);
      new google.maps.Marker({
          position: latLng,
          map: map,
          title: pin.name
      });
  });
}

function addPinsToMapPolygon(map: google.maps.Map, pins: Pin[]): void {
  const coords: google.maps.LatLngLiteral[] = [];

  pins.forEach((pin) => {
    const location = pin.geometry.location;
    coords.push({ lat: location.lat, lng: location.lng });
  });

  const polygon = new google.maps.Polygon({
    paths: coords,
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.35,
  });

  polygon.setMap(map);
}

// this is googlemap's callback
function mapLoaded(): void {
    initMap();
}
