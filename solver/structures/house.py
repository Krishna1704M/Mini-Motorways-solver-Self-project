from base import Octagonal_cell


class House(Octagonal_cell):
    """
    Class for Houses in the game.
    """

    def __init__(self, g, node_labels) -> None:
        super().__init__(g, node_labels)

    def __call__(self, active_dir) -> None:
        # Only one direction should be active
        # Nodes for rest of the directions can be deleted
        n_active = 0
        for direction, active in active_dir.items():
            if not active:
                self.del_nodes.append(direction)
            else:
                n_active += 1
        assert n_active == 1
        return super().__call__(active_dir)
