"""Public tests for Project 3: Pathfinder.

These tests check the required API and important graph edge cases.

Students should add at least 3 meaningful tests of their own.
"""

from __future__ import annotations

import json

import pytest

from src.project import (
    bfs_order,
    dijkstra_distances,
    get_neighbors,
    load_graph,
    shortest_path,
)


def sample_graph() -> dict[str, dict[str, int]]:
    """Return a small undirected weighted graph with a unique shortest path."""
    return {
        "A": {"B": 4, "C": 2},
        "B": {"A": 4, "C": 1, "D": 5},
        "C": {"A": 2, "B": 1, "D": 8, "E": 10},
        "D": {"B": 5, "C": 8, "E": 2, "Z": 6},
        "E": {"C": 10, "D": 2, "Z": 3},
        "Z": {"D": 6, "E": 3},
    }


def disconnected_graph() -> dict[str, dict[str, int]]:
    """Return a graph with two disconnected components."""
    return {
        "A": {"B": 2},
        "B": {"A": 2},
        "X": {"Y": 1},
        "Y": {"X": 1},
    }


def cyclic_graph() -> dict[str, dict[str, int]]:
    """Return a graph with a cycle."""
    return {
        "A": {"B": 1, "C": 1},
        "B": {"A": 1, "C": 1},
        "C": {"A": 1, "B": 1, "D": 1},
        "D": {"C": 1},
    }


def test_load_graph_reads_json_file(tmp_path):
    graph_data = {
        "Gate": {"Food": 4, "Stage": 7},
        "Food": {"Gate": 4},
        "Stage": {"Gate": 7},
    }
    map_path = tmp_path / "map.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    assert load_graph(str(map_path)) == graph_data


def test_load_graph_rejects_zero_weight(tmp_path):
    graph_data = {
        "A": {"B": 0},
        "B": {"A": 0},
    }
    map_path = tmp_path / "bad_map.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    with pytest.raises(ValueError):
        load_graph(str(map_path))


def test_load_graph_rejects_negative_weight(tmp_path):
    graph_data = {
        "A": {"B": -3},
        "B": {"A": -3},
    }
    map_path = tmp_path / "bad_map.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    with pytest.raises(ValueError):
        load_graph(str(map_path))


def test_get_neighbors_existing_node():
    graph = sample_graph()

    assert get_neighbors(graph, "A") == {"B": 4, "C": 2}


def test_get_neighbors_missing_node_returns_empty_dict():
    graph = sample_graph()

    assert get_neighbors(graph, "Missing") == {}


def test_bfs_order_connected_graph():
    graph = sample_graph()

    assert bfs_order(graph, "A") == ["A", "B", "C", "D", "E", "Z"]


def test_bfs_order_missing_start_returns_empty_list():
    graph = sample_graph()

    assert bfs_order(graph, "Missing") == []


def test_bfs_order_handles_cycle_without_repeating_nodes():
    graph = cyclic_graph()

    result = bfs_order(graph, "A")

    assert result == ["A", "B", "C", "D"]
    assert len(result) == len(set(result))


def test_bfs_order_does_not_cross_disconnected_components():
    graph = disconnected_graph()

    assert bfs_order(graph, "A") == ["A", "B"]


def test_dijkstra_distances_from_start():
    graph = sample_graph()

    assert dijkstra_distances(graph, "A") == {
        "A": 0,
        "B": 3,
        "C": 2,
        "D": 8,
        "E": 10,
        "Z": 13,
    }


def test_dijkstra_missing_start_returns_empty_dict():
    graph = sample_graph()

    assert dijkstra_distances(graph, "Missing") == {}


def test_dijkstra_does_not_include_unreachable_nodes():
    graph = disconnected_graph()

    assert dijkstra_distances(graph, "A") == {"A": 0, "B": 2}


def test_dijkstra_rejects_zero_or_negative_weights():
    graph = {
        "A": {"B": 2},
        "B": {"A": 2, "C": 0},
        "C": {"B": 0},
    }

    with pytest.raises(ValueError):
        dijkstra_distances(graph, "A")


def test_shortest_path_returns_best_path():
    graph = sample_graph()

    assert shortest_path(graph, "A", "Z") == ["A", "C", "B", "D", "E", "Z"]


def test_shortest_path_start_equals_target():
    graph = sample_graph()

    assert shortest_path(graph, "A", "A") == ["A"]


def test_shortest_path_missing_start_or_target_returns_empty_list():
    graph = sample_graph()

    assert shortest_path(graph, "Missing", "A") == []
    assert shortest_path(graph, "A", "Missing") == []


def test_shortest_path_unreachable_returns_empty_list():
    graph = disconnected_graph()

    assert shortest_path(graph, "A", "Y") == []

# ==========================================
# Custom Tests added for Project Requirements
# ==========================================

def test_load_graph_rejects_non_integer_weights(tmp_path):
    """Custom Test 1: Ensure float or boolean weights raise a ValueError during load."""
    graph_data = {
        "A": {"B": 2.5},
        "B": {"A": 2.5},
    }
    map_path = tmp_path / "bad_map_float.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    with pytest.raises(ValueError):
        load_graph(str(map_path))


def test_shortest_path_rejects_negative_weights():
    """Custom Test 2: Ensure shortest_path algorithm raises ValueError on negative weights."""
    graph = {
        "A": {"B": -5},
        "B": {"A": -5}
    }

    with pytest.raises(ValueError):
        shortest_path(graph, "A", "B")


def test_single_node_graph_operations():
    """Custom Test 3: Ensure all algorithms handle a graph with only one node correctly."""
    graph = {"A": {}}

    assert bfs_order(graph, "A") == ["A"]
    assert dijkstra_distances(graph, "A") == {"A": 0.0}
    assert shortest_path(graph, "A", "A") == ["A"]



def test_custom_map_loads_correctly(tmp_path):
    """Test 1: Verify my own map logic works as expected."""
    my_map = {
        "Library": {"IT Building": 2},
        "IT Building": {"Library": 2}
    }
    file_path = tmp_path / "my_map.json"
    file_path.write_text(json.dumps(my_map), encoding="utf-8")

    loaded = load_graph(str(file_path))
    assert loaded == my_map


def test_shortest_path_with_float_weights():
    """Test 2: Make sure load_graph catches float weights (like 2.5)."""
    bad_data = {
        "A": {"B": 2.5},
        "B": {"A": 2.5}
    }
    import tempfile
    import os

    # Write bad data to a temporary file
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, 'w') as f:
        json.dump(bad_data, f)

    with pytest.raises(ValueError):
        load_graph(path)

    os.remove(path)


def test_dijkstra_raises_error_on_negative_weight_in_traversal():
    """Test 3: Ensure algorithms abort if a bad weight slips through."""
    bad_graph = {
        "A": {"B": -4},
        "B": {"A": -4}
    }
    with pytest.raises(ValueError):
        dijkstra_distances(bad_graph, "A")