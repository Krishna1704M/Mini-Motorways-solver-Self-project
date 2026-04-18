# Design Notes — Mini Motorways Solver

## Problem Formulation

The game grid is an R×C lattice. Road segments connect adjacent grid cells. Given a set of road segments, houses, and markets, answer routing queries: *what is the shortest road-path from house h to market m?*

## Graph Representations

### Simple Grid Graph (`game/graph.py`)
- Nodes: grid cells `(x, y)` encoded as `x + y * cols`
- Edges: each road segment → bidirectional edge with path `[target]`
- Adjacency stored as `dict[int, list]` (position-encoded → path)

### Directed Graph (`solver/graph.py`)
- Nodes: `Node` objects with `children` and `parents` dicts
- Supports weighted directed edges
- Used by the solver's structure system

## Algorithm Design

### BFS Path-Finding (`sim-bfs` mode)
Standard BFS on the unweighted grid graph. Appropriate when road lengths don't vary.

### DFS Graph Compression (`dfs-djk` mode)
**Motivation:** Dense grid graphs have many degree-2 nodes (straight road segments). These inflate graph size without adding routing choices.

**Compression step:**
1. Run DFS on the simple graph
2. When traversing through a degree-2 node, don't add it as a node in the compressed graph — accumulate it into the current path
3. Only add nodes at junctions (degree ≠ 2): these are the real decision points
4. Edge weight in compressed graph = length of the road segment between junctions

**Result:** Compressed graph has significantly fewer nodes/edges for networks with long straight roads.

### Dijkstra's Path-Finding
Runs on the compressed graph. Edge weights = road segment lengths. Returns shortest weighted path.

## Structures System (`solver/structures/`)

Models road infrastructure as graph mutations:
- `Structure`: base class — holds lists of edges/nodes to add/delete, applies them on `__call__`
- `Octagonal_cell`: 8-directional cell (N, S, E, W, NE, NW, SE, SW)
- `Diamond_cell`: 4-directional cell (NE, NW, SE, SW)
- `House`: Octagonal cell where only one direction is active — prunes all inactive direction nodes

## Known Incomplete Parts
- `bfs_path_finder` in `game/utilities.py` — stub (returns `None`)
- `dijkstras_path_finder` in `game/utilities.py` — stub (returns `None`)
