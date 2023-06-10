function initMap() {
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
        const map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        addPinsToMap(map, locationPins.formatted_pins);
    } catch (error) {
        console.error('JSON parsing error:', error);
    }
}

function addPinsToMap(map, pins) {
    if (pins && Array.isArray(pins)) {
        let location_lat;
        let location_lng;
        pins.forEach(function (pin) {
            location_lat = pin.geometry.location.lat;
            location_lng = pin.geometry.location.lng;
            const latLng = new google.maps.LatLng(location_lat, location_lng);
            new google.maps.Marker({
                position: latLng,
                map: map,
                title: pin.name
            });
        });
    }
}

function mapLoaded() {
    initMap();
}
