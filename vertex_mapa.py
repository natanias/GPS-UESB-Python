class Vertex:
    
    def __init__(self, key, lat, lon):
        self.id = key
        self.lat = lat
        self.lon = lon
        self.connected_to = {}

    def add_neighbor(self, nbr, weight=0):
        self.connected_to[nbr] = weight

    def get_connections(self):
        return self.connected_to.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr):
        return self.connected_to[nbr]
    
    def getLat(self, lat):
        return self.lat

    def getLon(self, lon):
        return self.lon