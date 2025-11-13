import networkx as nx
from pathlib import Path

current_file = Path(__file__).resolve()
current_dir = current_file.parent
target_path = current_dir.parent.parent / "map_data" / "graph.graphml"

# đọc file GraphML
G = nx.read_graphml(target_path)

# số node
num_nodes = G.number_of_nodes()
# số edge
num_edges = G.number_of_edges()

print(f"Số node: {num_nodes}")
print(f"Số edge: {num_edges}")
