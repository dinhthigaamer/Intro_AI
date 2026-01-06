import requests
import json

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def draw_boundary_phuong_lang():
    query = """
    [out:json];
    relation["boundary"="administrative"]["name"="Phường Láng"];
    (._;>;);
    out;
    """

    # 1. Gọi Overpass API
    res = requests.get(
        OVERPASS_URL,
        params={"data": query},
        timeout=60
    )
    res.raise_for_status()
    data = res.json()

    # 2. Map node_id -> [lat, lon]
    nodes = {
        el["id"]: [el["lat"], el["lon"]]
        for el in data["elements"]
        if el["type"] == "node"
    }

    boundaries = []

    # 3. Lấy các way → danh sách tọa độ
    for el in data["elements"]:
        if el["type"] == "way":
            coords = [
                nodes[node_id]
                for node_id in el["nodes"]
                if node_id in nodes
            ]

            if coords:
                boundaries.append(coords)

    # 4. GHI RA FILE JSON
    with open("phuong_lang_boundary.json", "w", encoding="utf-8") as f:
        json.dump(boundaries, f, ensure_ascii=False, indent=2)

    print("Saved phuong_lang_boundary.json")
    return boundaries


draw_boundary_phuong_lang()
