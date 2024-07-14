from typing import Any, Dict, Hashable


class Node:
    """
    Class for nodes to be used in a directed graph.
    """

    def __init__(self, label: Hashable) -> None:
        self.label = label  # Unique hashable label for each node

        # Nodes connected by out-going edges
        self.children: Dict[Hashable, Any] = dict()
        # Nodes connected by in-coming edges
        self.parents: Dict[Hashable, Any] = dict()

    def add_child(self, c_label: Hashable, weight) -> None:
        self.children[c_label] = weight

    def del_child(self, c_label: Hashable) -> None:
        self.children.pop(c_label)

    def add_parent(self, p_label: Hashable, weight) -> None:
        self.parents[p_label] = weight

    def del_parent(self, p_label: Hashable) -> None:
        self.parents.pop(p_label)


class Graph:
    """
    Class for a directed graph.
    """
    def __init__(self) -> None:
        """
        Nodes stored in a dict as per Adjacency List format.
        """
        self.nodes: Dict[Hashable, Node] = dict()

    def add_node(self, label: Hashable) -> None:
        self.nodes[label] = Node(label)

    def del_node(self, label: Hashable) -> None:
        for c_label in self.nodes[label].children.keys():
            self.del_edge(p_label=label, c_label=c_label)
        for p_label in self.nodes[label].parents.keys():
            self.del_edge(p_label=p_label, c_label=label)
        self.nodes.pop(label)

    def add_edge(self, p_label, c_label, weight) -> None:
        if p_label in self.nodes.keys() and c_label in self.nodes.keys():
            self.nodes[p_label].add_child(c_label=c_label, weight=weight)
            self.nodes[c_label].add_parent(p_label=p_label, weight=weight)

    def del_edge(self, p_label, c_label) -> None:
        if p_label in self.nodes.keys() and c_label in self.nodes.keys():
            self.nodes[p_label].del_child(c_label=c_label)
            self.nodes[c_label].del_parent(p_label=p_label)
