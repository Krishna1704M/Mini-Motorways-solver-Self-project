class Graph():
    """Initialising the graph with n=rows,m=columns, the Graph Boundaries"""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        """adjDict has nodes as key and a corresponding dictionary as Adjacency Dictionary"""
        self.adjDict = dict()

    def addNode(self, node: tuple[int, int]):
        pos = node[0]+node[1]*self.cols
        if self._inGraph(node):
            """Initialising an empty dictionary as Adjacency list for that node"""
            self.adjDict[pos] = dict()
        else:
            print(
                f"Node {node[0]},{node[1]} is not inside the graph boundaries")

    def addEdge(self, src: tuple[int, int], tgt: tuple[int, int],  path: list[tuple[int, int]]):
        """Adding edges with weight"""
        pos1 = src[0]+src[1]*self.cols
        pos2 = tgt[0]+tgt[1]*self.cols
        allgood = True
        if pos1 not in self.adjDict.keys():
            print('Source not defined as a node')
            allgood = False
        if pos2 not in self.adjDict.keys():
            print('Target not defined as a node')
            allgood = False
        """Weight = len(path)"""
        """src->a->b->c->tgt"""
        """path=[a,b,c,tgt]"""
        if allgood:
            self.adjDict[pos1][pos2] = path

    def _getAdjDict(self, node: tuple[int, int]):
        pos = node[0]+node[1]*self.cols
        if pos in self.adjDict.keys():
            return self.adjDict[pos]
        else:
            return dict()

    def getAdjList(self, node: tuple[int, int]):
        adj_dict = self._getAdjDict(node=node)
        return [((pos % self.cols, pos//self.cols), val) for pos, val in adj_dict.items()]

    def getNodes(self):
        """Returns a list of Nodes with their coordinates as tuples"""
        return list(map(lambda pos: (pos % self.cols, pos//self.cols), self.adjDict.keys()))

    def _inGraph(self, node: tuple[int, int]):
        """Check if the point is in the graph"""
        if node[0] >= self.rows or node[1] >= self.cols:
            print(node, self.rows, self.cols)
            return 0
        return 1


""""The graph is one indexed i.e."""
"""0 1  2  3"""
"""4 5  6  7"""
"""8 9 10 11"""


if __name__ == '__main__':
    g = Graph(3, 3)
    g.addNode((1, 1))
    g.addNode((2, 2))
    g.addNode((3, 3))
    g.addEdge((1, 1), (2, 2), [(2, 2)])
    g.addEdge((1, 1), (0, 0), [(0, 0)])
    a = g.getAdjList((1, 1))
    print(a)
    b = g.getNodes()
    print(b)
