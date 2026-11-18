#!/usr/bin/env python3
"""Deterministic bounded exact search for an n=2 weighted Clos counterexample.

This enumerates connected bipartite multigraph multiplicity matrices and exact
rational edge-weight grids. It emits a witness only after a complete exact
three-colour search proves that particular instance non-colourable.

The search is finite but normally resource-bounded. Its JSON summary records
the exact topology and weight-assignment frontier actually covered.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class SearchEdge:
    cell: int
    left: int
    right: int
    weight: Fraction


class DeadlineReached(RuntimeError):
    pass


class NodeLimitReached(RuntimeError):
    pass


def rational_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build_grid(denominator_min: int, denominator_max: int) -> list[Fraction]:
    # Visit raw denominator frontiers in order. Within each denominator, try
    # values near 1/2 first and alternate heavy/light. Reduced duplicates are
    # removed, and the endpoint 1 is left until last.
    result: list[Fraction] = []
    seen: set[Fraction] = set()
    for denominator in range(denominator_min, denominator_max + 1):
        values = [Fraction(numerator, denominator) for numerator in range(1, denominator)]
        values.sort(
            key=lambda value: (
                abs(value - Fraction(1, 2)),
                0 if value > Fraction(1, 2) else 1,
                value.numerator,
            )
        )
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
    result.append(Fraction(1))
    return result


def multiplicity_vectors(cells: int, edges: int, maximum: int) -> Iterator[tuple[int, ...]]:
    current = [0] * cells

    def generate(position: int, remaining: int) -> Iterator[tuple[int, ...]]:
        if position == cells:
            if remaining == 0:
                yield tuple(current)
            return
        cells_left = cells - position - 1
        low = max(0, remaining - cells_left * maximum)
        high = min(maximum, remaining)
        for value in range(low, high + 1):
            current[position] = value
            yield from generate(position + 1, remaining - value)

    yield from generate(0, edges)


def has_no_isolates(matrix: tuple[int, ...], left: int, right: int) -> bool:
    return all(sum(matrix[i * right + j] for j in range(right)) > 0 for i in range(left)) and all(
        sum(matrix[i * right + j] for i in range(left)) > 0 for j in range(right)
    )


def is_connected(matrix: tuple[int, ...], left: int, right: int) -> bool:
    seen_left = {0}
    seen_right: set[int] = set()
    changed = True
    while changed:
        changed = False
        for i in tuple(seen_left):
            for j in range(right):
                if matrix[i * right + j] and j not in seen_right:
                    seen_right.add(j)
                    changed = True
        for j in tuple(seen_right):
            for i in range(left):
                if matrix[i * right + j] and i not in seen_left:
                    seen_left.add(i)
                    changed = True
    return len(seen_left) == left and len(seen_right) == right


def is_canonical(matrix: tuple[int, ...], left: int, right: int) -> bool:
    """Canonical under independent permutations of the two bipartition sides."""

    best = matrix
    for rows in itertools.permutations(range(left)):
        for columns in itertools.permutations(range(right)):
            candidate = tuple(matrix[i * right + j] for i in rows for j in columns)
            if candidate < best:
                return False
    return True


def topology_edges(matrix: tuple[int, ...], left: int, right: int) -> list[tuple[int, int, int]]:
    result = []
    for i in range(left):
        for j in range(right):
            cell = i * right + j
            result.extend((cell, i, j) for _ in range(matrix[cell]))
    return result


def pack_two(weights_and_ids: list[tuple[Fraction, int]]) -> list[list[int]] | None:
    ordered = sorted(weights_and_ids, key=lambda item: (-item[0], item[1]))
    bins: list[list[int]] = [[], []]
    loads = [Fraction(0), Fraction(0)]

    def place(position: int) -> bool:
        if position == len(ordered):
            return True
        weight, identifier = ordered[position]
        tried: set[Fraction] = set()
        for bin_number in range(2):
            if loads[bin_number] in tried or loads[bin_number] + weight > 1:
                continue
            tried.add(loads[bin_number])
            loads[bin_number] += weight
            bins[bin_number].append(identifier)
            if place(position + 1):
                return True
            bins[bin_number].pop()
            loads[bin_number] -= weight
        return False

    return [list(bin_edges) for bin_edges in bins] if place(0) else None


def all_local_bins(
    edges: list[SearchEdge], left: int, right: int
) -> tuple[dict[str, list[list[int]]], bool] | None:
    result: dict[str, list[list[int]]] = {}
    exact_two = False
    for side, count in (("L", left), ("R", right)):
        for vertex in range(count):
            incident = [
                (edge.weight, index)
                for index, edge in enumerate(edges)
                if (edge.left if side == "L" else edge.right) == vertex
            ]
            bins = pack_two(incident)
            if bins is None:
                return None
            result[f"{side}:{side.lower()}{vertex}"] = bins
            if sum((weight for weight, _ in incident), Fraction(0)) > 1:
                exact_two = True
    return result, exact_two


def colouring_status(
    edges: list[SearchEdge],
    left: int,
    right: int,
    node_limit: int | None,
    deadline: float,
) -> tuple[str, int]:
    """Return colorable/noncolorable/unknown and explored search nodes."""

    loads_left = [[Fraction(0)] * 3 for _ in range(left)]
    loads_right = [[Fraction(0)] * 3 for _ in range(right)]
    colours = [-1] * len(edges)
    unassigned = set(range(len(edges)))
    failed: set[tuple[int, tuple[tuple[Fraction, ...], ...]]] = set()
    nodes = 0

    def state(mask: int) -> tuple[int, tuple[tuple[Fraction, ...], ...]]:
        columns = []
        for colour in range(3):
            columns.append(
                tuple(loads_left[i][colour] for i in range(left))
                + tuple(loads_right[j][colour] for j in range(right))
            )
        return mask, tuple(sorted(columns))

    def options(index: int) -> list[int]:
        edge = edges[index]
        return [
            colour
            for colour in range(3)
            if loads_left[edge.left][colour] + edge.weight <= 1
            and loads_right[edge.right][colour] + edge.weight <= 1
        ]

    def visit(mask: int) -> bool:
        nonlocal nodes
        nodes += 1
        if nodes & 1023 == 0 and time.monotonic() >= deadline:
            raise DeadlineReached
        if node_limit is not None and nodes > node_limit:
            raise NodeLimitReached
        if not unassigned:
            return True
        snapshot = state(mask)
        if snapshot in failed:
            return False
        ranked = []
        for index in unassigned:
            available = options(index)
            if not available:
                failed.add(snapshot)
                return False
            edge = edges[index]
            ranked.append((len(available), -edge.weight, edge.cell, index, available))
        _, _, _, index, available = min(ranked)

        used = {colour for colour in colours if colour >= 0}
        unused = sorted(set(range(3)) - used)
        representative = unused[0] if unused else None
        available = [colour for colour in available if colour in used or colour == representative]

        unassigned.remove(index)
        edge = edges[index]
        for colour in available:
            colours[index] = colour
            loads_left[edge.left][colour] += edge.weight
            loads_right[edge.right][colour] += edge.weight
            if visit(mask ^ (1 << index)):
                return True
            loads_left[edge.left][colour] -= edge.weight
            loads_right[edge.right][colour] -= edge.weight
            colours[index] = -1
        unassigned.add(index)
        failed.add(snapshot)
        return False

    try:
        colourable = visit((1 << len(edges)) - 1)
    except (DeadlineReached, NodeLimitReached):
        return "unknown", nodes
    return ("colorable" if colourable else "noncolorable"), nodes


def witness_json(
    edges: list[SearchEdge],
    left: int,
    right: int,
    local_bins: dict[str, list[list[int]]],
    metadata: dict[str, object],
) -> dict[str, object]:
    identifiers = [f"e{index}" for index in range(len(edges))]
    rendered_bins = {
        vertex: [[identifiers[index] for index in bin_edges] for bin_edges in bins]
        for vertex, bins in local_bins.items()
    }
    return {
        "schema": "weighted-clos-n2-v1",
        "left_vertices": [f"l{i}" for i in range(left)],
        "right_vertices": [f"r{j}" for j in range(right)],
        "edges": [
            {
                "id": identifiers[index],
                "left": f"l{edge.left}",
                "right": f"r{edge.right}",
                "weight": rational_text(edge.weight),
            }
            for index, edge in enumerate(edges)
        ],
        "local_bins": rendered_bins,
        "claim": {"n": 2, "colors": 3},
        "search": metadata,
    }


def write_witness(path: Path | None, witness: dict[str, object]) -> None:
    text = json.dumps(witness, indent=2, sort_keys=True) + "\n"
    if path is None:
        print(text, end="")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", type=int, default=3)
    parser.add_argument("--right", type=int, default=3)
    parser.add_argument("--edges", type=int, default=8)
    parser.add_argument("--max-multiplicity", type=int, default=2)
    parser.add_argument("--den-min", type=int, default=3)
    parser.add_argument("--den-max", type=int, default=12)
    parser.add_argument(
        "--grid-limit",
        type=int,
        default=12,
        help="use the first N deterministically ordered grid values; 0 means the full grid",
    )
    parser.add_argument("--max-topologies", type=int, default=100)
    parser.add_argument("--max-assignments", type=int, default=250000)
    parser.add_argument("--max-colour-nodes", type=int, default=1000000)
    parser.add_argument("--seconds", type=float, default=240.0)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--no-canonical", action="store_true")
    parser.add_argument("--allow-unmixed", action="store_true")
    args = parser.parse_args()
    for name in ("left", "right", "edges", "max_multiplicity", "max_topologies", "max_assignments"):
        if getattr(args, name) < 1:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.den_min < 2 or args.den_max < args.den_min:
        parser.error("require 2 <= --den-min <= --den-max")
    if args.grid_limit < 0 or args.max_colour_nodes < 0 or args.seconds <= 0:
        parser.error("grid/node limits must be nonnegative and --seconds positive")
    if args.edges > args.left * args.right * args.max_multiplicity:
        parser.error("edge count exceeds the multiplicity-matrix capacity")
    return args


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    deadline = started + args.seconds
    full_grid = build_grid(args.den_min, args.den_max)
    grid = full_grid[: args.grid_limit] if args.grid_limit else full_grid
    has_light = any(value < Fraction(1, 2) for value in grid)
    has_heavy = any(value > Fraction(1, 2) for value in grid)
    if not args.allow_unmixed and not (has_light and has_heavy):
        raise SystemExit("selected grid must contain weights on both sides of 1/2")

    counters = {
        "multiplicity_matrices_generated": 0,
        "connected_nonisolated_topologies": 0,
        "canonical_topologies": 0,
        "topologies_started": 0,
        "topologies_completed": 0,
        "weight_assignments_completed": 0,
        "locally_two_packable": 0,
        "exact_n2_instances": 0,
        "colourable_instances": 0,
        "colour_unknown_instances": 0,
        "colour_search_nodes": 0,
    }
    stop_reason = "exhausted"
    witness: dict[str, object] | None = None
    frontier: dict[str, object] = {
        "current_topology_matrix": None,
        "last_completed_topology_matrix": None,
        "last_completed_assignment_matrix": None,
        "last_completed_weights": None,
    }

    try:
        for matrix in multiplicity_vectors(
            args.left * args.right, args.edges, args.max_multiplicity
        ):
            counters["multiplicity_matrices_generated"] += 1
            if time.monotonic() >= deadline:
                raise DeadlineReached
            if not has_no_isolates(matrix, args.left, args.right) or not is_connected(
                matrix, args.left, args.right
            ):
                continue
            counters["connected_nonisolated_topologies"] += 1
            if not args.no_canonical and not is_canonical(matrix, args.left, args.right):
                continue
            counters["canonical_topologies"] += 1
            if counters["topologies_started"] >= args.max_topologies:
                stop_reason = "max_topologies"
                break
            counters["topologies_started"] += 1
            frontier["current_topology_matrix"] = list(matrix)

            bare_edges = topology_edges(matrix, args.left, args.right)
            chosen: list[SearchEdge] = []
            incident_weights: dict[tuple[str, int], list[tuple[Fraction, int]]] = {
                **{("L", i): [] for i in range(args.left)},
                **{("R", j): [] for j in range(args.right)},
            }
            last_grid_index_by_cell: dict[int, int] = {}

            def assign(position: int, saw_light: bool, saw_heavy: bool) -> None:
                nonlocal witness, stop_reason
                if witness is not None:
                    return
                if counters["weight_assignments_completed"] >= args.max_assignments:
                    stop_reason = "max_assignments"
                    raise NodeLimitReached
                if time.monotonic() >= deadline:
                    raise DeadlineReached
                if position == len(bare_edges):
                    counters["weight_assignments_completed"] += 1
                    frontier["last_completed_assignment_matrix"] = list(matrix)
                    frontier["last_completed_weights"] = [
                        rational_text(edge.weight) for edge in chosen
                    ]
                    if not args.allow_unmixed and not (saw_light and saw_heavy):
                        return
                    packed = all_local_bins(chosen, args.left, args.right)
                    if packed is None:
                        return
                    local_bins, exact_two = packed
                    counters["locally_two_packable"] += 1
                    if not exact_two:
                        return
                    counters["exact_n2_instances"] += 1
                    status, nodes = colouring_status(
                        chosen,
                        args.left,
                        args.right,
                        args.max_colour_nodes or None,
                        deadline,
                    )
                    counters["colour_search_nodes"] += nodes
                    if status == "colorable":
                        counters["colourable_instances"] += 1
                    elif status == "unknown":
                        counters["colour_unknown_instances"] += 1
                    else:
                        metadata = {
                            "matrix": list(matrix),
                            "grid": [rational_text(value) for value in grid],
                            "counters_at_discovery": dict(counters),
                        }
                        witness = witness_json(
                            chosen, args.left, args.right, local_bins, metadata
                        )
                    return

                cell, left_vertex, right_vertex = bare_edges[position]
                minimum_index = last_grid_index_by_cell.get(cell, 0)
                previous = last_grid_index_by_cell.get(cell)
                for grid_index in range(minimum_index, len(grid)):
                    weight = grid[grid_index]
                    edge = SearchEdge(cell, left_vertex, right_vertex, weight)
                    edge_index = len(chosen)
                    chosen.append(edge)
                    incident_weights[("L", left_vertex)].append((weight, edge_index))
                    incident_weights[("R", right_vertex)].append((weight, edge_index))
                    last_grid_index_by_cell[cell] = grid_index
                    left_ok = pack_two(incident_weights[("L", left_vertex)]) is not None
                    right_ok = pack_two(incident_weights[("R", right_vertex)]) is not None
                    if left_ok and right_ok:
                        assign(
                            position + 1,
                            saw_light or weight < Fraction(1, 2),
                            saw_heavy or weight > Fraction(1, 2),
                        )
                    incident_weights[("L", left_vertex)].pop()
                    incident_weights[("R", right_vertex)].pop()
                    chosen.pop()
                    if witness is not None:
                        return
                if previous is None:
                    last_grid_index_by_cell.pop(cell, None)
                else:
                    last_grid_index_by_cell[cell] = previous

            assign(0, False, False)
            if witness is not None:
                stop_reason = "witness_found"
                break
            counters["topologies_completed"] += 1
            frontier["last_completed_topology_matrix"] = list(matrix)
    except DeadlineReached:
        stop_reason = "deadline"
    except NodeLimitReached:
        if stop_reason == "exhausted":
            stop_reason = "max_assignments"

    elapsed = time.monotonic() - started
    if witness is not None:
        write_witness(args.output, witness)
        summary = {
            "witness_found": True,
            "output": str(args.output) if args.output else "stdout",
            "elapsed_seconds": round(elapsed, 6),
            "stop_reason": stop_reason,
            "counters": counters,
            "frontier": frontier,
        }
        print(json.dumps(summary, sort_keys=True), file=sys.stderr)
        return 0

    summary = {
        "witness_found": False,
        "elapsed_seconds": round(elapsed, 6),
        "stop_reason": stop_reason,
        "parameters": {
            "left": args.left,
            "right": args.right,
            "edges": args.edges,
            "max_multiplicity": args.max_multiplicity,
            "denominator_range_raw": [args.den_min, args.den_max],
            "grid": [rational_text(value) for value in grid],
            "grid_is_full_for_denominator_range": len(grid) == len(full_grid),
            "canonical_topologies": not args.no_canonical,
            "require_mixed_sides_of_half": not args.allow_unmixed,
        },
        "counters": counters,
        "frontier": frontier,
        "interpretation": (
            "Finite null result only. Coverage ends exactly at the counters and stop_reason above; "
            "it is not a proof for larger graphs, other rational weights, or interrupted assignments."
        ),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
