import osmnx as ox

place = "Phường Láng, Hanoi, Vietnam"
G = ox.graph_from_place(place, network_type='bike')

for s, t, d in G.edges(data=True):
    if "weight" not in d:
        d["weight"] = 1
    else:
        d["weight"] = 1

ox.save_graphml(G, "../map_data/phuong_lang_bike.graphml")
