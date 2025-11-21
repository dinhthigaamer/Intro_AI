import networkx as nx
from pathlib import Path
from file_path import MAP_DIR
import insert_point

target_path = MAP_DIR / "graph.graphml"


def check_point_exist(G, x, y):
    # Kiểm tra đỉnh có nằm trong dataset ko, chưa có thì thêm vào tập
    for n, d in G.nodes(data=True):
        if d['x'] == x and d['y'] == y:
            return True
    return False


def update_weight_path(G, path, new_weight):
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if G.has_edge(u, v):
            G[u][v]["weight"] = new_weight
        else:
            raise ("Không tồn tại cạnh:", u, "->", v)

    nx.write_graphml(G, "output.graphml")


def update_weight(xu, yu, xv, yv, new_weight=1):
    # Cập nhật trọng số cho đường đi giữa 2 đỉnh
    # xu, yu, xv, yv là toạ độ của điểm đầu vào cuối
    # new_weight là trọng số mới cần cập nhật

    G = nx.read_graphml(target_path)
    # Kiểm tra xem đỉnh đã tồn tai chưa
    if check_point_exist(G, xu, yu) == False:
        insert_point.insert_point(MAP_DIR / "lmao")

    if check_point_exist(G, xv, yv) == False:
        insert_point.insert_point(MAP_DIR / "lmao")

    # Lấy danh sách đường đi ngắn nhất từ u->v
    # Cái này đợi Minh
    path = shortest_path_func(xu, yu, xv, yv)

    update_weight_path(G, path, new_weight)
