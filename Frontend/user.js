
document.addEventListener('DOMContentLoaded', async () => {
  const map = L.map('map').setView([21.016, 105.812], 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

  let originMarker = null;
  let destMarker = null;
  let picking = 'origin'; 
  async function drawBoundaryPhuongLang() {
    const query = `
      [out:json];
      relation["boundary"="administrative"]["name"="Phường Láng"];
      (._;>;);
      out;
    `;
    const url = "https://overpass-api.de/api/interpreter?data=" + encodeURIComponent(query);

    try {
      const res = await fetch(url);
      const data = await res.json();

      const nodes = {};
      data.elements.filter(el => el.type === "node").forEach(node => {
        nodes[node.id] = [node.lat, node.lon];
      });

      data.elements.filter(el => el.type === "way").forEach(way => {
        const coords = way.nodes.map(id => nodes[id]).filter(Boolean);
        if (coords.length > 0) {
          L.polygon(coords, {
            color: 'red',
            weight: 2,
            fillColor: 'red',
            fillOpacity: 0.1
          }).addTo(map);
        }
      });
    } catch (err) {
      console.error("Lỗi khi tải boundary phường Láng:", err);
    }
  }

  await drawBoundaryPhuongLang();
  async function searchPlace(query) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`;
    const res = await fetch(url);
    return res.json();
  }
  document.getElementById('find-route').onclick = async () => {
    const originQuery = document.getElementById('origin-input').value.trim();
    const destQuery = document.getElementById('dest-input').value.trim();

    if (originQuery) {
      const data = await searchPlace(originQuery);
      if (data[0]) {
        const { lat, lon, display_name } = data[0];
        if (originMarker) originMarker.remove();
        originMarker = L.marker([lat, lon]).addTo(map).bindPopup("Điểm đi: " + display_name).openPopup();
        map.setView([lat, lon], 15);
      }
    }

    if (destQuery) {
      const data = await searchPlace(destQuery);
      if (data[0]) {
        const { lat, lon, display_name } = data[0];
        if (destMarker) destMarker.remove();
        destMarker = L.marker([lat, lon]).addTo(map).bindPopup("Điểm đến: " + display_name).openPopup();
        map.setView([lat, lon], 15);
      }
    }
  };
  map.on('click', e => {
    const { lat, lng } = e.latlng;
    if (picking === 'origin') {
      if (originMarker) originMarker.remove();
      originMarker = L.marker([lat, lng]).addTo(map).bindPopup("Điểm đi").openPopup();
      picking = 'dest';
    } else {
      if (destMarker) destMarker.remove();
      destMarker = L.marker([lat, lng]).addTo(map).bindPopup("Điểm đến").openPopup();
      picking = 'origin';
    }
  });
});
