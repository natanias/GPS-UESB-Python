from queue import Queue
from collections import defaultdict
from vertex_mapa import Vertex

    
class Graph:
    def __init__(self):
        self.vert_list = {}

    def add_vertex(self, key, lat, lon):
        novo_vertice = Vertex(key, lat, lon)
        self.vert_list[key] = novo_vertice
        return novo_vertice
        
    def get_vertex(self, key):
        return self.vert_list[key]
        
    def add_edge(self, de, para, cost=0):
        if not de in self.vert_list:
            v1 = Vertex(de)
            self.vert_list[de] = v1
        if not para in self.vert_list:
            v2 = Vertex(para)
            self.vert_list[para] = v2
        v_de = self.vert_list[de]
        v_para = self.vert_list[para]
        v_de.add_neighbor(v_para, cost)
            
    def get_vertices(self):
        return self.vert_list.keys()
        
    def get_edges(self):
        edges = set()
        for key, vertex in self.vert_list.items():
            for vizinho in vertex.connected_to:
                edges.add((key, vizinho.id, vertex.get_weight(vizinho)))
        return list(edges)
    
    def bfs(self, start):
        queue = Queue()
        queue.put(self.get_vertex(start))
        visited = list()
        while (queue.qsize() > 0):
            vertex = queue.get()
            if vertex.id not in visited:
                visited.append(vertex.id)
                for nbr in vertex.get_connections():
                    if nbr.id not in visited:
                        queue.put(nbr)
        return visited


    def dfs(self, start):
        visited, stack = list(), [self.get_vertex(start)]
        while stack:
            vertex = stack.pop()
            if vertex.id not in visited:
                visited.append(vertex.id)
                for nbr in vertex.get_connections():
                    if nbr.id not in visited:
                        stack.append(nbr)
        return visited

    def dijkstra(self, start, maxD=1e309):
         # total distance from origin
        tdist = defaultdict(lambda: 1e309)
        tdist[start] = 0
        # neighbour that is nearest to the origin
        preceding_node = {}
        unvisited = set(self.get_vertices())
        while unvisited:
            current = unvisited.intersection(tdist.keys())
            if not current: break
            min_node = min(current, key=tdist.get)
            unvisited.remove(min_node)
            vertex = self.get_vertex(min_node)
            for neighbour in vertex.get_connections():
                d = tdist[min_node] + vertex.get_weight(neighbour)
                if tdist[neighbour.id] > d and maxD >= d:
                    tdist[neighbour.id] = d
                    preceding_node[neighbour.id] = min_node
        return tdist, preceding_node
    
    def min_path(self, start, end, maxD=1e309):
        tdist, preceding_node = self.dijkstra(start, maxD)
        dist = tdist[end]
        backpath = [end]
        try:
            while end != start:
                end = preceding_node[end]
                backpath.append(end)
            path = list(reversed(backpath))
        except KeyError:
            path = None
        return dist, path
    