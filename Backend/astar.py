import heapq
from math import radians, sin, cos, sqrt, atan2
from constraints import get_constraint

# ---------------------------
# HAVERSINE DISTANCE
# ---------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


# ---------------------------
# A* SEARCH (MultiDiGraph aware)
# ---------------------------
def astar(G, start, goal, vehicle="car"):
    allow = get_constraint(vehicle)

    def h(n):
        x1, y1 = G.nodes[n]["x"], G.nodes[n]["y"]
        x2, y2 = G.nodes[goal]["x"], G.nodes[goal]["y"]
        return haversine(y1, x1, y2, x2)

    open_set = [(0, start)]
    g_score = {start: 0}
    came_from = {}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor in G.neighbors(current):
            edges_dict = G[current][neighbor]  # dict các edge key trong MultiDiGraph

            for key, edge in edges_dict.items():
                # Kiểm tra đường một chiều (oneway)
                if edge.get("oneway", False) and not G.is_directed():
                    continue  # nếu không đi đúng chiều, bỏ qua

                # Kiểm tra phương tiện
                if not allow(edge):
                    continue

                tentative_g = g_score[current] + edge.get("length", 1.0)

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + h(neighbor)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

    # Reconstruct path
    if goal not in came_from:
        return None, float("inf")

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()

    return path, g_score[goal]
