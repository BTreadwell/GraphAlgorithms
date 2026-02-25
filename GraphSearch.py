from collections import deque
from Graph import Graph

def dfs_reach(G: Graph, s: int, marked: set[int] | None = None) -> set[int]:
    # returns elements reachable by s in G using DFS
    if marked is None:
            marked = set()
    if s not in marked:
        marked.add(s)
        for v in G.nbrs(s):
            if v not in marked:
                marked = dfs(G, v, marked)
    return marked

def dfs(G: Graph, s: int, marked: set[int] | None =None, preorder: list[int] | None = None, postorder: list[int] | None = None) -> tuple[set[int], list[int], list[int]]:
    # dfs starting at node s, returns vertices reachable by s, dfs preorder, dfs postorder
    for v in G:
        v.marked = False
        v.pre = None
        v.post = None

    if marked is None:
        marked = set()
    if preorder is None:
        preorder = []
    if postorder is None:
        postorder = []

    if s not in marked:
        marked.add(s)
        preorder.append(s)
        for v in G.nbrs(s):
            if v not in marked:
                marked, preorder, postorder = dfs(G, v, marked, preorder, postorder)
        postorder.append(s)
    return marked, preorder, postorder

def bfs(G: Graph, s: int):
    # bfs for graph starting at node s
    marked = set()
    queue = deque([s])
    while queue:
        u = queue.pop()
        if u not in marked:
            marked.add(u)
            for v in G.nbrs(u):
                queue.append(v)
    return marked

def conn_components(G: Graph) -> set[set[int]]:
    # returns connected components of undirected graph G
    components = set()
    visited = set()

    for v in G:
        if v not in visited:
            c = dfs(G, v)[0]
            components.add(c)
            visited.update(c)
    return components


