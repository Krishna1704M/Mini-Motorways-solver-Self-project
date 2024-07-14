import queue

from graph import Graph


def simple_graph_maker(dim: tuple[int, int],
                       roads: list[tuple[tuple[int, int], tuple[int, int]]]
                       ) -> Graph:
    # initializing the graph
    g = Graph(rows=dim[0], cols=dim[1])

    # creating a set of all the nodes connected by at least 1 road
    nodes = set()
    for road in roads:
        nodes.add(road[0])
        nodes.add(road[1])

    # adding all the nodes to the graph
    for node in nodes:
        g.addNode(node)

    # adding edges between each pair of nodes connected by a road
    for node1, node2 in roads:
        g.addEdge(node1, node2, [node2])
        g.addEdge(node2, node1, [node1])
    return g


def bfs_path_finder(G: Graph, src: tuple[int, int], trg: tuple[int, int]
                    ) -> list[tuple[int, int]]:
    pass  # implement task 1 here by removing that pass


def dfs_graph_maker(dim: tuple[int, int],
                    roads: list[tuple[tuple[int, int], tuple[int, int]]]
                    ) -> Graph:
    cols = dim[1]
    def encode(co_ord):
        return co_ord[0]*cols + co_ord[1]

    g_simple = simple_graph_maker(dim, roads)
    g_dfs = Graph(rows=dim[0], cols=dim[1])
    # implement dfs in g_simple and analyse each node
    nodes = g_simple.getNodes()
    for node in nodes:
        if len(g_simple.getAdjList(node)) != 2:
            start = node
            break

    stack = queue.LifoQueue(maxsize=-1)
    visited = set()
    parents = {y*cols+x: (None, None)
               for x in range(dim[1]) for y in range(dim[0])}
    # path is the list of nodes traversed
    stack.put((start, [], 0))

    # Check if the starting node has 2 nodes or not. If it has 2 nodes, then in g_dfs,
    # add the two neighbors as an edge along with the path else simply add the nodes and corresponding edges
    while not stack.empty():
        vertex, path, index = stack.get()
        adj_list = g_simple.getAdjList(vertex)

        if vertex not in visited:
            if len(adj_list) != 2:
                g_dfs.addNode(vertex)

        if len(adj_list) != 2:
            if len(path) != 0 and path[0] != vertex:
                g_dfs.addEdge(path[0], vertex, path[1:]+[vertex])
            new_path = [vertex]
        else:
            new_path = path + [vertex]

        if vertex not in visited:
            visited.add(vertex)
            if len(path) != 0:
                parents[encode(vertex)] = path[-1]
            else:
                parents[encode(vertex)] = (None, None)

        if len(path) == 0 or (
                parents[encode(path[-1])] == vertex or
                parents[encode(vertex)] == path[-1]):
            while index < len(adj_list) and (
                adj_list[index][0] == parents[encode(vertex)] or (
                    adj_list[index][0] in visited and
                    adj_list[index][0] not in g_dfs.getNodes())):
                index = index+1

            if index < len(adj_list):
                neighbor = adj_list[index][0]
                if neighbor:
                    stack.put((vertex, path, index+1))
                    stack.put((neighbor, new_path, 0))
                    continue

        if not stack.empty():
            parent, parent_path, parent_index = stack.get()
            stack.put((parent, new_path, parent_index))

    return g_dfs


def dijkstras_path_finder(G: Graph, src: tuple[int, int], trg: tuple[int, int]
                          ) -> list[tuple[int, int]]:
    pass  # implement task 3 here by removing that pass
