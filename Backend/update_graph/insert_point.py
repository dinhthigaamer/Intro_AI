import networkx as nx
from file_path import MAP_DIR
import math
from math import sin, radians, atan2, cos, sqrt

cnt = 0


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2-x1, y2-y1)


def parse_linestring(ls_str: str):
    """Chuyển LINESTRING string -> list[(x,y)]"""
    ls_str = ls_str.replace("LINESTRING (", "").replace(")", "")
    return [tuple(map(float, p.strip().split())) for p in ls_str.split(",")]


def is_point_on_edge(px: float, py: float, x1: float, y1: float, x2: float, y2: float, tol=1e-6) -> bool:
    """
    Kiểm tra điểm (px, py) có nằm trên đoạn (x1,y1)-(x2,y2) không
    tol: sai số cho phép
    """
    # vector AB
    dx, dy = x2 - x1, y2 - y1
    # vector AP
    dx1, dy1 = px - x1, py - y1
    # tính t
    if dx == dy == 0:  # đoạn dài 0
        return math.isclose(px, x1, abs_tol=tol) and math.isclose(py, y1, abs_tol=tol)
    t = (dx*dx1 + dy*dy1) / (dx*dx + dy*dy)
    if t < 0 or t > 1:
        return False
    nearest_x = x1 + t*dx
    nearest_y = y1 + t*dy
    dist = math.hypot(px - nearest_x, py - nearest_y)
    return dist <= tol


def is_point_on_linestring(px: float, py: float, linestring: list, tol=1e-6) -> bool:
    """
    linestring: [(x1,y1), (x2,y2), ..., (xn,yn)]
    """
    for i in range(len(linestring)-1):
        x1, y1 = linestring[i]
        x2, y2 = linestring[i+1]
        if is_point_on_edge(px, py, x1, y1, x2, y2, tol):
            return True, i
    return False, -1


def compute_linestring_weight(linestring_coords):
    """
    Tính độ dài thật (mét) của đoạn đường biểu diễn bằng list tọa độ [(lon, lat), (lon, lat), ...].
    Không cần split point.
    """

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # bán kính Trái Đất (m)
        phi1, phi2 = radians(lat1), radians(lat2)
        dphi = radians(lat2 - lat1)
        dlambda = radians(lon2 - lon1)
        a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
        return 2 * R * atan2(sqrt(a), sqrt(1 - a))

    total_length = 0.0
    for i in range(len(linestring_coords) - 1):
        lon1, lat1 = linestring_coords[i]
        lon2, lat2 = linestring_coords[i + 1]
        total_length += haversine(lat1, lon1, lat2, lon2)

    return total_length


def insert_point(name_file: str, xw: float, yw: float):
    G = nx.read_graphml(MAP_DIR / name_file)
    if G == None:
        print("graph not found !")
        return

    pos = {}

    for n, d in G.nodes(data=True):
        # Đảm bảo node có cả d4, d5
        pos[n] = (float(d['x']), float(d['y']))  # lon, lat

    global cnt
    # thêm đỉnh vào graph
    node_id = "newnode" + str(cnt)
    cnt += 1
    G.add_node(node_id, d5=xw, d4=yw)

    for u, v, data in G.edges(data=True):
        if 'LINESTRING' in data:
            linestring = parse_linestring(data['LINESTRING'])
        else:
            linestring = [pos[u], pos[v]]

        ok, idx = is_point_on_linestring(xw, yw, linestring)
        if (ok == False):
            continue

        linestring1 = linestring[:idx+1] + [(xw, yw)]
        linestring2 = [(xw, yw)] + linestring[idx+1:]

        w1 = compute_linestring_weight(linestring1)
        w2 = compute_linestring_weight(linestring2)

        G.add_edge(u, node_id, d14=w1,
                   d15=f"LINESTRING ({', '.join(f'{x} {y}' for x, y in linestring1)})")
        G.add_edge(node_id, v, d14=w2,
                   d15=f"LINESTRING ({', '.join(f'{x} {y}' for x, y in linestring2)})")

    nx.write_graphml(G, MAP_DIR / "graph_updated.graphml")


insert_point("graph.graphml", 36, 36)
