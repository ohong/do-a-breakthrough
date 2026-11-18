#!/usr/bin/env python3
"""Reproducible exhaustive control for Route B5 on marked 2x2 multigraphs.

Heavy edges have weight 3/5 and light edges have weight 2/5.  A cell stores
the multiplicity pair (heavy, light).  The exhaustive domain applies exactly:

* B.1 at every vertex: h <= 3 and l <= 6-h;
* connectedness and no isolates;
* at least one degree-six vertex;
* B.5: max heavy degree + max light degree >= 7;
* if the graph is 6-regular, its heavy degrees are nonconstant.

Every retained labelled instance is checked by an exact five-colour
backtracker.  Row/column permutations and bipartition transpose are used only
for reporting orbit counts, never to prune the labelled coverage check.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence


COLOUR_COUNT = 5


@dataclass(frozen=True, order=True)
class Cell:
    heavy: int
    light: int

    @property
    def total(self) -> int:
        return self.heavy + self.light


@dataclass(frozen=True)
class MarkedInstance:
    cells: tuple[Cell, Cell, Cell, Cell]

    @property
    def edge_count(self) -> int:
        return sum(cell.total for cell in self.cells)

    @property
    def instance_id(self) -> str:
        return ";".join(f"{cell.heavy},{cell.light}" for cell in self.cells)


@dataclass(frozen=True)
class Edge:
    edge_id: int
    left: int
    right: int
    heavy: bool


@dataclass(frozen=True)
class DomainStats:
    scanned: int
    retained: int
    retained_by_edges: dict[int, int]
    symmetry_orbits: int
    symmetry_orbits_by_edges: dict[int, int]


def cell_options() -> tuple[Cell, ...]:
    # Any one cell is incident to two vertices, so B.1 already implies these
    # per-cell bounds.  Enumerating precisely this 22-element set is complete.
    return tuple(
        Cell(heavy, light)
        for heavy in range(4)
        for light in range(7 - heavy)
    )


def vertex_degrees(
    instance: MarkedInstance,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    c00, c01, c10, c11 = instance.cells
    return (
        (c00.heavy + c01.heavy, c00.light + c01.light),
        (c10.heavy + c11.heavy, c10.light + c11.light),
        (c00.heavy + c10.heavy, c00.light + c10.light),
        (c01.heavy + c11.heavy, c01.light + c11.light),
    )


def connected(instance: MarkedInstance) -> bool:
    # A 2x2 bipartite support graph on all four vertices is connected exactly
    # when at least three of its four possible endpoint cells are occupied.
    return sum(cell.total > 0 for cell in instance.cells) >= 3


def retained_by_b5(instance: MarkedInstance) -> bool:
    degrees = vertex_degrees(instance)
    if any(heavy > 3 or light > 6 - heavy for heavy, light in degrees):
        return False
    totals = tuple(heavy + light for heavy, light in degrees)
    if 6 not in totals:
        return False
    if not connected(instance):
        return False
    if max(heavy for heavy, _light in degrees) + max(
        light for _heavy, light in degrees
    ) < 7:
        return False
    if all(total == 6 for total in totals):
        heavy_degrees = {heavy for heavy, _light in degrees}
        if len(heavy_degrees) == 1:
            return False
    return True


def transformed_cells(
    cells: tuple[Cell, Cell, Cell, Cell],
    row_order: tuple[int, int],
    column_order: tuple[int, int],
    transpose: bool,
) -> tuple[Cell, Cell, Cell, Cell]:
    output: list[Cell] = []
    for new_row in range(2):
        for new_column in range(2):
            if transpose:
                old_row = column_order[new_column]
                old_column = row_order[new_row]
            else:
                old_row = row_order[new_row]
                old_column = column_order[new_column]
            output.append(cells[2 * old_row + old_column])
    return (output[0], output[1], output[2], output[3])


def canonical_cells(
    cells: tuple[Cell, Cell, Cell, Cell],
) -> tuple[Cell, Cell, Cell, Cell]:
    candidates = [
        transformed_cells(cells, rows, columns, transpose)
        for rows in ((0, 1), (1, 0))
        for columns in ((0, 1), (1, 0))
        for transpose in (False, True)
    ]
    return min(candidates)


def enumerate_domain() -> Iterator[MarkedInstance]:
    options = cell_options()
    for cells in itertools.product(options, repeat=4):
        instance = MarkedInstance((cells[0], cells[1], cells[2], cells[3]))
        if retained_by_b5(instance):
            yield instance


def expand_edges(instance: MarkedInstance) -> tuple[Edge, ...]:
    edges: list[Edge] = []
    for cell_index, cell in enumerate(instance.cells):
        left, right = divmod(cell_index, 2)
        for _parallel in range(cell.heavy):
            edges.append(Edge(len(edges), left, right, True))
        for _parallel in range(cell.light):
            edges.append(Edge(len(edges), left, right, False))
    return tuple(edges)


def local_three_bins(
    edges: Sequence[Edge],
) -> dict[str, list[list[int]]]:
    """Construct the B.1 packing: H+L pairs, then two lights per empty bin."""

    output: dict[str, list[list[int]]] = {}
    for side in ("L", "R"):
        for vertex in range(2):
            incident = [
                edge
                for edge in edges
                if (edge.left if side == "L" else edge.right) == vertex
            ]
            heavy = [edge.edge_id for edge in incident if edge.heavy]
            light = [edge.edge_id for edge in incident if not edge.heavy]
            bins: list[list[int]] = [[] for _index in range(3)]
            for index, edge_id in enumerate(heavy):
                bins[index].append(edge_id)
            light_index = 0
            for index in range(len(heavy)):
                if light_index < len(light):
                    bins[index].append(light[light_index])
                    light_index += 1
            for index in range(len(heavy), 3):
                for _slot in range(2):
                    if light_index < len(light):
                        bins[index].append(light[light_index])
                        light_index += 1
            if light_index != len(light):
                raise AssertionError(f"B.1 packing construction failed at {side}{vertex}")
            output[f"{side}{vertex}"] = bins
    return output


def allowed_colour(
    edge: Edge,
    colour: int,
    total_loads: list[list[list[int]]],
    heavy_loads: list[list[list[int]]],
) -> bool:
    for side_index, vertex in ((0, edge.left), (1, edge.right)):
        if total_loads[side_index][vertex][colour] >= 2:
            return False
        if edge.heavy and heavy_loads[side_index][vertex][colour] >= 1:
            return False
    return True


def find_five_colouring(edges: Sequence[Edge]) -> tuple[tuple[int, ...] | None, int]:
    """Primary deterministic DFS, with global colour symmetry removed."""

    order = sorted(
        edges,
        key=lambda edge: (
            not edge.heavy,
            -sum(
                other.left == edge.left or other.right == edge.right
                for other in edges
            ),
            edge.edge_id,
        ),
    )
    total_loads = [[[0] * COLOUR_COUNT for _vertex in range(2)] for _side in range(2)]
    heavy_loads = [[[0] * COLOUR_COUNT for _vertex in range(2)] for _side in range(2)]
    assignment = [-1] * len(edges)
    nodes = 0

    def visit(position: int, used_colours: int) -> tuple[int, ...] | None:
        nonlocal nodes
        nodes += 1
        if position == len(order):
            return tuple(assignment)
        edge = order[position]
        colour_limit = min(COLOUR_COUNT, used_colours + 1)
        for colour in range(colour_limit):
            if not allowed_colour(edge, colour, total_loads, heavy_loads):
                continue
            for side_index, vertex in ((0, edge.left), (1, edge.right)):
                total_loads[side_index][vertex][colour] += 1
                if edge.heavy:
                    heavy_loads[side_index][vertex][colour] += 1
            assignment[edge.edge_id] = colour
            found = visit(position + 1, max(used_colours, colour + 1))
            if found is not None:
                return found
            assignment[edge.edge_id] = -1
            for side_index, vertex in ((0, edge.left), (1, edge.right)):
                total_loads[side_index][vertex][colour] -= 1
                if edge.heavy:
                    heavy_loads[side_index][vertex][colour] -= 1
        return None

    return (visit(0, 0), nodes)


def independent_uncolourability_backtracker(
    edges: Sequence[Edge],
    deadline: float,
) -> tuple[str, tuple[int, ...] | None, int]:
    """Independent MRV backtracker, used only if the primary DFS finds none."""

    total_loads = [[[0] * COLOUR_COUNT for _vertex in range(2)] for _side in range(2)]
    heavy_loads = [[[0] * COLOUR_COUNT for _vertex in range(2)] for _side in range(2)]
    assignment = [-1] * len(edges)
    unassigned = {edge.edge_id for edge in edges}
    edge_by_id = {edge.edge_id: edge for edge in edges}
    nodes = 0

    def visit() -> tuple[int, ...] | None:
        nonlocal nodes
        nodes += 1
        if nodes % 4096 == 0 and time.monotonic() >= deadline:
            raise TimeoutError
        if not unassigned:
            return tuple(assignment)
        choices: list[tuple[int, int, list[int]]] = []
        for edge_id in unassigned:
            edge = edge_by_id[edge_id]
            colours = [
                colour
                for colour in range(COLOUR_COUNT)
                if allowed_colour(edge, colour, total_loads, heavy_loads)
            ]
            choices.append((len(colours), edge_id, colours))
        _count, edge_id, colours = min(choices)
        if not colours:
            return None
        edge = edge_by_id[edge_id]
        unassigned.remove(edge_id)
        for colour in colours:
            for side_index, vertex in ((0, edge.left), (1, edge.right)):
                total_loads[side_index][vertex][colour] += 1
                if edge.heavy:
                    heavy_loads[side_index][vertex][colour] += 1
            assignment[edge_id] = colour
            found = visit()
            if found is not None:
                return found
            assignment[edge_id] = -1
            for side_index, vertex in ((0, edge.left), (1, edge.right)):
                total_loads[side_index][vertex][colour] -= 1
                if edge.heavy:
                    heavy_loads[side_index][vertex][colour] -= 1
        unassigned.add(edge_id)
        return None

    try:
        colouring = visit()
    except TimeoutError:
        return ("UNKNOWN", None, nodes)
    if colouring is None:
        return ("UNSAT", None, nodes)
    return ("SAT", colouring, nodes)


def verify_colouring(edges: Sequence[Edge], colouring: Sequence[int]) -> bool:
    if len(edges) != len(colouring):
        return False
    for side in ("L", "R"):
        for vertex in range(2):
            incident = [
                edge
                for edge in edges
                if (edge.left if side == "L" else edge.right) == vertex
            ]
            for colour in range(COLOUR_COUNT):
                selected = [
                    edge for edge in incident if colouring[edge.edge_id] == colour
                ]
                if len(selected) > 2:
                    return False
                if sum(edge.heavy for edge in selected) > 1:
                    return False
    return all(0 <= colour < COLOUR_COUNT for colour in colouring)


def verify_local_bins(
    edges: Sequence[Edge],
    bins: dict[str, list[list[int]]],
) -> bool:
    edge_by_id = {edge.edge_id: edge for edge in edges}
    for side in ("L", "R"):
        for vertex in range(2):
            key = f"{side}{vertex}"
            expected = {
                edge.edge_id
                for edge in edges
                if (edge.left if side == "L" else edge.right) == vertex
            }
            flattened = [edge_id for local_bin in bins[key] for edge_id in local_bin]
            if set(flattened) != expected or len(flattened) != len(expected):
                return False
            for local_bin in bins[key]:
                load_fifths = sum(
                    3 if edge_by_id[edge_id].heavy else 2 for edge_id in local_bin
                )
                if load_fifths > 5:
                    return False
    return True


def witness_json(
    instance: MarkedInstance,
    edges: Sequence[Edge],
    bins: dict[str, list[list[int]]],
    independent_nodes: int,
) -> dict[str, object]:
    return {
        "schema": "weighted-clos-marked-b5-counterexample-v1",
        "weights": {"heavy": "3/5", "light": "2/5"},
        "instance_id": instance.instance_id,
        "edges": [
            {
                "id": edge.edge_id,
                "left": f"L{edge.left}",
                "right": f"R{edge.right}",
                "mark": "heavy" if edge.heavy else "light",
                "weight": "3/5" if edge.heavy else "2/5",
            }
            for edge in edges
        ],
        "local_three_bins": bins,
        "independent_backtracker_nodes": independent_nodes,
    }


def exhaust_2x2(total_seconds: float) -> dict[str, object]:
    started = time.monotonic()
    deadline = started + total_seconds
    options = cell_options()
    scanned = len(options) ** 4
    retained_by_edges: Counter[int] = Counter()
    orbit_keys: set[tuple[Cell, Cell, Cell, Cell]] = set()
    orbit_edges: dict[tuple[Cell, Cell, Cell, Cell], int] = {}
    status_counts: Counter[str] = Counter()
    status_by_edges: dict[int, Counter[str]] = {}
    coverage = hashlib.sha256()
    retained = 0
    total_nodes = 0
    max_nodes = 0
    candidate_witness: dict[str, object] | None = None
    stop_reason = "domain exhausted"

    for instance in enumerate_domain():
        if time.monotonic() >= deadline:
            stop_reason = "total time limit"
            break
        retained += 1
        retained_by_edges[instance.edge_count] += 1
        key = canonical_cells(instance.cells)
        orbit_keys.add(key)
        orbit_edges[key] = instance.edge_count
        edges = expand_edges(instance)
        bins = local_three_bins(edges)
        if not verify_local_bins(edges, bins):
            raise AssertionError(f"invalid local bins for {instance.instance_id}")
        colouring, nodes = find_five_colouring(edges)
        total_nodes += nodes
        max_nodes = max(max_nodes, nodes)
        if colouring is not None:
            if not verify_colouring(edges, colouring):
                raise AssertionError(f"invalid colouring for {instance.instance_id}")
            status = "SAT_5_COLOURING"
            coverage.update(instance.instance_id.encode("ascii"))
            coverage.update(b"|")
            coverage.update(",".join(str(colour) for colour in colouring).encode("ascii"))
            coverage.update(b"\n")
        else:
            independent_status, independent_colouring, independent_nodes = (
                independent_uncolourability_backtracker(edges, deadline)
            )
            if independent_status == "SAT":
                if independent_colouring is None or not verify_colouring(
                    edges, independent_colouring
                ):
                    raise AssertionError("independent backtracker returned invalid SAT")
                status = "INTERNAL_DISAGREEMENT"
            elif independent_status == "UNKNOWN":
                status = "UNKNOWN"
            else:
                # UNSAT refers specifically to the exact five-colouring CSP.
                # Under B.1 this is precisely a marked counterexample.
                status = "UNSAT_5_COLOURING"
                candidate_witness = witness_json(
                    instance, edges, bins, independent_nodes
                )
            status_counts[status] += 1
            status_by_edges.setdefault(instance.edge_count, Counter())[status] += 1
            stop_reason = (
                "candidate or disagreement found"
                if status != "UNKNOWN"
                else "independent checker time limit"
            )
            break
        status_counts[status] += 1
        status_by_edges.setdefault(instance.edge_count, Counter())[status] += 1

    symmetry_by_edges = Counter(orbit_edges.values())
    complete = stop_reason == "domain exhausted"
    return {
        "schema": "weighted-clos-marked-b5-search-v1",
        "status": (
            "NO_COUNTEREXAMPLE_IN_FRONTIER"
            if complete and candidate_witness is None
            else "UNKNOWN"
            if candidate_witness is None
            else "COUNTEREXAMPLE_FOUND"
        ),
        "frontier": {
            "shape": "2x2",
            "labeled_domain_scanned": scanned,
            "filters": [
                "B.1 at every vertex",
                "connected with no isolates",
                "some vertex degree six",
                "B.5 max-heavy-degree + max-light-degree >= 7",
                "nonconstant heavy degree when 6-regular",
            ],
            "retained_labeled_instances": retained,
            "retained_labeled_by_edge_count": dict(sorted(retained_by_edges.items())),
            "symmetry": (
                "independent row/column swaps and bipartition transpose; "
                "reporting only, not search pruning"
            ),
            "symmetry_reduced_instances": len(orbit_keys),
            "symmetry_reduced_by_edge_count": dict(sorted(symmetry_by_edges.items())),
            "frontier_exhaustive": complete,
        },
        "status_counts": dict(status_counts),
        "status_counts_by_edge_count": {
            str(edge_count): dict(counts)
            for edge_count, counts in sorted(status_by_edges.items())
        },
        "search": {
            "five_colours": COLOUR_COUNT,
            "primary": "restricted-growth deterministic exact backtracking",
            "independent_candidate_checker": "MRV exact backtracking",
            "total_backtracking_nodes": total_nodes,
            "maximum_nodes_for_one_instance": max_nodes,
            "coverage_sha256": coverage.hexdigest(),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stop_reason": stop_reason,
        },
        "witness": candidate_witness,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--total-seconds", type=float, default=220.0)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not 0 < args.total_seconds <= 235:
        parser.error("--total-seconds must be in (0,235]")
    payload = exhaust_2x2(args.total_seconds)
    output = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(output)
    else:
        args.output.write_text(output, encoding="utf-8")
        print(
            json.dumps(
                {"event": "result_written", "path": str(args.output.resolve())},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
    return 0 if payload["status"] != "COUNTEREXAMPLE_FOUND" else 2


if __name__ == "__main__":
    raise SystemExit(main())
