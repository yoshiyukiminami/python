interface LocationPins {
  center: {
    lat: number;
    lng: number;
  };
  formatted_pins: any[];
}
interface Location {
  lat: number;
  lng: number;
}

// values assigned in base.html
declare const locationPins: LocationPins;

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
    } catch (error) {
        console.error('JSON parsing error:', error);
    }
}

function addPinsToMap(map: google.maps.Map, pins: any[]): void {
    if (pins && Array.isArray(pins)) {
        pins.forEach(function (pin) {
            const location: Location = pin.geometry.location;
            const latLng = new google.maps.LatLng(location.lat, location.lng);
            new google.maps.Marker({
                position: latLng,
                map: map,
                title: pin.name
            });
        });
    }
}

// function addPinsToMapPolygon(map: HTMLElement, pins: any[]): void {
//   const bermudaTriangle = new google.maps.Polygon({
//     paths: triangleCoords,
//     strokeColor: "#FF0000",
//     strokeOpacity: 0.8,
//     strokeWeight: 2,
//     fillColor: "#FF0000",
//     fillOpacity: 0.35,
//   });
//
//   bermudaTriangle.setMap(map);
// }

// this is googlemap's callback
function mapLoaded(): void {
    initMap();
}
