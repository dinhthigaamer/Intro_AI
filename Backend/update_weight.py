import astar  # isort:skip
from graph_loader import MapLoader
import os
import sys
# import insert_point
# from file_path import MAP_DIR
from pathlib import Path
import networkx as nx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

target_path = "../map_data/weighted_graph.graphml"
output_path = "../map_data/weighted_graph.graphml"


def check_point_exist(G, x, y):
    # Kiểm tra đỉnh có nằm trong dataset ko, chưa có thì thêm vào tập
    for n, d in G.nodes(data=True):
        if d['x'] == x and d['y'] == y:
            return True
    return False


def update_weight(start, goal, new_weight=1, vehicle=None):
    # Cập nhật trọng số cho đường đi giữa 2 đỉnh
    # xu, yu, xv, yv là toạ độ của điểm đầu vào cuối
    # new_weight là trọng số mới cần cập nhật

    mp = MapLoader(target_path)
    G = mp.get_graph()
    # # Kiểm tra xem đỉnh đã tồn tai chưa
    # if check_point_exist(G, xu, yu) == False:
    #     insert_point.insert_point(MAP_DIR / "lmao")

    # if check_point_exist(G, xv, yv) == False:
    #     insert_point.insert_point(MAP_DIR / "lmao")

    # Lấy danh sách đường đi ngắn nhất từ u->v
    # Cái này đợi Minh
    if vehicle is not None:
        path, len = astar.astar(G, start, goal, vehicle)
    else:
        path, len = astar.astar(G, start, goal)
    # print(path)

    if path is None:
        return

    edges = list(zip(path[:-1], path[1:]))

    G = nx.read_graphml(target_path)
    for a, b in edges:
        for k in G[a][b]:
            G[a][b][k]["weight"] = 1.0*new_weight

    nx.write_graphml(G, output_path)


# <edge source="5709996137" target="5709996140" id="0">
if __name__ == '__main__':
    update_weight("5709996137", "5709996124", 3)
