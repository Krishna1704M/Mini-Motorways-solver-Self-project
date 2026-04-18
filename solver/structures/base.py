from functools import reduce
from typing import Any, Dict, Hashable, List, Tuple
from graph import Graph


class Structure:
    """
    Base class for all kinds of road structures.
    """

    def __init__(self, g: Graph, node_labels: Dict[str, Hashable]) -> None:
        """
        For passing all relavant information to this structure.
        """
        self.graph = g  # graph instance

        # Relevant nodes stored using a particular format
        self.internal_nodes = node_labels

        # Lists of edges and nodes to be added or deleted
        # Need to add elements to these in __call__
        self.add_edges: List[Tuple[str, str, Any]] = []
        self.del_edges: List[Tuple[str, str]] = []
        self.del_nodes: List[str] = []

    def __call__(self) -> None:
        """
        For adding or deleting edges and nodes among the internal nodes.
        """
        for edge in self.del_edges:
            self.graph.del_edge(p_label=self.internal_nodes[edge[0]],
                                c_label=self.internal_nodes[edge[1]])
        for node in self.del_nodes:
            self.graph.del_node(label=self.internal_nodes[node])
        for edge in self.add_edges:
            self.graph.add_edge(p_label=self.internal_nodes[edge[0]],
                                c_label=self.internal_nodes[edge[1]],
                                weight=edge[2])
        return


class Octagonal_cell(Structure):
    """
    Base class for all structures that occupy a single octagonal cell.
    """
    def __init__(self, g: Graph, node_labels: Dict[str, Hashable]) -> None:
        assert reduce(lambda x, y: x and y, [x in self.internal_nodes.keys() for x in [
            "N", "E", "W", "S", "NE", "SW", "SE", "NW"]]) and (len(node_labels) == 8)
        super().__init__(g, node_labels)

    def __call__(self, active_dir: Dict[str, bool]) -> None:
        assert reduce(lambda x, y: x and y, [x in self.internal_nodes.keys() for x in [
            "N", "E", "W", "S", "NE", "SW", "SE", "NW"]]) and (len(active_dir) == 8)
        return super().__call__()


class Diamond_cell(Structure):
    """
    Base class for all structures that occupy a single diamond cell.
    """
    def __init__(self, g: Graph, node_labels: Dict[str, Hashable]) -> None:
        assert reduce(lambda x, y: x and y, [x in self.internal_nodes.keys() for x in [
            "NE", "SW", "SE", "NW"]]) and (len(node_labels) == 4)
        super().__init__(g, node_labels)

    def __call__(self, active_dir: Dict[str, bool]) -> None:
        assert reduce(lambda x, y: x and y, [x in self.internal_nodes.keys() for x in [
            "NE", "SW", "SE", "NW"]]) and (len(active_dir) == 4)
        return super().__call__()
