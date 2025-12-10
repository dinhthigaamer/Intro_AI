import networkx as nx
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def node_to_coordinate(map_path, list_of_node):
    G = nx.read_graphml(map_path)
    # list_of_node = [tuple(c) for c in list_of_node]
    coords = []

    for i in range(len(list_of_node)):
        u = list_of_node[i]
        lat = float(G.nodes[u]["y"])
        lon = float(G.nodes[u]["x"])

        if i == len(list_of_node)-1:
            coords.append((lat, lon, 1.0))
            continue

        v = list_of_node[i+1]
        w = float(G[u][v][0]["weight"])

        print(G[u][v][0])
        print(u, v, w)

        if "geometry" in G[u][v][0]:
            # print(u, v, G[u][v][0])
            latlon = G[u][v][0]["geometry"].replace(
                "LINESTRING (", "").replace(")", "").split(",")

            # print("LineString: ", [d.strip().split(" ") for d in latlon])
            for d in latlon:
                data = d.strip().split(" ")
                lat = float(data[1])
                lon = float(data[0])

                if (d == latlon[-1]):
                    pass
                else:
                    coords.append((lat, lon, w))
        else:
            coords.append((lat, lon, w))

    print(coords)

    return coords


def coordinate_to_node(map_path, list_of_coord):
    list_of_coord = [tuple(c) for c in list_of_coord]
    G = nx.read_graphml(map_path)
    nodes = []

    def findNearestNode(lat, lon):
        bestdis = -1
        best = ""
        for node in G.nodes:
            lat1 = float(G.nodes[node]["y"])
            lon1 = float(G.nodes[node]["x"])

            dis = haversine(lat, lon, lat1, lon1)
            if (bestdis == -1 or bestdis > dis):
                bestdis = dis
                best = node
        return best

    for coord in list_of_coord:
        lat, lon = coord
        node = findNearestNode(lat, lon)
        nodes.append(node)

    return nodes


def test(map_path):
    G = nx.read_graphml(map_path)
    coords = []
    nodes = []

    for s, t, d in G.edges(data=True):
        if "geometry" in d:
            latlon = d["geometry"].replace(
                "LINESTRING (", "").replace(")", "").split(",")

            # print("LineString: ", [d.strip().split(" ") for d in latlon])
            last = None
            for l in latlon:
                data = l.strip().split(" ")
                lat = float(data[1])
                lon = float(data[0])

                if last is not None:
                    coords.append([[float(last[0]), float(last[1])], [
                        float(lat), float(lon)]])
                last = (lat, lon)
        else:
            coords.append([[float(G.nodes[s]["y"]), float(G.nodes[s]["x"])], [
                float(G.nodes[t]["y"]), float(G.nodes[t]["x"])]])

    for node in G.nodes:
        nodes.append([float(G.nodes[node]["y"]), float(G.nodes[node]["x"])])

    return coords, nodes


if __name__ == '__main__':
    print(coordinate_to_node("../map_data/weighted_graph.graphml",
                             [[21.0239519, 105.8032043], [21.0225029, 105.8051480]]))
