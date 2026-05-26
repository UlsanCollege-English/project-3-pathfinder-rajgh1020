"""Project 3: Pathfinder.

Implement graph utilities for an undirected weighted map.
"""

from __future__ import annotations

from collections import deque
import heapq
import json


Graph = dict[str, dict[str, int]]


def load_graph(path: str) -> Graph:
    """Load a weighted graph from a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"Could not load file: {e}")

    if type(data) is not dict:
        raise ValueError("JSON file must contain a dictionary at the top level.")

    for node, neighbors in data.items():
        if type(neighbors) is not dict:
            raise ValueError(f"Neighbors for {node} must be a dictionary.")

        for neighbor, weight in neighbors.items():
            # Using type() instead of isinstance() to safely avoid booleans acting as ints
            if type(weight) is not int:
                raise ValueError(f"Weight from {node} to {neighbor} must be an integer.")
            if weight <= 0:
                raise ValueError(f"Weight from {node} to {neighbor} must be a positive integer.")

    return data


def get_neighbors(graph: Graph, node: str) -> dict[str, int]:
    """Return the neighbors and weights for node."""
    if node in graph:
        return graph[node]
    return {}


def bfs_order(graph: Graph, start: str) -> list[str]:
    """Return nodes in breadth-first traversal order."""
    if start not in graph:
        return []

    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dijkstra_distances(graph: Graph, start: str) -> dict[str, float]:
    """Return shortest distances from start to every reachable node."""
    if start not in graph:
        return {}

    distances = {start: 0.0}
    pq = [(0.0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # Skip if we already found a better path
        if current_dist > distances.get(current_node, float('inf')):
            continue

        for neighbor, weight in graph[current_node].items():
            if weight <= 0:
                raise ValueError("Found a zero or negative weight.")

            distance = current_dist + weight

            # If we found a shorter path to the neighbor, update it
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = float(distance)
                heapq.heappush(pq, (distance, neighbor))

    return distances


def shortest_path(graph: Graph, start: str, target: str) -> list[str]:
    """Return the shortest path from start to target."""
    if start not in graph or target not in graph:
        return []
    if start == target:
        return [start]

    distances = {start: 0.0}
    previous = {start: None}
    pq = [(0.0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node == target:
            break

        if current_dist > distances.get(current_node, float('inf')):
            continue

        for neighbor, weight in graph[current_node].items():
            if weight <= 0:
                raise ValueError("Found a zero or negative weight.")

            distance = current_dist + weight

            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = float(distance)
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path by walking backwards
    if target not in previous:
        return []

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()
    return path


def demo() -> None:
    """Print a short demonstration of your project."""
    print("================================")
    print("   Campus Pathfinder Demo       ")
    print("================================")

    try:
        graph = load_graph("data/map.json")
        nodes = list(graph.keys())
        print(f"Loaded {len(nodes)} locations successfully.")

        # Stretch feature: Simple command-line menu
        while True:
            print("\nOptions:")
            print("1. Show BFS traversal")
            print("2. Find shortest path between two buildings")
            print("3. Exit")

            choice = input("Enter choice (1-3): ").strip()

            if choice == "1":
                start = "Main Gate"
                print(f"\nBFS Order from '{start}':")
                print(" -> ".join(bfs_order(graph, start)))

            elif choice == "2":
                start = "Main Gate"
                target = "IT Building"
                print(f"\nCalculating route from {start} to {target}...")

                path = shortest_path(graph, start, target)
                dists = dijkstra_distances(graph, start)

                if path:
                    print("Route: " + " -> ".join(path))
                    print(f"Total walking time: {int(dists[target])} minutes.")
                else:
                    print("No path found.")

            elif choice == "3":
                print("Exiting demo. Goodbye!")
                break
            else:
                print("Invalid choice.")

    except Exception as e:
        print(f"Demo failed to run: {e}")


if __name__ == "__main__":
    demo()