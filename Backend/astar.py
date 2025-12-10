import networkx as nx
import heapq
from math import radians, sin, cos, sqrt, atan2


def astar(path_graphml, start, goal, vehicle="car", use_weight_length=1):
    # ------------------- Load và chuẩn hóa map -------------------
    G = nx.read_graphml(path_graphml)
    G = nx.relabel_nodes(G, str)  # ép node IDs sang string

    # Node: ép x, y sang float
    for n, data in G.nodes(data=True):
        if "x" in data:
            try:
                data["x"] = float(data["x"])
            except:
                pass

        if "y" in data:
            try:
                data["y"] = float(data["y"])
            except:
                pass

    # Edge: chuẩn hóa các thuộc tính cần thiết
    for u, v, data in G.edges(data=True):
        # chiều dài
        if "length" in data:
            try:
                data["length"] = float(data["length"])
            except:
                data["length"] = 1.0
        else:
            data["length"] = 1.0

        # trọng số
        if "weight" in data:
            try:
                data["weight"] = float(data["weight"])
            except:
                data["weight"] = 1.0
        else:
            data["weight"] = 1.0

        # thêm thuộc tính mới là chi phí = weight * length
        data["weight_length"] = data["weight"] * data["length"]

        # Trường hợp cạnh bị cấm
        if data["weight"] == 9999:
            data["weight_length"] = -1

        # độ rộng
        if "width" in data:
            try:
                data["width"] = float(data["width"])
            except:
                data["width"] = 3.0
        else:
            data["width"] = 3.0

        # data xử lý cho ràng buộc phương tiện
        data["highway"] = str(data.get("highway", "")).lower()
        data["access"] = str(data.get("access", "")).lower()

        # data xử lý cho hướng xe được đi
        one = str(data.get("oneway", "false")).lower()
        data["oneway"] = one in ("yes", "true", "1")

        rev = str(data.get("reversed", "false")).lower()
        data["reversed"] = rev in ("yes", "true", "1")

    # ------------------- Luật chiều hợp lệ -------------------
    def allow_direction(current, neighbor, edge):
        oneway = edge["oneway"]
        reversed_dir = edge["reversed"]

        # đường không phải 1 chiều → OK
        if not oneway:
            return True

        # nếu là đường 1 chiều
        # reversed=True nghĩa là hướng này là "ngược"
        if reversed_dir:
            return False

        # Còn lại là chiều đúng
        return True

    # ------------------- Ràng buộc phương tiện -------------------
    def allow_vehicle(edge):
        hwy = edge.get("highway", "")
        acc = edge.get("access")  # có thể None
        width = edge.get("width")  # có thể None

        # nếu trong data cạnh k có thuộc tính access thì hiểu là nhận giá trị "permit"
        if acc is None or acc == "":
            acc = "permit"

        # ----- CAR -----
        if vehicle == "car":
            if hwy == "footway":
                return False

            if acc == "no":
                return False

            if width is not None and width < 2.5:
                return False

            return True

        # ----- MOTORCYCLE -----
        if vehicle == "motorcycle":
            if hwy == "footway":
                return False

            if acc == "no":
                return False

            return True

        # ----- WALK -----
        if vehicle == "walk":
            if acc == "no":
                return False
            return True

        # ----- BIKE -----
        if vehicle == "bike":
            return True

        return False

    # ------------------- Haversine heuristic -------------------
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # meters
        lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

    def h(n):
        x1, y1 = G.nodes[n]["x"], G.nodes[n]["y"]
        x2, y2 = G.nodes[goal]["x"], G.nodes[goal]["y"]
        return haversine(y1, x1, y2, x2)

    # ------------------- A* -------------------

    # khởi tạo g_score, f_score nhận giá trị lớn nhất
    g_score = {node: float("inf") for node in G.nodes}
    f_score = {node: float("inf") for node in G.nodes}
    parent = {node: None for node in G.nodes}

    # gán giá trị f_score cho đỉnh đầu
    g_score[start] = 0
    f_score[start] = h(start)

    open_set = [(f_score[start], start)]
    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in closed_set:
            continue

        # print(current)

        closed_set.add(current)

        # Đã tới đích
        if current == goal:
            break

        # Mở rộng từng cạnh đúng chuẩn MultiDiGraph
        for neighbor in G.neighbors(current):

            edges_dict = G[current][neighbor]
            for key, edge in edges_dict.items():

                # Kiểm tra chiều hợp lệ
                if not allow_direction(current, neighbor, edge):
                    continue

                # Ràng buộc phương tiện trên edge
                if not allow_vehicle(edge):
                    continue

                # Cost theo lựa chọn
                cost_edge = edge["weight_length"] if use_weight_length == 1 else edge["length"]

                # Trường hợp cạnh bị cấm thì không đi vào
                if cost_edge < 0:
                    continue

                tentative_g = g_score[current] + cost_edge

                # Nếu đã đóng -> bỏ qua (giống C++)
                if neighbor in closed_set:
                    continue

                # Nếu tốt hơn hoặc chưa từng thấy neighbor
                if tentative_g < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + h(neighbor)

                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # ------------------- Reconstruct path -------------------
    if parent[goal] is None and start != goal:
        return None, float("inf")

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    path.reverse()
    return path, g_score[goal]
