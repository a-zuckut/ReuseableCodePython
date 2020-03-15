# graph.py

# IMPORTS
from collections import defaultdict

# Graph class
class Graph(object):
    """ Standard Graph ... undirected by default, can be directed """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections to graph - list of tuple pairs """
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add edge between node1 and node2, if directed from node1 -> node2 """
        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """
        for n, cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 - works for directed """
        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find a path between node1 and node2 (Not necessarily shortest) """
        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def find_shortest_path(self, node1, node2, path=[]):
        """ Returns shortest path from node1 to node2 """
        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        shortest = len(self._graph.items())
        p = None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_shortest_path(node, node2, path)
                if new_path and len(new_path) < shortest:
                    p = new_path
                    shortest = len(new_path)

        return p

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


if __name__ == "__main__":
    import pprint
    pretty_print = pprint.PrettyPrinter()

    connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),
                   ('C', 'D'), ('E', 'F'), ('F', 'C')]
    g = Graph(connections)
    g.add('E', 'D')
    g.add('G', 'B')
    g.find_path('G', 'E')

    pretty_print.pprint(g._graph)
    print(g.find_path('G', 'E'))
    print(g.find_shortest_path('G', 'E'))