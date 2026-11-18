#!/usr/bin/env python3
"""Reproduce the bounded calibration and structured-candidate experiments."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

import z3

from routing import RoutingResult, hamming_distance, solve_routing


def antipodal(dimension: int) -> list[int]:
    mask = (1 << dimension) - 1
    return [source ^ mask for source in range(1 << dimension)]


def mutate_targets(
    permutation: list[int], swaps: list[tuple[int, int]]
) -> list[int]:
    result = permutation.copy()
    for left, right in swaps:
        result[left], result[right] = result[right], result[left]
    return result


def rotate_then_complement(dimension: int, amount: int) -> list[int]:
    mask = (1 << dimension) - 1
    result = []
    for source in range(1 << dimension):
        rotated = (
            ((source << amount) | (source >> (dimension - amount))) & mask
        )
        result.append(rotated ^ mask)
    return result


def random_antipodal_mutation(
    dimension: int, seed: int, swaps: int
) -> list[int]:
    rng = random.Random(seed)
    permutation = antipodal(dimension)
    for _ in range(swaps):
        left, right = rng.sample(range(1 << dimension), 2)
        permutation[left], permutation[right] = (
            permutation[right],
            permutation[left],
        )
    return permutation


def result_record(name: str, result: RoutingResult) -> dict[str, object]:
    return {
        "name": name,
        "dimension": result.dimension,
        "permutation": list(result.permutation),
        "total_hamming_distance": sum(
            hamming_distance(source, target)
            for source, target in enumerate(result.permutation)
        ),
        "directed_arc_count": result.dimension * (1 << result.dimension),
        "shortest_only": result.shortest_only,
        "status": result.status,
        "elapsed_seconds": result.elapsed_seconds,
        "reason_unknown": result.reason_unknown,
        "solver_statistics": result.solver_statistics,
        "paths": (
            {str(source): list(path) for source, path in result.paths.items()}
            if result.paths is not None
            else None
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    args = parser.parse_args()
    if not 0 < args.timeout_seconds <= 295:
        parser.error("timeout must be in (0, 295] seconds")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    work: list[tuple[str, int, list[int], bool]] = []
    for dimension in (1, 2):
        for index, permutation in enumerate(
            itertools.permutations(range(1 << dimension))
        ):
            work.append(
                (f"q{dimension}-exhaustive-{index:02d}", dimension, list(permutation), False)
            )
            work.append(
                (f"q{dimension}-exhaustive-{index:02d}-shortest", dimension, list(permutation), True)
            )

    for dimension in (3, 4):
        base = antipodal(dimension)
        structured = [
            ("identity", list(range(1 << dimension))),
            ("antipodal", base),
            ("antipodal-swap-01", mutate_targets(base, [(0, 1)])),
            (
                "antipodal-disjoint-swaps",
                mutate_targets(base, [(0, 1), (2, 3), (4, 5)]),
            ),
            ("rotate1-complement", rotate_then_complement(dimension, 1)),
            (
                "high-distance-random",
                random_antipodal_mutation(dimension, 1989 + dimension, 3),
            ),
        ]
        for name, permutation in structured:
            work.append((f"q{dimension}-{name}", dimension, permutation, False))
            work.append(
                (f"q{dimension}-{name}-shortest", dimension, permutation, True)
            )

    dimension = 5
    base = antipodal(dimension)
    candidates = [
        ("antipodal", base),
        ("antipodal-swap-01", mutate_targets(base, [(0, 1)])),
        (
            "antipodal-4cycle",
            mutate_targets(base, [(0, 1), (1, 2), (2, 3)]),
        ),
        (
            "antipodal-disjoint-swaps",
            mutate_targets(
                base, [(0, 1), (2, 3), (4, 5), (8, 9), (16, 17)]
            ),
        ),
        ("rotate1-complement", rotate_then_complement(dimension, 1)),
        ("rotate2-complement", rotate_then_complement(dimension, 2)),
        (
            "high-distance-random-a",
            random_antipodal_mutation(dimension, 1989, 7),
        ),
        (
            "high-distance-random-b",
            random_antipodal_mutation(dimension, 2001, 11),
        ),
    ]
    for name, permutation in candidates:
        work.append((f"q5-{name}", dimension, permutation, False))

    records: list[dict[str, object]] = []
    unrestricted_unsat = False
    for index, (name, dimension, permutation, shortest_only) in enumerate(work):
        print(f"[{index + 1}/{len(work)}] {name}", flush=True)
        result = solve_routing(
            dimension,
            permutation,
            shortest_only=shortest_only,
            timeout_ms=round(args.timeout_seconds * 1000),
            include_smt2=True,
        )
        record = result_record(name, result)
        records.append(record)
        instance_path = args.output_dir / f"{name}.instance.json"
        instance_path.write_text(
            json.dumps(
                {"dimension": dimension, "permutation": permutation}, indent=2
            )
            + "\n"
        )
        result_path = args.output_dir / f"{name}.result.json"
        result_path.write_text(json.dumps(record, indent=2) + "\n")
        if result.status == "unsat" and not shortest_only:
            smt2_path = args.output_dir / f"{name}.unsat.smt2"
            if result.smt2 is None:
                raise RuntimeError("missing SMT-LIB for unrestricted UNSAT")
            smt2_path.write_text(result.smt2)
            unrestricted_unsat = True
            print("STOP: unrestricted UNSAT candidate preserved", flush=True)
            break

    summary = {
        "z3_version": z3.get_version_string(),
        "timeout_seconds_per_instance": args.timeout_seconds,
        "planned_instances": len(work),
        "completed_instances": len(records),
        "unrestricted_unsat_found": unrestricted_unsat,
        "status_counts": {
            status: sum(record["status"] == status for record in records)
            for status in ("sat", "unsat", "unknown")
        },
        "records": records,
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "records"}))
    return 3 if unrestricted_unsat else 0


if __name__ == "__main__":
    raise SystemExit(main())
