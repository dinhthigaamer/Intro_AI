import networkx as nx

class MapLoader:
    def __init__(self, path_graphml):
        self.G = nx.read_graphml(path_graphml)
        self._convert_nodes()
        self._convert_edges()

    # ---------------------------
    # Node: chỉ cần x, y (float)
    # ---------------------------
    def _convert_nodes(self):
        for n, data in self.G.nodes(data=True):

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

    # ---------------------------
    # Edge: giữ lại đúng thuộc tính cần thiết cho từng phương tiện
    # ---------------------------
    def _convert_edges(self):
        for u, v, data in self.G.edges(data=True):

            # length
            if "length" in data:
                try:
                    data["length"] = float(data["length"])
                except:
                    data["length"] = 1.0
            else:
                data["length"] = 1.0

            # width
            if "width" in data:
                try:
                    data["width"] = float(data["width"])
                except:
                    data["width"] = 3.0
            else:
                data["width"] = 3.0

            # maxspeed
            if "maxspeed" in data:
                try:
                    data["maxspeed"] = float(data["maxspeed"])
                except:
                    data["maxspeed"] = 40.0
            else:
                data["maxspeed"] = 40.0

            # normalize strings
            if "highway" in data:
                data["highway"] = str(data["highway"]).lower()
            else:
                data["highway"] = ""

            if "access" in data:
                data["access"] = str(data["access"]).lower()
            else:
                data["access"] = ""

            # oneway
            if "oneway" in data:
                s = str(data["oneway"]).lower()
                data["oneway"] = (s in ("yes", "true", "1"))
            else:
                data["oneway"] = False

    def get_graph(self):
        return self.G
