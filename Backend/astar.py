import math
import heapq

#khởi tạo cạnh
class Edge:
    def __init__(self, to, distance_km, base_weight, traffic_level, allowed_vehicles, status):
        self.to = to
        self.distance_km = distance_km
        self.base_weight = base_weight
        self.traffic_level = traffic_level
        self.allowed_vehicles = allowed_vehicles
        self.status = status

#khởi tạo graph
class Graph:
    def __init__(self):
        self.nodes = {}     
        self.edges = {}    

#heuristic
def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#chi phí thật của cạnh (cần điều chỉnh thêm trạng thái sau)
def effective_cost(edge: Edge, vehicle):
    # 1. Kiểm tra Phương tiện Bị Cấm
    if vehicle not in edge.allowed_vehicles:
        return float('inf')
    
    # Trạng thái 'A' (Bình thường) - đã được đặt mặc định là 1.0
    # elif edge.status == 'A':
    # status_multiplier = 1.0
    # 2. Xử lý Trạng thái Đường (status)
    status_multiplier = 1.0
    
    # Trạng thái 'D'
    if edge.status == 'D':
        return float('inf') # Chi phí Vô hạn
    
    # Trạng thái 'C'
    elif edge.status == 'C':
        status_multiplier = 2.5 # Tăng chi phí lên 2.5 lần
        
    # Trạng thái 'B'
    elif edge.status == 'B':
        status_multiplier = 1.5 # Tăng chi phí lên 1.5 lần
        
    # 3. Tính toán Chi phí Thực tế
    # Chi phí = (Khoảng cách * Trọng số Cơ sở * Mức độ Giao thông) * Hệ số Trạng thái
    return edge.distance_km * edge.base_weight * edge.traffic_level * status_multiplier


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


def astar(graph: Graph, start, goal, vehicle):
    #fringe
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}

    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = haversine(graph.nodes[start], graph.nodes[goal])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), g_score[goal]

        for edge in graph.edges[current]:
            tentative_g = g_score[current] + effective_cost(edge, vehicle)

            if tentative_g < g_score[edge.to]:
                came_from[edge.to] = current
                g_score[edge.to] = tentative_g
                f_score[edge.to] = tentative_g + haversine(graph.nodes[edge.to], graph.nodes[goal])
                heapq.heappush(open_set, (f_score[edge.to], edge.to))

    return None, float('inf')
