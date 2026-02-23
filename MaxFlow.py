from collections import defaultdict
from Graph import Graph, Vertex

def ford_fulkerson(G: Graph, c: dict[tuple[int, int], int], s: Vertex, t: Vertex) -> tuple[int, dict[tuple[int, int], int]]:
    # output: int, dict[Edge] = int cost of max flow and flow on each edge
    # initialize flow to 0
    flow = defaultdict(int)
    resid_weights = update_weights(G, c, flow)

    path = find_st_path(G, resid_weights, s.id, t.id)
    while path is not None:
        path_amt = min([resid_weights[(path[i], path[i+1])] for i in range(len(path) - 1)])
        for i in range(len(path) -1):
            flow[(path[i], path[i+1])] += path_amt
            flow[(path[i+1], path[i])] -= path_amt
        resid_weights = update_weights(G, c, flow)
        path = find_st_path(G, resid_weights, s.id, t.id)

    return flow

def update_weights(G: Graph, c: dict[tuple[int, int], int], f: dict[tuple[Vertex, Vertex], int]) -> dict[tuple[int, int], int]:
    weights = defaultdict(int)
    for u, endpoints in G.edges.items():
        for v in endpoints:
            weights[(u, v)] = max(0, c[(u, v)] - f[(u, v)])
            weights[(v, u)] = f[(u, v)]
    return weights

def find_st_path(G: Graph, w: dict[tuple[int, int], int], s: int, t: int) -> list[int] | None:
    for v in G:
        G[v].parent = None

    marked = set()
    stack = [s]
    while stack:
        u = stack.pop()
        marked.add(u)
        for v in G.nbrs(u):
            if v not in marked:
                if w[(u, v)] > 0:
                    if v == t:
                        path = [t]
                        prev = u
                        while prev is not None:
                            path.append(prev)
                            prev = prev.parent
                        return path[::-1]
                    G[v].parent = u
                    stack.append(v)
    return None