
document.addEventListener('DOMContentLoaded', async () => {
  // Khởi tạo bản đồ
  const map = L.map('map').setView([21.016, 105.812], 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

  let originMarker, destMarker;
  let selectedSegment = null;
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
        const coords = way.nodes.map(id => nodes[id]);
        L.polygon(coords, {
          color: 'red',
          weight: 2,
          fillColor: 'red',
          fillOpacity: 0.1
        }).addTo(map);
      });
    } catch (err) {
      console.error("Boundary load error:", err);
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
        if (originMarker) originMarker.remove();
        originMarker = L.marker([data[0].lat, data[0].lon])
          .addTo(map).bindPopup("Điểm đi").openPopup();
        map.setView([data[0].lat, data[0].lon], 15);
      }
    }

    if (destQuery) {
      const data = await searchPlace(destQuery);
      if (data[0]) {
        if (destMarker) destMarker.remove();
        destMarker = L.marker([data[0].lat, data[0].lon])
          .addTo(map).bindPopup("Điểm đến").openPopup();
        map.setView([data[0].lat, data[0].lon], 15);
      }
    }
  };
  let picking = 'origin';
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
  document.getElementById('update-segment').onclick = () => {
    if (!selectedSegment) return alert("Chọn đoạn đường");
    const status = document.getElementById('segment-status').value;
    const weight = document.getElementById('segment-weight').value;
    selectedSegment._status=status;
    selectedSegment._weight=weight;
    selectedSegment.setStyle({color: status==="jam"?"red":"green"});
    alert("Đã cập nhật đoạn "+selectedSegment._id);
  };
});
