from collections import defaultdict

# Graph: given by adjacency list dict[int, set[int]]
# Vertices: int
# directed edges: tuple[int, int]
# weight/caps/flow: dict[tuple[int, int], int]
# assume no anti-parallel edges in G



def ford_fulkerson(G: dict[int, set[int]], c: dict[tuple[int, int], int], s: int, t: int) -> tuple[int, dict[tuple[int, int], int]]:
    flow = defaultdict(int)
    value = 0
    resid_weights = update_weights(G, c, flow)

    path = find_st_path(G, resid_weights, s, t)
    while path is not None:
        path_amt = min([resid_weights[(path[i], path[i+1])] for i in range(len(path) - 1)])
        value += path_amt
        for i in range(len(path) -1):
            u, v = path[i], path[i+1]

            if v in G[u]:
                flow[(u, v)] += path_amt
                assert flow[(u, v)] <= c[(u, v)]
            elif u in G[v]:
                flow[(v, u)] -= path_amt
                assert flow[(v, u)] >= 0
            else:
                raise Exception
        resid_weights = update_weights(G, c, flow)
        path = find_st_path(G, resid_weights, s, t)

    return value, flow

def update_weights(G: dict[int, set[int]], c: dict[tuple[int, int], int], f: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
    weights = defaultdict(int)
    for u, endpoints in G.items():
        for v in endpoints:
            weights[(u, v)] = max(0, c[(u, v)] - f[(u, v)])
            weights[(v, u)] = f[(u, v)]
    return weights

def find_st_path(G: dict[int, set[int]], w: dict[tuple[int, int], int], s: int, t: int) -> list[int] | None:
    parent: dict[int, int | None] = defaultdict(lambda: None)

    marked = set()
    stack = [s]
    while stack:
        u = stack.pop()
        marked.add(u)
        for v in G[u]:
            if v not in marked:
                if w[(u, v)] > 0:
                    if v == t:
                        path = [t]
                        prev = u
                        while prev is not None:
                            path.append(prev)
                            prev = parent[prev]
                        return path[::-1]
                    parent[v] = u
                    stack.append(v)
    return None



graph1 = {
    0: {1, 2},
    1: {3},
    2: {3},
    3: {4},
    4: set()
}

capacity1 = {
        (0, 1): 10,
        (0, 2): 5,
        (1, 3): 4,
        (2, 3): 8,
        (3, 4): 7,
    }

graph2 = {
    0: {1, 2},
    1: {3},
    2: {3},
    3: {4, 5},
    4: {6},
    5: {6},
    6: set()
}

capacity2 = {
        (0, 1): 8,
        (0, 2): 12,
        (1, 3): 6,
        (2, 3): 10,
        (3, 4): 3,
        (3, 5): 15,
        (4, 6): 3,
        (5, 6): 15,
    }

# Graph 3
graph3 = {
    0: {1, 2},
    1: {3},
    2: {3, 4},
    3: {5},
    4: {5},
    5: {6},
    6: set()
}

capacity3 = {
        (0, 1): 10,
        (0, 2): 10,
        (1, 3): 4,
        (2, 3): 6,
        (2, 4): 8,
        (3, 5): 8,
        (4, 5): 5,
        (5, 6): 9,
    }

# Graph 4
graph4 = {
    0: {1, 2, 3},
    1: {4},
    2: {4, 5},
    3: {5},
    4: {6},
    5: {6, 7},
    6: {8},
    7: {8},
    8: set()
}

capacity4 = {
        (0, 1): 15,
        (0, 2): 10,
        (0, 3): 5,
        (1, 4): 10,
        (2, 4): 5,
        (2, 5): 5,
        (3, 5): 5,
        (4, 6): 10,
        (5, 6): 5,
        (5, 7): 5,
        (6, 8): 10,
        (7, 8): 5,
    }

# Graph 5
graph5 = {
    0: {1, 2},
    1: {3, 4},
    2: {4},
    3: {5},
    4: {5},
    5: set()
}

capacity5 = {
        (0, 1): 10,
        (0, 2): 5,
        (1, 3): 4,
        (1, 4): 8,
        (2, 4): 5,
        (3, 5): 4,
        (4, 5): 8,
    }
testcases = [
    (graph1, capacity1), (graph2, capacity2), (graph3, capacity3), (graph4, capacity4), (graph5, capacity5)
]
def main():
    for (g, c) in testcases:
        print(ford_fulkerson(g, c, 0, max(g.keys())))

if __name__ == "__main__":
    main()