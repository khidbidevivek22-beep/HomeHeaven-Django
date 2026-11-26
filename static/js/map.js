(function () {
  'use strict';

  function initMap(element) {
    if (!element || typeof L === 'undefined' || element.dataset.ready === '1') return;
    element.dataset.ready = '1';

    const center = [
      parseFloat(element.dataset.lat || '18.5204'),
      parseFloat(element.dataset.lng || '73.8567')
    ];
    const map = L.map(element).setView(center, parseInt(element.dataset.zoom || '11', 10));

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map);

    let items = [];
    try { items = JSON.parse(element.dataset.items || '[]'); } catch (error) { items = []; }

    const markers = [];
    items.forEach(function (item) {
      const marker = L.marker([item.lat, item.lng]).addTo(map);
      marker.bindPopup(
        '<strong>' + item.title + '</strong><br>' + item.locality + ', ' + item.city +
        '<br><b>₹' + Number(item.rent).toLocaleString('en-IN') + '/month</b><br>' +
        '<a href="' + item.url + '">View details →</a>'
      );
      markers.push(marker);
    });

    if (markers.length > 1) {
      map.fitBounds(L.featureGroup(markers).getBounds(), { padding: [35, 35], maxZoom: 14 });
    }

    window.setTimeout(function () { map.invalidateSize(); }, 200);
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-map]').forEach(initMap);
  });
})();
