(() => {
  const container = document.getElementById('map-container');
  const status = document.getElementById('map-status');
  const locations = document.getElementById('talk-map-locations').content.querySelectorAll('[data-location]');
  const leaflet = window.L;

  if (!locations.length || !leaflet?.markerClusterGroup) {
    container.hidden = true;
    status.textContent = 'The interactive map is unavailable. The full list of talks is below.';
    return;
  }

  const map = leaflet.map('map').setView([30, 10], 2);
  const tiles = leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  });

  let hasLoadedTile = false;
  tiles.on('tileload', () => {
    if (hasLoadedTile) return;
    hasLoadedTile = true;
    status.textContent = '';
  });
  tiles.on('load', () => {
    if (!hasLoadedTile) {
      status.textContent = 'The map background could not load. You can still use the markers or read the full list below.';
    }
  });
  tiles.addTo(map);

  const markers = leaflet.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 80 });
  for (const location of locations) {
    const { location: name, lat, lng } = location.dataset;
    const marker = leaflet.marker([Number(lat), Number(lng)], { title: name, alt: name });
    marker.bindPopup(location.cloneNode(true), { maxWidth: 250 });
    markers.addLayer(marker);
  }
  markers.addTo(map);
})();
