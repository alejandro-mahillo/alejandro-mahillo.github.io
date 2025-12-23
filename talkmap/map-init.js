/* talkmap/map-init.js */

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Verificación de seguridad
    if (typeof addressPoints === 'undefined') {
        console.error("ERROR: No se encontró 'addressPoints'.");
        return;
    }

    // 2. CAMBIO CLAVE: Usamos 'CartoDB Positron' en lugar de OpenStreetMap.
    // Es mucho más limpio, elegante para webs académicas y disimula mejor la carga.
    var tiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    });

    var latlng = L.latLng(30, 10);
    
    var map = L.map('map', {
        center: latlng, 
        zoom: 2, 
        layers: [tiles],
        scrollWheelZoom: true, // AHORA SÍ: Permitimos zoom con la rueda/trackpad
        zoomControl: true
    });

    // 3. Hack para el "Shift + Scroll" (Zoom manual simple)
    // Leaflet por defecto no trae esto, así que si quieres ESTRICTAMENTE
    // que solo funcione con Shift, usa este bloque y pon scrollWheelZoom: false arriba.
    /*
    document.getElementById('map').addEventListener('wheel', function(event) {
        if (event.shiftKey) {
            event.preventDefault(); // Evita que la página baje
            if (event.deltaY < 0) map.zoomIn();
            else map.zoomOut();
        }
    });
    */
    // MI RECOMENDACIÓN: Deja scrollWheelZoom: true y borra este bloque comentado.
    // Es mucho más suave y natural para el usuario.

    // 4. Clusters
    var markers = L.markerClusterGroup({
        showCoverageOnHover: false,
        maxClusterRadius: 80
    });

    for (var i = 0; i < addressPoints.length; i++) {
        var a = addressPoints[i];
        var title = a[0];
        var lat = a[1];
        var lon = a[2];
        
        var marker = L.marker(new L.LatLng(lat, lon), { title: title });
        marker.bindPopup(title);
        markers.addLayer(marker);
    }

    map.addLayer(markers);
    
    // 5. Renderizado
    setTimeout(function(){ map.invalidateSize(); }, 200);
});