MAP_PATH = "weighted_graph.graphml"
API = "http://127.0.0.1:8000"

document.addEventListener('DOMContentLoaded', async () => {
  const map = L.map('map').setView([21.016, 105.812], 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  let originMarker = null;
  let destMarker = null;
  let picking = 'origin';
  let myPolyline = null;
  let myPolyline1 = null;
  let myPolyline2 = null;

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
    // console.log(res)
    return res.json();
  }

  document.getElementById('find-route').onclick = async () => {
    const originQuery = document.getElementById('origin-input').value.trim();
    const destQuery = document.getElementById('dest-input').value.trim();

    const vehicle = document.getElementById('vehicle').value;

    let coords = []

    if (originQuery) {
      const data = await searchPlace(originQuery);
      if (data[0]) {
        const { lat, lon, display_name } = data[0];

        coords.push([Number(lat), Number(lon)])

        if (originMarker) originMarker.remove();
        originMarker = L.marker([lat, lon]).addTo(map).bindPopup("Điểm đi: " + display_name).openPopup();
        map.setView([lat, lon], 15);
      }
    }

    if (destQuery) {
      const data = await searchPlace(destQuery);
      if (data[0]) {
        const { lat, lon, display_name } = data[0];
        coords.push([Number(lat), Number(lon)])
        // destNode = await findNearestNode(lat, lon)

        if (destMarker) destMarker.remove();
        destMarker = L.marker([lat, lon]).addTo(map).bindPopup("Điểm đến: " + display_name).openPopup();
        map.setView([lat, lon], 15);
      }
    }

    // L.polyline(coords, {
    //   color: 'red',
    //   weight: 2,
    // }).addTo(map);

    const body = { "nodes": coords, "vehicle": vehicle }
    let res = null
    // Gọi API tìm đường
    if (coords.length >= 2) {
      res = await fetch(API + "/path", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      });
    }

    if (myPolyline != null)
      myPolyline.remove()
    if (myPolyline1 != null)
      myPolyline1.remove()
    if (myPolyline2 != null)
      myPolyline2.remove()

    console.log(body)

    const data = res ? await res.json() : null;

    if (data == null || data["state"] == "fail") {
      console.log(data)
      alert("Không tìm được đường đi phù hợp !")
    } else {
      // console.log(data["path"])
      path = data["path"]
      len = data["len"]

      if (path[0] != coords[0])
        myPolyline1 = L.polyline([coords[0], path[0]], {
          color: 'blue',
          dashArray: "6 6",
          weight: 2,
        }).addTo(map);

      if (path[path.length - 1] != coords[coords.length - 1])
        myPolyline2 = L.polyline([path[path.length - 1], coords[coords.length - 1]], {
          color: 'blue',
          dashArray: "6 6",
          weight: 2,
        }).addTo(map);

      myPolyline = L.polyline(path, {
        color: 'blue',
        weight: 2,
      }).addTo(map);

      alert("Tìm đc đường đi")
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
