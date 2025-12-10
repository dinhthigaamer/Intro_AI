import astar  # isort:skip
from graph_loader import MapLoader
import os
import sys
# import insert_point
# from file_path import MAP_DIR
from pathlib import Path
import networkx as nx
import osmnx as ox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

target_path = "../map_data/phuong_lang.graphml"
MAP_PATH = {
    "car": "../map_data/phuong_lang_drive.graphml",
    "bike": "../map_data/phuong_lang_bike.graphml",
    "walk": "../map_data/phuong_lang_walk.graphml",
    "motorcycle": "../map_data/phuong_lang_drive.graphml",
}


def check_point_exist(G, x, y):
    # Kiểm tra đỉnh có nằm trong dataset ko, chưa có thì thêm vào tập
    for n, d in G.nodes(data=True):
        if d['x'] == x and d['y'] == y:
            return True
    return False


def update_weight(path_graphml, start, goal, new_weight=1, vehicle=None):
    # Cập nhật trọng số cho đường đi giữa 2 đỉnh
    # xu, yu, xv, yv là toạ độ của điểm đầu vào cuối
    # new_weight là trọng số mới cần cập nhật
    # Lấy danh sách đường đi ngắn nhất từ u->v
    # Cái này đợi Minh
    try:
        if vehicle is not None:
            path, _ = astar.astar(path_graphml, start, goal,
                                  vehicle, use_weight_length=0)
        else:
            path, _ = astar.astar(
                path_graphml, start, goal, vehicle="car", use_weight_length=0)

        if path is None:
            return

        edges = list(zip(path[:-1], path[1:]))

        G = nx.read_graphml(target_path)
        G_drive = nx.read_graphml(MAP_PATH["car"])
        G_bike = nx.read_graphml(MAP_PATH["bike"])
        G_walk = nx.read_graphml(MAP_PATH["walk"])
        G_moto = nx.read_graphml(MAP_PATH["motorcycle"])
        G_vehical = nx.read_graphml(MAP_PATH[vehicle])

        graphs = [(G, target_path), (G_drive, MAP_PATH["car"]),
                  (G_bike, MAP_PATH["bike"]), (G_walk, MAP_PATH["walk"]),
                  (G_moto, MAP_PATH["motorcycle"])]

        for gr, _ in graphs:
            for key in list(gr.graph.keys()):
                if "default" in key:
                    del gr.graph[key]

        for a, b in edges:
            for k in G_vehical[a][b]:
                osmid = G_vehical[a][b][k]["osmid"]

                for gr, _ in graphs:
                    for s, t, d in gr.edges(data=True):
                        if (d["osmid"] == osmid):
                            d["weight"] = 1.0*new_weight

                        if isinstance(osmid, list) and isinstance(d["osmid"], list):
                            if all(hw in osmid for hw in d["osmid"]):
                                d["weight"] = 1.0*new_weight

        for gr, path in graphs:
            ox.save_graphml(gr, path)
        return {"state": "updated successfully"}
    except:
        raise


def update_weight_one_vehicle(path_graphml, start, goal, new_weight=1, vehicle=None):
    # Cập nhật trọng số cho đường đi giữa 2 đỉnh
    # xu, yu, xv, yv là toạ độ của điểm đầu vào cuối
    # new_weight là trọng số mới cần cập nhật
    # Lấy danh sách đường đi ngắn nhất từ u->v
    # Cái này đợi Minh
    try:
        if vehicle is not None:
            path, _ = astar.astar(path_graphml, start, goal,
                                  vehicle, use_weight_length=0)
        else:
            path, _ = astar.astar(
                path_graphml, start, goal, vehicle="car", use_weight_length=0)

        if path is None:
            return

        edges = list(zip(path[:-1], path[1:]))

        G_vehical = nx.read_graphml(MAP_PATH[vehicle])
        G = nx.read_graphml(target_path)
        graphs = [(G_vehical, MAP_PATH[vehicle]), (G, target_path)]

        for gr, _ in graphs:
            for key in list(gr.graph.keys()):
                if "default" in key:
                    del gr.graph[key]

        for a, b in edges:
            for k in G_vehical[a][b]:
                osmid = G_vehical[a][b][k]["osmid"]

                for gr, _ in graphs:
                    for s, t, d in gr.edges(data=True):
                        if (d["osmid"] == osmid):
                            d["weight"] = 1.0*new_weight

                        if isinstance(osmid, list) and isinstance(d["osmid"], list):
                            if all(hw in osmid for hw in d["osmid"]):
                                d["weight"] = 1.0*new_weight

        for gr, path in graphs:
            ox.save_graphml(gr, path)
        return {"state": "updated successfully"}
    except:
        raise

        # <edge source="5709996137" target="5709996140" id="0">
if __name__ == '__main__':
    update_weight("../map_data/weighted_graph.graphml",
                  "5709996137", "5709996124", 3, "car")
