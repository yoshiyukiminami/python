function initMap() {
    var mapOptions = {
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
        var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        addPinsToMap(map, locationPins.formatted_pins);
        addPinsToMapPolygon(map, locationPins.formatted_pins);
    }
    catch (error) {
        console.error('JSON parsing error:', error);
    }
}
function addPinsToMap(map, pins) {
    pins.forEach(function (pin) {
        var location = pin.geometry.location;
        var latLng = new google.maps.LatLng(location.lat, location.lng);
        new google.maps.Marker({
            position: latLng,
            map: map,
            title: pin.name
        });
    });
}
function addPinsToMapPolygon(map, pins) {
    var coords = [];
    pins.forEach(function (pin) {
        var location = pin.geometry.location;
        coords.push({ lat: location.lat, lng: location.lng });
    });
    var polygon = new google.maps.Polygon({
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
function mapLoaded() {
    initMap();
}
