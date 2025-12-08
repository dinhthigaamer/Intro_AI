# import osmnx as ox
import networkx as nx
import json

# Lấy đồ thị đường của quận / thành phố
G = nx.read_graphml("../map_data/weighted_graph.graphml")

# Convert nodes ra list [lat, lon]
nodes = [{"lat": data['y'], "lon": data['x']}
         for n, data in G.nodes(data=True)]

# Convert edges ra list các tuyến [ [lat, lon], [lat, lon], ...]
edges = []
for u, v, data in G.edges(data=True):
    # Lấy đường từ node u → v
    start = (G.nodes[u]['y'], G.nodes[u]['x'])
    end = (G.nodes[v]['y'], G.nodes[v]['x'])
    edges.append([start, end])

# Lưu thành JSON
with open("../graph.json", "w") as f:
    json.dump({"nodes": nodes, "edges": edges}, f)
