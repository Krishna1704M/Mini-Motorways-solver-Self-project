# 🚗 Mini Motorways Solver

A graph-based AI solver for the game [Mini Motorways](https://dinopoloclub.com/games/mini-motorways/) — automatically computes optimal road paths between houses and markets using BFS, DFS-based graph compression, and Dijkstra's algorithm.

---

## 📌 What is Mini Motorways?

Mini Motorways is a strategy game where you build road networks to connect coloured houses to matching coloured markets in a growing city. As the city expands, roads become congested — the challenge is to design efficient networks that minimize travel time.

This project models the game grid as a graph and implements path-finding algorithms to solve routing queries optimally.

---

## 🏗️ Project Structure

```
Mini-Motorways-Solver/
│
├── game/                        # Game state model and path-finding
│   ├── main.py                  # Entry point — CLI runner
│   ├── mini_motorways.py        # Core game class (state management, routing)
│   ├── graph.py                 # Undirected grid graph implementation
│   ├── utilities.py             # Graph construction + BFS/DFS/Dijkstra utilities
│   └── test_case.txt            # Sample input for testing
│
├── solver/                      # Advanced solver with game automation
│   ├── graph.py                 # Directed graph (Node + adjacency dict)
│   ├── input.py                 # X11 window automation (xdo) to control game
│   └── structures/
│       ├── base.py              # Base classes: Structure, Octagonal_cell, Diamond_cell
│       └── house.py             # House structure (single active direction)
│
├── docs/
│   └── design.md                # Architecture and algorithm notes
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧠 Algorithms Implemented

### 1. Simple BFS Graph + BFS Path-Finding (`sim-bfs` mode)
- Builds a flat grid graph directly from road segments
- Each road segment becomes a bidirectional edge
- Shortest path found via Breadth-First Search (unweighted)

### 2. DFS Graph Compression + Dijkstra's (`dfs-djk` mode)
- **Graph compression via DFS:** Collapses long straight road segments (degree-2 nodes) into single weighted edges — reduces graph size significantly for dense networks
- **Dijkstra's algorithm:** Finds the shortest weighted path in the compressed graph
- More efficient for large, complex road networks

### Input Format

```
<rows> <cols>
<num_markets>
<market_1: x1 y1 x2 y2 x3 y3>   # 3 entry points per market
...
<num_houses>
<house_1: x y>
...
<num_roads>
<road_1: x1 y1 x2 y2>
...
<num_queries>
<query: house_idx market_idx>
...
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the Solver

```bash
# BFS mode (simpler graph, BFS path-finding)
python3 game/main.py sim-bfs < game/test_case.txt

# DFS-compressed graph + Dijkstra's
python3 game/main.py dfs-djk < game/test_case.txt
```

### Sample Output

Given the included `test_case.txt` — **8 cols × 14 rows grid, 2 markets, 5 houses, 58 road segments:**

**Full Road Network:**
```
   0 1 2 3 4 5 6 7
   ────────────────
 0│· · · ┼ ┼ ─ ─ ┼
 1│· · │ │ │ · M1┼
 2│· · M0│ │ · · ·
 3│· · │ │ │ · · ·
 4│· · ┼ ┼ ┼ ─ ─ ┼
 5│· · │ · │ · · │
 6│· · ┼ ─ ┼ · · │
 7│· · │ · │ · · │
 8│· · │ · │ · · ·
 9│· · │ · │ ┼ H1·
10│· · │ · │ ┼ H2H3
11│· · │ · │ │ H4│
12│· · ┼ ─ ┼ ┼ ┼ ┼
13│· · │ · H0· · ·

· = empty  ─/│ = road  ┼ = junction
```

**Query Results — BFS Shortest Paths:**

```
H0 (4,13) → M0 (2,2)    13 steps
 0│· · · ┼ ┼ ─ ─ ┼
 1│· · │ │ │ · M ┼
 2│· · M │ │ · · ·       ← destination
 3│· · * │ │ · · ·
 4│· · * ┼ ┼ ─ ─ ┼
 5│· · * · │ · · │
 6│· · * ─ ┼ · · │
 7│· · * · │ · · │
 8│· · * · │ · · ·
 9│· · * · │ ┼ H ·
10│· · * · │ ┼ H H
11│· · * · │ │ H │
12│· · * * * ┼ ┼ ┼       ← joins horizontal corridor
13│· · │ · H · · ·       ← source

Route: (4,13)→(4,12)→(3,12)→(2,12)→(2,11)→...→(2,3)→(2,2)
```

```
H1 (6,9) → M0 (2,2)     17 steps
 9│· · * · │ * H ·       ← source, takes road left
10│· · * · │ * H H
11│· · * · │ * H │
12│· · * * * * ┼ ┼       ← merges into corridor
...
 2│· · M │ │ · · ·       ← destination

Route: (6,9)→(5,9)→(5,10)→(5,11)→(5,12)→(4,12)→...→(2,2)
```

```
H2 (6,10) → M1 (6,1)    21 steps
 0│· · · ┼ * * * *       ← top horizontal run to M1
 1│· · │ │ * · M *       ← destination
 2│· · M │ * · · ·
...
12│· · ┼ ─ * * ┼ ┼       ← enters horizontal corridor
13│· · │ · H · · ·

Route: (6,10)→(5,10)→(5,11)→(5,12)→(4,12)→(4,11)→...→(6,1)
```

---

## 🔌 Game Automation (Linux only)

`solver/input.py` uses `python-xdo` to directly control the Mini Motorways game window via X11:

- **Mouse drag** to connect road segments
- **Right-click** to disconnect roads
- **Powerup selection** (roundabouts, traffic lights)
- Configurable delay between actions

```python
from solver.input import InputParser

inp = InputParser(delay=0.3)
inp.activate_window()
inp.set_grid_parameters((16, 9), cell_size=84.0)
inp.connect(cell1=(5, 3), x_move=1, y_move=0)   # draw road right
inp.select_powerup(choice=2)                      # pick 2nd powerup
```

> ⚠️ Requires a running Mini Motorways window on Linux (X11). Does not work on Wayland or macOS/Windows without modification.

---

## 🖼️ Screenshots & Demo

> 📸 *Screenshots and GIF demos of the solver running on the live game will be added here.*

| Game View | Solver Output |
|-----------|--------------|
| ![Game screenshot](assets/game_screenshot.png) | ![Solver output](assets/solver_output.png) |

*To record your own demo: run the game, launch `solver/input.py`, and capture with any screen recorder.*

---

## 📊 Complexity Analysis

| Mode | Graph Build | Path Query | Space |
|------|------------|------------|-------|
| `sim-bfs` | O(R + N) | O(N + R) | O(N + R) |
| `dfs-djk` | O(N + R) | O((N' + R') log N') | O(N + R) |

Where N = grid nodes, R = road segments, N' and R' = compressed graph size.

---

## 🛣️ Roadmap

- [ ] Complete BFS path-finder (`game/utilities.py`)
- [ ] Complete Dijkstra's path-finder (`game/utilities.py`)
- [ ] Visualize road network and computed path (matplotlib)
- [ ] Add multi-query benchmarking
- [ ] Extend automation to Wayland / macOS

---

## 🎮 About

Built as a personal project to explore **graph algorithm design** in a practical, game-based setting. The core challenge — collapsing a dense grid graph into a compact weighted graph using DFS before running Dijkstra's — mirrors real-world road network simplification problems in transportation engineering.

---

## 📄 License

MIT License
