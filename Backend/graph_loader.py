import networkx as nx
# Giả định 'astar' là module chứa các class Graph và Edge
from astar import Graph, Edge 

def load_graphml(path):
    # Đọc đồ thị từ file GraphML bằng NetworkX
    nx_graph = nx.read_graphml(path)
    graph = Graph()

    # 1. Xử lý Nodes (Các nút/điểm)
    for node in nx_graph.nodes:
        # Lấy tọa độ (lat, lon) từ thuộc tính của nút trong NetworkX
        lat = float(nx_graph.nodes[node]["lat"])
        lon = float(nx_graph.nodes[node]["lon"])
        
        # Lưu tọa độ vào dictionary nodes của Graph tùy chỉnh
        graph.nodes[node] = (lat, lon)
        # Khởi tạo danh sách cạnh rỗng cho mỗi nút
        graph.edges[node] = []

    # 2. Xử lý Edges (Các cạnh/đoạn đường)
    for u, v, data in nx_graph.edges(data=True):
        edge = Edge(
            to=v,
            distance_km=float(data["distance_km"]),
            base_weight=float(data["base_weight"]),
            traffic_level=float(data["traffic"]),
            allowed_vehicles=data["allowed"].split(","),
            status=data["status"]  # Lấy trạng thái A, B, C, D từ dữ liệu GraphML
        )
        
        # Thêm cạnh vào danh sách các cạnh đi ra từ nút u
        graph.edges[u].append(edge)

    return graph