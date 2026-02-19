from collections import defaultdict


def build_adj_list(edges: list[tuple[int, int]], dir: bool=False) -> dict[int, set]:
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        if not dir:
            adj[v].add(u)
    return adj

class Vertex:
    def __init__(self, id: int):
        self.id = id

    def __str__(self) -> str:
        return str(self.id)

class Graph:

    def __init__(self, n: int, edges: list[tuple[int, int]], directed=False):
        self.directed = directed
        self.edges = build_adj_list(edges, directed)
        self.n = n
        self.vertices = {i: Vertex(i) for i in range(n)}

    def __getitem__(self, item: int | tuple[int, int]) -> Vertex | bool:
        if isinstance(item, int):
            return self.vertices[item]
        elif isinstance(item, tuple):
            if self.directed:
                return item[1] in self.edges[item[0]]
            else:
                return item[1] in self.edges[item[0]] or item[0] in self.edges[item[0]]
        else:
            raise TypeError

    def __iter__(self):
        return iter(range(self.n))

    def __len__(self):
        return self.n

    def nbrs(self, v: Vertex| int) -> set[int]:
        if isinstance(v, Vertex):
            return self.edges[v.id]
        elif isinstance(v, int):
            return self.edges[v]
        else:
            raise TypeError

    def get_vertex(self, v: int) -> Vertex:
        return self.vertices[v]
