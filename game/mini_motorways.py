from pprint import pprint

from utilities import *


class MiniMotorways:
    """Overall class to manage the game"""

    def __init__(self, mode: str):
        """Initializes the game"""
        self.mode = mode

        # dimensions
        self.dim = tuple(int(i) for i in input().split(" "))

        # Markets
        n = int(input())
        self.markets = []
        while n:
            n -= 1
            s = [int(i) for i in input().split(" ")]
            self.markets.append(
                tuple((s[i], s[i+1]) for i in range(0, 6, 2)))

        # Houses
        n = int(input())
        self.houses = []
        while n:
            n -= 1
            self.houses.append(tuple(int(i) for i in input().split(" ")))

        # Roads
        n = int(input())
        self.roads = []
        while n:
            n -= 1
            s = [int(i) for i in input().split(" ")]
            self.roads.append(
                tuple((s[i], s[i+1]) for i in range(0, 4, 2)))

        self.road_network = self._make_graph()
        # for node in self.road_network.getNodes():
        #     print(node, end=" -> ")
        #     pprint(self.road_network.getAdjList(node))

    def _make_graph(self):
        """Will create a graph modelling the current road network"""
        if self.mode == "sim-bfs":
            return simple_graph_maker(self.dim, self.roads)
        elif self.mode == "dfs-djk":
            return dfs_graph_maker(self.dim, self.roads)

    def run(self):
        """Runs the game loop"""
        q = int(input())

        while q:
            q -= 1
            src, trg = tuple(int(i) for i in input().split(" "))
            path = self._shortest_path(src, trg)
            print(path)

    def _shortest_path(self, src, trg):
        if self.mode == "sim-bfs":
            return bfs_path_finder(self.road_network, self.houses[src], self.markets[trg][2])
        elif self.mode == "dfs-djk":
            return dijkstras_path_finder(self.road_network, self.houses[src], self.markets[trg][2])
