import osmnx as ox
import networkx as nx

place = "Phường Láng, Hanoi, Vietnam"
G = ox.graph_from_place(place, network_type='all')

for s, t, d in G.edges(data=True):
    if "weight" not in d:
        d["weight"] = 1
    else:
        d["weight"] = 1

ox.save_graphml(G, "../map_data/phuong_lang.graphml")

# G = nx.read_graphml("../map_data/phuong_lang.graphml")

# forbidden_highways = [
#     "motorway", "motorway_link",
#     "trunk", "trunk_link",
#     "pedestrian", "footway",
#     "cycleway", "path", "steps"
# ]

# edges_to_remove = []

# for u, v, k, data in G.edges(keys=True, data=True):
#     highway = data.get("highway", "")

#     # highway có thể là list → chuẩn hoá
#     if isinstance(highway, list):
#         hw_list = highway
#     else:
#         hw_list = [highway]

#     # 1. Nếu thuộc loại cấm → xoá
#     if any(hw in forbidden_highways for hw in hw_list):
#         edges_to_remove.append((u, v, k))
#         continue

#     # 2. Nếu tag cấm xe máy
#     if data.get("motorcycle") == "no":
#         edges_to_remove.append((u, v, k))
#         continue

#     if data.get("motor_vehicle") == "no":
#         edges_to_remove.append((u, v, k))
#         continue

#     if data.get("access") == "no":
#         edges_to_remove.append((u, v, k))
#         continue

# G.remove_edges_from(edges_to_remove)

# G.remove_nodes_from(list(nx.isolates(G)))

# for key in list(G.graph.keys()):
#     if "default" in key:
#         del G.graph[key]

# print(G.graph)
# ox.save_graphml(G, "../map_data/phuong_lang_motorcycle.graphml")
