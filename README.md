[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/RNukvtFO)

# Project 3: Pathfinder

## Map Theme

My map represents a localized city navigation system for Ulsan, South Korea. It models the layout between major commercial districts, transit hubs, and parks to calculate the fastest driving routes across the city.

## Map Picture

![Project map](assets/map.png)

## How the Graph Works

### Nodes

Each node represents a distinct physical landmark, park, or major transit station in Ulsan (e.g., Ulsan City Hall, KTX Ulsan Station, Taehwa River National Garden).

### Edges

Each edge represents the primary physical road networks or highways connecting two locations.

### Weights

Each weight represents the travel cost, specifically measured in the estimated driving time (in minutes) under normal traffic conditions.

## Features Implemented

Check the features you completed:

- [x] Load graph from JSON
- [x] Get neighbors
- [x] BFS traversal
- [x] Dijkstra shortest distances
- [x] Shortest path reconstruction
- [x] Demo function
- [x] Extra tests
- [x] Stretch feature: Interactive Command-Line Menu with Dynamic Node Loading

## How to Run

To run the interactive demonstration menu (which automatically loads the available locations from the JSON file), run the following from the root directory:

```bash
python -m src.project
```

## How to Test

To run the standard tests alongside my three custom edge-case tests, run:

```bash
pytest -q
```

## Complexity

### BFS

**Time:**

```
O(V + E)
```

**Space:**

```
O(V)
```

**Explanation:**

`V` is the number of vertices (locations) and `E` is the number of edges (roads). The BFS algorithm visits each location exactly once and iterates through every road to check its neighbors. The space complexity is `O(V)` because the `queue` and the `visited` set will store at most `V` elements at the same time in the worst-case scenario.

---

### Dijkstra

**Time:**

```
O((V + E) log V)
```

**Space:**

```
O(V)
```

**Explanation:**

Dijkstra's algorithm also evaluates every vertex and edge. However, because it tracks the shortest known distances using a priority queue (`heapq` in Python), adding and removing nodes from the queue takes `O(log V)` time. This adds a logarithmic multiplier to the standard traversal time. Space is `O(V)` because the `distances` dictionary, `previous` tracker, and priority queue all scale linearly with the number of vertices.

---

### Shortest Path Reconstruction

**Time:**

```
O(P)
```

**Space:**

```
O(P)
```

**Explanation:**

`P` is the number of nodes in the final shortest path. Rebuilding the path simply involves stepping backward through the `previous` dictionary from the target node until we hit the start node. The space complexity is `O(P)` because we create a single list of size `P` to store this sequence of nodes before reversing it.

## Edge Cases

Check the edge cases your project handles:

- [x] Empty graph
- [x] Missing start node
- [x] Missing target node
- [x] Start equals target
- [x] Unreachable target
- [x] Graph with a cycle
- [x] Graph with one node
- [x] Disconnected graph
- [x] Multiple possible paths
- [x] Zero weight rejected
- [x] Negative weight rejected

**Notes:**

My `load_graph` function aggressively checks data types using `type()` rather than just `isinstance()`. This ensures that boolean values (which Python sometimes treats as integers) and floats (like `2.5`) are immediately rejected, strictly enforcing the rule that weights must be positive integers. Furthermore, missing start/target nodes safely return empty lists or dictionaries instead of raising `KeyError` crashes.

## Known Limitations

- **Directed Graphs:** The current project assumes an undirected graph where every path goes both ways. It does not support one-way roads.
- **Negative Weights:** By nature of Dijkstra's algorithm, the program cannot handle negative weights (and actively raises a `ValueError` if one is encountered) because it assumes once a node is popped from the priority queue, the shortest path to it has been found.
- **Path Ties:** If there are multiple paths with the exact same shortest time, the algorithm will only return the first valid shortest path it discovers, rather than all possible optimal routes.

## Assistance & Sources

### AI Used?

Yes

### What AI Helped With

I used AI to help brainstorm edge cases for my custom `pytest` functions, and to confirm the logarithmic time complexity logic for the `heapq` priority queue implementation.

### Other Sources

- Python Official Documentation for `heapq`: <https://docs.python.org/3/library/heapq.html>
- Python Official Documentation for `collections.deque`: <https://docs.python.org/3/library/collections.html#collections.deque>