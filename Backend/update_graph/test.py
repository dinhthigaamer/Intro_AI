import osmnx as ox
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx

current_file = Path(__file__).resolve()
current_dir = current_file.parent
target_path = current_dir.parent.parent / "map_data" / "graph.graphml"
# load GraphML bằng osmnx (nếu GraphML xuất từ osmnx sẽ đúng chuẩn)
G = nx.read_graphml(target_path)

# tạo pos từ x, y
pos = {n: (float(d['x']), float(d['y'])) for n, d in G.nodes(data=True)}

for u, v, d in G.edges(data=True):
    print(u, v, d)

# # vẽ
# plt.figure(figsize=(10, 10))
# nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
# nx.draw_networkx_nodes(G, pos, node_size=10, node_color='red')
# plt.axis('off')
# plt.show()
