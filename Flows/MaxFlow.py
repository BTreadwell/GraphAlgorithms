import time
from collections import defaultdict, deque
from typing import Callable

def _ford_fulkerson(G: dict[int, set[int]], c: dict[tuple[int, int], int], s: int, t: int, get_path: Callable) -> tuple[int, dict[tuple[int, int], int]]:
    """
    Ford-Fulkerson Max Flow implementation
    :param G: Graph represented as an adjacency list
    :param c: integral capacity function mapping directed edges to capacities
    :param s: source vertex
    :param t: sink vertex
    :param get_path: function for finding st paths ("ek-fat-pipe" (default) or "ek-short-pipe")
    :return: value of max flow (int) and flow values on each edge
    """
    flow, flow_value = defaultdict(int), 0

    resid_weights = update_weights(G, c, flow)
    path = get_path(G, resid_weights, s, t)
    while path is not None:
        path_amt = min([resid_weights[(path[i], path[i+1])] for i in range(len(path) - 1)])
        flow_value += path_amt
        for i in range(len(path) -1):
            u, v = path[i], path[i+1]
            if v in G[u]:
                flow[(u, v)] += path_amt
            elif u in G[v]:
                flow[(v, u)] -= path_amt
        resid_weights = update_weights(G, c, flow)
        path = get_path(G, resid_weights, s, t)
    return flow_value, flow

def update_weights(G: dict[int, set[int]], c: dict[tuple[int, int], int], f: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
    """
    Helper function for ford-fulkerson. Given flow and capacities, calculates edge weights in residual graph
    :param G: Graph G represented as an adjacency list
    :param c: Integral capcity function
    :param f: current flow values
    :return: weight function on residual graph
    """
    weights = defaultdict(int)
    for u, endpoints in G.items():
        for v in endpoints:
            weights[(u, v)] = c[(u, v)] - f[(u, v)]
            weights[(v, u)] = f[(u, v)]
    return weights

def st_path_bfs(G: dict[int, set[int]], w: dict[tuple[int, int], int], s: int, t: int) -> list[int] | None:
    """
    Finds an s,t path in G using BFS
    :param G: Graph represented as adjacency list
    :param w: weight function (only used so we don't take 0 edges)
    :param s: int start point
    :param t: int end point
    :return: path represented as list of vertices or None if no st path exists
    """
    parent: dict[int, int | None] = defaultdict(lambda: None)
    marked = set()
    queue = deque([s])
    while queue:
        u = queue.pop()
        marked.add(u)
        for v in G[u]:
            if v not in marked and w[(u,v)] > 0:
                parent[v] = u
                if v == t:
                    return get_path(parent, t)
                queue.append(v)
    return None

def shortest_path_lengths(G: dict[int, set[int]], w: dict[tuple[int, int], int], s: int) -> dict[int, int | None]:
    sp_lengths = defaultdict(lambda: None)
    queue = deque([(s, 0)])
    while queue:
        u, lvl = queue.pop()
        sp_lengths[u] = lvl
        for v in G[u]:
            if sp_lengths[v] is None and w[(u, v)] > 0:
                queue.append((v, lvl + 1))
    return sp_lengths


def get_path(parent: dict[int, int | None], tail: int) -> list[int]:
    """
    Returns path from head to tail
    :param parent: list of predecessors
    :param tail: end point of path
    :return: path as list of vertices
    """
    path = [tail]
    curr = parent[tail]
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]

def st_path_fat(G: dict[int, set[int]], w: dict[tuple[int, int], int], s: int, t: int) -> list[int] | None:
    """
    Finds st path with max bottle neck
    :param G: Graph represented as adjacency list
    :param w: integral weight function
    :param s: int source
    :param t: int sink
    :return: path as list of vertices
    """
    edges = [x for (x,y) in w.items() if y != 0]
    edges.sort(key = lambda e: w[e], reverse=True)

    if st_path_bfs(G, w, s, t) is None:
        return None

    lwr = 0
    upr = len(edges)
    midpt = (lwr + upr) // 2
    while midpt != lwr:
        G_e = get_graph(edges[:midpt])
        if st_path_bfs(G_e, w, s, t) is not None:
            upr = midpt
        else:
            lwr = midpt
        midpt = (upr + lwr) // 2
    return st_path_bfs(get_graph(edges[:upr]), w, s, t)

def get_graph(edges: list[tuple[int, int]]) -> dict[int, set[int]]:
    """
    Get adjacency list from list of edges
    :param edges: list of edges (int, int)
    :return: adjacency list
    """
    G = defaultdict(set)
    for (u,v) in edges:
        G[u].add(v)
    return G

def get_blocking_flow(G, resid_weights, sp_dists, s, t):
    val, blocking_flow = 0, defaultdict(int)

    parent: dict[int, int | None] = defaultdict(lambda: None)

    stack = [s]
    while stack:
        u = stack.pop()
        if u == t:
            p = get_path(parent, t)
            bottleneck_val = min([resid_weights[(p[i], p[i+1])] for i in range(len(p) - 1)])
            val += bottleneck_val
            for i in range(len(p) - 1):
                resid_weights[p[i], p[i + 1]] -= bottleneck_val
                resid_weights[p[i+1], p[i]] += bottleneck_val
                if resid_weights[p[i], p[i+1]] == 0:
                    parent[p[i + 1]] = None
                if (i+1) in G[i]:
                    blocking_flow[(i, i+1)] += bottleneck_val
                else:
                    blocking_flow[(i+1, i)] -= bottleneck_val
        else:
            for v in G[u]:
                if parent[v] is None and resid_weights[(u, v)] > 0 and sp_dists[v] - 1 == sp_dists[u]:
                    parent[v] = u
                    stack.append(v)

    return val, blocking_flow

def ek_short_pipe(G: dict[int, set[int]], c: dict[tuple[int, int], int], s: int, t: int) -> tuple[int, dict[tuple[int, int], int]]:
    return _ford_fulkerson(G, c, s, t, st_path_bfs)

def ek_fat_pipe(G: dict[int, set[int]], c: dict[tuple[int, int], int], s: int, t: int) -> tuple[int, dict[tuple[int, int], int]]:
    return _ford_fulkerson(G, c, s, t, st_path_fat)

def dinics(G: dict[int, set[int]], c: dict[tuple[int, int], int], s: int, t: int) -> tuple[int, dict[tuple[int, int], int]]:
    max_val, flow = 0, defaultdict(int)
    resid_weights = update_weights(G, c, flow)
    sp_dists = shortest_path_lengths(G, resid_weights, s)
    val, blocking_flow = get_blocking_flow(G, resid_weights, sp_dists, s, t)
    while val > 0:
        max_val += val
        #resid_weights = update_weights(G, c, flow)
        val, blocking_flow = get_blocking_flow(G, resid_weights, sp_dists, s, t)
    return max_val, flow


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

    results = [] * len(testcases)
    for i, (g, c) in enumerate(testcases):
        r = []
        start = time.perf_counter()
        ans = ek_fat_pipe(g, c, 0, max(g.keys()))
        end = time.perf_counter()
        r.append(ans[0])
        r.append(end - start)

        start = time.perf_counter()
        ans = ek_short_pipe(g, c, 0, max(g.keys()))
        end = time.perf_counter()
        r.append(ans[0])
        r.append(end - start)

        start = time.perf_counter()
        ans = dinics(g, c, 0, max(g.keys()))
        end = time.perf_counter()
        r.append(ans[0])
        r.append(end - start)

        results.append(r)

    for i, r in enumerate(results):
        print(f"***Testcase {i}***\nFP Ans: {results[i][0]}\tFP Time: {results[i][1]}\nSP Ans: {results[i][2]}\tSP Time: {results[i][3]}\nDN Ans: {results[i][4]}\tDN Time: {results[i][5]}")

if __name__ == "__main__":
    main()