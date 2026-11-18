#!/usr/bin/env python3
"""Independent exact verifier for an n=2 weighted Clos counterexample.

Accepted JSON schemas:

{
  "schema": "weighted-clos-n2-v1",
  "left_vertices": ["l0", ...],
  "right_vertices": ["r0", ...],
  "edges": [
    {"id": "e0", "left": "l0", "right": "r0", "weight": "2/3"},
    ...
  ],
  "local_bins": {
    "L:l0": [["e0", ...], ["e2", ...]],
    "R:r0": [["e0", ...], ["e3", ...]]
  },
  "claim": {"n": 2, "colors": 3}
}

The verifier also accepts ``weighted-clos-counterexample-v1`` emitted by
``search_cegar.py``, either directly or inside its fixed/survey result wrapper.
It normalizes integer edge IDs and then applies the same independent checks.

The verifier deliberately shares no code with search_discrete.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


class VerificationError(ValueError):
    """The supplied object is not a valid counterexample witness."""


class SearchLimit(RuntimeError):
    """The exhaustive colouring check exceeded an explicit user limit."""


@dataclass(frozen=True)
class Edge:
    identifier: str
    left: str
    right: str
    weight: Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def parse_fraction(value: Any, context: str) -> Fraction:
    require(
        isinstance(value, str) or (isinstance(value, int) and not isinstance(value, bool)),
        f"{context} must be a rational string or integer",
    )
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError(f"{context} is not a rational number: {value!r}") from exc
    require(Fraction(0) < result <= Fraction(1), f"{context} must lie in (0, 1]")
    return result


def parse_string_list(value: Any, context: str) -> list[str]:
    require(isinstance(value, list), f"{context} must be a list")
    require(all(isinstance(item, str) and item for item in value), f"{context} contains a bad name")
    require(len(set(value)) == len(value), f"{context} contains duplicate names")
    return value


def normalize_cegar_witness(raw: dict[str, Any]) -> dict[str, Any]:
    require(raw.get("target_n") == 2, "CEGAR target_n must equal 2")
    require(raw.get("global_colours") == 3, "CEGAR global_colours must equal 3")
    topology = raw.get("topology")
    require(isinstance(topology, dict), "CEGAR topology must be an object")
    left = parse_string_list(topology.get("left_vertices"), "topology.left_vertices")
    right = parse_string_list(topology.get("right_vertices"), "topology.right_vertices")

    matrix = topology.get("multiplicity_matrix")
    require(isinstance(matrix, list) and len(matrix) == len(left), "bad multiplicity matrix rows")
    require(
        all(isinstance(row, list) and len(row) == len(right) for row in matrix),
        "bad multiplicity matrix columns",
    )
    require(
        all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for row in matrix
            for value in row
        ),
        "multiplicity matrix entries must be nonnegative integers",
    )

    edge_values = raw.get("edges")
    require(isinstance(edge_values, list), "CEGAR edges must be a list")
    normalized_edges: list[dict[str, Any]] = []
    observed = {(u, v): 0 for u in left for v in right}
    for index, item in enumerate(edge_values):
        require(isinstance(item, dict), f"CEGAR edges[{index}] must be an object")
        identifier = item.get("id")
        require(
            (isinstance(identifier, str) and identifier)
            or (isinstance(identifier, int) and not isinstance(identifier, bool)),
            f"CEGAR edges[{index}].id is invalid",
        )
        u, v = item.get("left"), item.get("right")
        require((u, v) in observed, f"CEGAR edge {identifier!r} has an unknown endpoint")
        observed[(u, v)] += 1
        normalized_edges.append(
            {
                "id": str(identifier),
                "left": u,
                "right": v,
                "weight": item.get("weight"),
            }
        )
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            require(
                observed[(u, v)] == matrix[i][j],
                f"multiplicity matrix disagrees at ({u}, {v})",
            )

    raw_bins = raw.get("local_two_bins")
    require(isinstance(raw_bins, dict), "CEGAR local_two_bins must be an object")
    normalized_bins: dict[str, Any] = {}
    for name in left:
        require(name in raw_bins, f"CEGAR bins missing left vertex {name}")
        normalized_bins[f"L:{name}"] = [
            [str(identifier) for identifier in bin_edges]
            if isinstance(bin_edges, list)
            else bin_edges
            for bin_edges in raw_bins[name]
        ] if isinstance(raw_bins[name], list) else raw_bins[name]
    for name in right:
        require(name in raw_bins, f"CEGAR bins missing right vertex {name}")
        normalized_bins[f"R:{name}"] = [
            [str(identifier) for identifier in bin_edges]
            if isinstance(bin_edges, list)
            else bin_edges
            for bin_edges in raw_bins[name]
        ] if isinstance(raw_bins[name], list) else raw_bins[name]
    require(
        set(raw_bins) == set(left) | set(right),
        "CEGAR local_two_bins contains unknown or ambiguous vertex keys",
    )

    return {
        "schema": "weighted-clos-n2-v1",
        "left_vertices": left,
        "right_vertices": right,
        "edges": normalized_edges,
        "local_bins": normalized_bins,
        "claim": {"n": 2, "colors": 3},
        "_cegar_exact_vertices": raw.get("vertices_requiring_two_bins"),
    }


def normalize_witness(raw: Any) -> dict[str, Any]:
    require(isinstance(raw, dict), "top-level JSON value must be an object")
    if raw.get("schema") not in {
        "weighted-clos-n2-v1",
        "weighted-clos-counterexample-v1",
    }:
        wrapped = raw.get("witness")
        require(isinstance(wrapped, dict), "unsupported schema and no witness object found")
        raw = wrapped
    if raw.get("schema") == "weighted-clos-counterexample-v1":
        return normalize_cegar_witness(raw)
    require(raw.get("schema") == "weighted-clos-n2-v1", "unsupported or missing schema")
    return raw


def parse_witness(
    raw: Any,
) -> tuple[list[str], list[str], list[Edge], dict[str, Any], list[str] | None]:
    raw = normalize_witness(raw)
    require(raw.get("schema") == "weighted-clos-n2-v1", "unsupported or missing schema")
    left = parse_string_list(raw.get("left_vertices"), "left_vertices")
    right = parse_string_list(raw.get("right_vertices"), "right_vertices")
    require(left and right, "both bipartition sides must be nonempty")

    claim = raw.get("claim")
    require(isinstance(claim, dict), "claim must be an object")
    require(claim.get("n") == 2, "claim.n must equal 2")
    require(claim.get("colors") == 3, "claim.colors must equal 3")

    edge_values = raw.get("edges")
    require(isinstance(edge_values, list) and edge_values, "edges must be a nonempty list")
    edges: list[Edge] = []
    seen_ids: set[str] = set()
    left_set, right_set = set(left), set(right)
    for index, item in enumerate(edge_values):
        require(isinstance(item, dict), f"edges[{index}] must be an object")
        identifier = item.get("id")
        u, v = item.get("left"), item.get("right")
        require(isinstance(identifier, str) and identifier, f"edges[{index}].id is invalid")
        require(identifier not in seen_ids, f"duplicate edge id {identifier!r}")
        require(u in left_set, f"edge {identifier!r} has unknown left endpoint")
        require(v in right_set, f"edge {identifier!r} has unknown right endpoint")
        weight = parse_fraction(item.get("weight"), f"edge {identifier!r} weight")
        seen_ids.add(identifier)
        edges.append(Edge(identifier, u, v, weight))

    bins = raw.get("local_bins")
    require(isinstance(bins, dict), "local_bins must be an object")
    expected_keys = {f"L:{name}" for name in left} | {f"R:{name}" for name in right}
    require(set(bins) == expected_keys, "local_bins keys must exactly match all namespaced vertices")
    claimed_exact = raw.get("_cegar_exact_vertices")
    if claimed_exact is not None:
        claimed_exact = parse_string_list(
            claimed_exact, "vertices_requiring_two_bins"
        )
    return left, right, edges, bins, claimed_exact


def check_graph_and_bins(
    left: list[str],
    right: list[str],
    edges: list[Edge],
    bins: dict[str, Any],
    claimed_exact: list[str] | None,
) -> dict[str, list[int]]:
    incident: dict[str, list[int]] = {f"L:{name}": [] for name in left}
    incident.update({f"R:{name}": [] for name in right})
    id_to_index = {edge.identifier: index for index, edge in enumerate(edges)}
    for index, edge in enumerate(edges):
        incident[f"L:{edge.left}"].append(index)
        incident[f"R:{edge.right}"].append(index)
    require(all(indices for indices in incident.values()), "isolated vertices must be deleted")

    exact_two = False
    exact_vertices: list[str] = []
    for vertex, indices in incident.items():
        value = bins[vertex]
        require(isinstance(value, list) and len(value) == 2, f"{vertex} must have exactly two bins")
        flattened: list[str] = []
        for bin_number, identifiers in enumerate(value):
            require(isinstance(identifiers, list), f"{vertex} bin {bin_number} must be a list")
            require(
                all(isinstance(identifier, str) for identifier in identifiers),
                f"{vertex} bin {bin_number} contains a non-string edge id",
            )
            require(
                len(set(identifiers)) == len(identifiers),
                f"{vertex} bin {bin_number} repeats an edge",
            )
            try:
                bin_indices = [id_to_index[identifier] for identifier in identifiers]
            except KeyError as exc:
                raise VerificationError(f"{vertex} bin {bin_number} names an unknown edge") from exc
            load = sum((edges[index].weight for index in bin_indices), Fraction(0))
            require(load <= 1, f"{vertex} bin {bin_number} has load {load} > 1")
            flattened.extend(identifiers)

        expected = sorted(edges[index].identifier for index in indices)
        require(sorted(flattened) == expected, f"{vertex} bins do not partition its incident edges")
        total = sum((edges[index].weight for index in indices), Fraction(0))
        if total > 1:
            exact_two = True
            # Convert the verifier's namespaced key back to the CEGAR key.
            exact_vertices.append(vertex.split(":", 1)[1])
    require(exact_two, "no vertex needs two bins; the instance parameter is not exactly n=2")
    if claimed_exact is not None:
        require(
            set(claimed_exact) == set(exact_vertices),
            "vertices_requiring_two_bins disagrees with exact rational loads",
        )
    return incident


def find_three_colouring(
    edges: list[Edge],
    incident: dict[str, list[int]],
    max_nodes: int | None,
) -> tuple[list[int] | None, int]:
    """Return a valid colouring, or None after an exhaustive exact search."""

    vertices = sorted(incident)
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    endpoints = [
        (vertex_index[f"L:{edge.left}"], vertex_index[f"R:{edge.right}"]) for edge in edges
    ]
    loads = [[Fraction(0) for _ in range(3)] for _ in vertices]
    assignment = [-1] * len(edges)
    remaining = set(range(len(edges)))
    memo: set[tuple[int, tuple[tuple[Fraction, ...], ...]]] = set()
    nodes = 0

    def canonical_state(mask: int) -> tuple[int, tuple[tuple[Fraction, ...], ...]]:
        columns = []
        for colour in range(3):
            columns.append(tuple(loads[vertex][colour] for vertex in range(len(vertices))))
        return mask, tuple(sorted(columns))

    def viable_colours(edge_index: int) -> list[int]:
        u, v = endpoints[edge_index]
        weight = edges[edge_index].weight
        return [
            colour
            for colour in range(3)
            if loads[u][colour] + weight <= 1 and loads[v][colour] + weight <= 1
        ]

    def visit(mask: int) -> bool:
        nonlocal nodes
        nodes += 1
        if max_nodes is not None and nodes > max_nodes:
            raise SearchLimit(f"colour search exceeded --max-nodes={max_nodes}")
        if not remaining:
            return True

        state = canonical_state(mask)
        if state in memo:
            return False

        choices: list[tuple[int, Fraction, int, list[int]]] = []
        for edge_index in remaining:
            colours = viable_colours(edge_index)
            if not colours:
                memo.add(state)
                return False
            choices.append((len(colours), -edges[edge_index].weight, edge_index, colours))
        _, _, edge_index, colours = min(choices)

        # Equivalent unused colours are globally symmetric. Only try the first one.
        used = {colour for colour in assignment if colour >= 0}
        unused = sorted(set(range(3)) - used)
        first_unused = unused[0] if unused else None
        colours = [colour for colour in colours if colour in used or colour == first_unused]

        remaining.remove(edge_index)
        u, v = endpoints[edge_index]
        weight = edges[edge_index].weight
        for colour in colours:
            assignment[edge_index] = colour
            loads[u][colour] += weight
            loads[v][colour] += weight
            if visit(mask ^ (1 << edge_index)):
                return True
            loads[u][colour] -= weight
            loads[v][colour] -= weight
            assignment[edge_index] = -1
        remaining.add(edge_index)
        memo.add(state)
        return False

    full_mask = (1 << len(edges)) - 1
    colourable = visit(full_mask)
    return (assignment.copy() if colourable else None), nodes


def verify(path: Path, max_nodes: int | None) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"cannot read JSON witness: {exc}") from exc
    left, right, edges, bins, claimed_exact = parse_witness(raw)
    incident = check_graph_and_bins(left, right, edges, bins, claimed_exact)
    colouring, nodes = find_three_colouring(edges, incident, max_nodes)
    if colouring is not None:
        rendered = {edges[index].identifier: colour for index, colour in enumerate(colouring)}
        raise VerificationError(f"instance is 3-colourable: {rendered}")
    return {
        "valid_counterexample": True,
        "vertices": len(left) + len(right),
        "edges": len(edges),
        "colour_search_nodes": nodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness", type=Path, help="JSON witness to verify")
    parser.add_argument(
        "--max-nodes",
        type=int,
        default=None,
        help="optional safety bound; exceeding it is inconclusive, not acceptance",
    )
    args = parser.parse_args()
    if args.max_nodes is not None and args.max_nodes < 1:
        parser.error("--max-nodes must be positive")
    try:
        result = verify(args.witness, args.max_nodes)
    except SearchLimit as exc:
        print(json.dumps({"valid_counterexample": None, "error": str(exc)}, sort_keys=True))
        return 2
    except VerificationError as exc:
        print(json.dumps({"valid_counterexample": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
