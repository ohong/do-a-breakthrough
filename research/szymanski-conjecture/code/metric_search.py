#!/usr/bin/env python3
"""Bounded search for a directed-length dual obstruction.

For nonnegative directed-arc lengths ``l``, every arc-disjoint routing obeys

    sum_v dist_l(v, sigma(v)) <= sum_a l(a).

The left side is maximized over permutations by an assignment problem.  This
script samples exact integer lengths, computes exact shortest-path distances,
and solves that assignment with a dependency-free Hungarian algorithm.
"""

from __future__ import annotations

import argparse
import heapq
import json
import random
from pathlib import Path

from routing import cube_arcs


def all_pairs_distances(
    dimension: int, lengths: dict[tuple[int, int], int]
) -> list[list[int]]:
    order = 1 << dimension
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for (tail, head), length in lengths.items():
        if length < 0:
            raise ValueError("arc lengths must be nonnegative")
        adjacency[tail].append((head, length))

    result: list[list[int]] = []
    for source in range(order):
        distances = [10**30] * order
        distances[source] = 0
        queue = [(0, source)]
        while queue:
            distance, tail = heapq.heappop(queue)
            if distance != distances[tail]:
                continue
            for head, length in adjacency[tail]:
                candidate = distance + length
                if candidate < distances[head]:
                    distances[head] = candidate
                    heapq.heappush(queue, (candidate, head))
        result.append(distances)
    return result


def maximum_assignment(weights: list[list[int]]) -> tuple[int, list[int]]:
    """Exact O(n^3) Hungarian algorithm for a square integer matrix."""
    size = len(weights)
    if any(len(row) != size for row in weights):
        raise ValueError("assignment matrix must be square")
    maximum = max(max(row) for row in weights) if size else 0
    costs = [[maximum - weight for weight in row] for row in weights]

    u = [0] * (size + 1)
    v = [0] * (size + 1)
    matched_row = [0] * (size + 1)
    predecessor = [0] * (size + 1)
    for row in range(1, size + 1):
        matched_row[0] = row
        min_value = [10**30] * (size + 1)
        used = [False] * (size + 1)
        column = 0
        while True:
            used[column] = True
            current_row = matched_row[column]
            delta = 10**30
            next_column = 0
            for candidate_column in range(1, size + 1):
                if used[candidate_column]:
                    continue
                reduced = (
                    costs[current_row - 1][candidate_column - 1]
                    - u[current_row]
                    - v[candidate_column]
                )
                if reduced < min_value[candidate_column]:
                    min_value[candidate_column] = reduced
                    predecessor[candidate_column] = column
                if min_value[candidate_column] < delta:
                    delta = min_value[candidate_column]
                    next_column = candidate_column
            for candidate_column in range(size + 1):
                if used[candidate_column]:
                    u[matched_row[candidate_column]] += delta
                    v[candidate_column] -= delta
                else:
                    min_value[candidate_column] -= delta
            column = next_column
            if matched_row[column] == 0:
                break
        while True:
            next_column = predecessor[column]
            matched_row[column] = matched_row[next_column]
            column = next_column
            if column == 0:
                break

    permutation = [0] * size
    for column in range(1, size + 1):
        permutation[matched_row[column] - 1] = column - 1
    value = sum(weights[row][permutation[row]] for row in range(size))
    return value, permutation


def sampled_lengths(
    dimension: int, samples: int, seed: int
) -> list[tuple[str, dict[tuple[int, int], int]]]:
    arcs = cube_arcs(dimension)
    families: list[tuple[str, dict[tuple[int, int], int]]] = [
        ("uniform", {arc: 1 for arc in arcs})
    ]
    for coordinate in range(dimension):
        families.append(
            (
                f"coordinate-{coordinate}",
                {
                    (tail, head): int((tail ^ head).bit_length() - 1 == coordinate)
                    for tail, head in arcs
                },
            )
        )
    rng = random.Random(seed)
    for sample in range(samples):
        # Small integers retain an easy-to-audit exact certificate if a strict
        # inequality appears.  Zeros also explore sparse directed metrics.
        families.append(
            (
                f"random-{sample:04d}",
                {arc: rng.randrange(8) for arc in arcs},
            )
        )
    return families


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=5)
    parser.add_argument("--samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=1989)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    best: dict[str, object] | None = None
    strict: dict[str, object] | None = None
    for name, lengths in sampled_lengths(
        args.dimension, args.samples, args.seed
    ):
        distances = all_pairs_distances(args.dimension, lengths)
        demand, permutation = maximum_assignment(distances)
        capacity = sum(lengths.values())
        record = {
            "family": name,
            "demand_distance": demand,
            "total_arc_length": capacity,
            "gap": demand - capacity,
            "permutation": permutation,
            "arc_lengths": [
                [tail, head, lengths[(tail, head)]]
                for tail, head in cube_arcs(args.dimension)
            ],
        }
        if best is None or record["gap"] > best["gap"]:
            best = record
        if demand > capacity:
            strict = record
            break

    payload = {
        "dimension": args.dimension,
        "samples_requested": args.samples,
        "seed": args.seed,
        "strict_certificate_found": strict is not None,
        "certificate": strict,
        "best_sample": best,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({key: value for key, value in payload.items() if key != "best_sample"}))
    if best is not None:
        print(
            json.dumps(
                {
                    "best_family": best["family"],
                    "best_gap": best["gap"],
                    "best_demand_distance": best["demand_distance"],
                    "best_total_arc_length": best["total_arc_length"],
                }
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
