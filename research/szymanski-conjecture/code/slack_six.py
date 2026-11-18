"""Enumerate and test the total-displacement-six near-antipodal family.

For a permutation ``tau`` of a cube, its total Hamming displacement is

    Delta(tau) = sum_x hamming(x, tau(x)).

The corresponding near-antipodal permutation is ``sigma = A o tau``, where
``A`` complements every bit.  This script:

* exhaustively classifies the Delta=6 permutations of Q_3 under cube
  automorphisms (translations and coordinate permutations);
* exhaustively checks shortest-path routability for every such Q_3
  permutation using ``routing.solve_routing``;
* lifts one representative of each local orbit to a single active fiber in
  Q_4 and Q_5 and checks those shortest-path instances too.

The Q_4 and Q_5 checks are experiments, not an exhaustive classification of
all placements of several active fibers.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from time import monotonic
from typing import Iterable, Sequence

from routing import solve_routing, verify_paths


def hamming(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def total_displacement(permutation: Sequence[int]) -> int:
    return sum(hamming(source, target) for source, target in enumerate(permutation))


def nontrivial_cycles(permutation: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    """Return nontrivial directed cycles, canonically rotated but not reversed."""
    seen: set[int] = set()
    cycles: list[tuple[int, ...]] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle: list[int] = []
        vertex = start
        while vertex not in seen:
            seen.add(vertex)
            cycle.append(vertex)
            vertex = permutation[vertex]
        if len(cycle) <= 1:
            continue
        minimum_index = cycle.index(min(cycle))
        rotated = cycle[minimum_index:] + cycle[:minimum_index]
        cycles.append(tuple(rotated))
    return tuple(sorted(cycles))


def cycle_cost(cycle: Sequence[int]) -> int:
    return sum(hamming(cycle[index], cycle[(index + 1) % len(cycle)])
               for index in range(len(cycle)))


def cycle_metric_signature(permutation: Sequence[int]) -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Coarse cycle type: length and lexicographically canonical cyclic side lengths."""
    signatures: list[tuple[int, tuple[int, ...]]] = []
    for cycle in nontrivial_cycles(permutation):
        side_lengths = tuple(
            hamming(cycle[index], cycle[(index + 1) % len(cycle)])
            for index in range(len(cycle))
        )
        rotations = [
            side_lengths[index:] + side_lengths[:index]
            for index in range(len(side_lengths))
        ]
        signatures.append((len(cycle), min(rotations)))
    return tuple(sorted(signatures))


def permute_bits(vertex: int, coordinate_image: Sequence[int]) -> int:
    result = 0
    for old_coordinate, new_coordinate in enumerate(coordinate_image):
        if vertex & (1 << old_coordinate):
            result |= 1 << new_coordinate
    return result


def cube_automorphisms(dimension: int) -> Iterable[tuple[int, ...]]:
    """Yield all vertex maps induced by a translation and coordinate permutation."""
    order = 1 << dimension
    for coordinate_image in itertools.permutations(range(dimension)):
        linear = tuple(
            permute_bits(vertex, coordinate_image) for vertex in range(order)
        )
        for translation in range(order):
            yield tuple(vertex ^ translation for vertex in linear)


def conjugate(permutation: Sequence[int], vertex_map: Sequence[int]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[vertex_map[source]] = vertex_map[target]
    return tuple(result)


def orbit_key(permutation: Sequence[int], dimension: int) -> tuple[int, ...]:
    return min(conjugate(permutation, automorphism)
               for automorphism in cube_automorphisms(dimension))


def near_antipodal(permutation: Sequence[int], dimension: int) -> tuple[int, ...]:
    mask = (1 << dimension) - 1
    return tuple(mask ^ target for target in permutation)


def lift_single_fiber(
    local_permutation: Sequence[int],
    dimension: int,
    *,
    local_dimension: int = 3,
    fiber: int = 0,
) -> tuple[int, ...]:
    """Extend a local permutation by the identity outside one inactive fiber."""
    if dimension < local_dimension:
        raise ValueError("ambient dimension must contain the local cube")
    local_order = 1 << local_dimension
    if len(local_permutation) != local_order:
        raise ValueError("wrong local permutation size")
    inactive_dimension = dimension - local_dimension
    if not 0 <= fiber < (1 << inactive_dimension):
        raise ValueError("fiber index out of range")

    order = 1 << dimension
    result = list(range(order))
    offset = fiber << local_dimension
    for source, target in enumerate(local_permutation):
        result[offset | source] = offset | target
    return tuple(result)


def serialize_paths(paths: dict[int, tuple[int, ...]] | None) -> dict[str, list[int]] | None:
    if paths is None:
        return None
    return {str(source): list(path) for source, path in sorted(paths.items())}


def permutation_from_cycles(
    dimension: int,
    cycles: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    result = list(range(1 << dimension))
    used: set[int] = set()
    for cycle in cycles:
        if len(cycle) < 2:
            raise ValueError("cycles must be nontrivial")
        if any(vertex in used for vertex in cycle):
            raise ValueError("cycles must have disjoint supports")
        used.update(cycle)
        for index, source in enumerate(cycle):
            result[source] = cycle[(index + 1) % len(cycle)]
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        raise SystemExit("--timeout-seconds must be positive")
    timeout_ms = round(args.timeout_seconds * 1000)

    dimension = 3
    order = 1 << dimension
    delta_six = [
        tuple(permutation)
        for permutation in itertools.permutations(range(order))
        if total_displacement(permutation) == 6
    ]

    orbit_members: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for permutation in delta_six:
        orbit_members[orbit_key(permutation, dimension)].append(permutation)

    started = monotonic()
    q3_statuses: Counter[str] = Counter()
    q3_example_paths: dict[tuple[int, ...], dict[int, tuple[int, ...]]] = {}
    q3_certificates = []
    for permutation in delta_six:
        sigma = near_antipodal(permutation, dimension)
        result = solve_routing(
            dimension,
            sigma,
            shortest_only=True,
            timeout_ms=timeout_ms,
        )
        q3_statuses[result.status] += 1
        if result.paths is not None:
            verify_paths(
                dimension,
                sigma,
                result.paths,
                shortest_only=True,
            )
            key = orbit_key(permutation, dimension)
            q3_example_paths.setdefault(key, result.paths)
        q3_certificates.append(
            {
                "tau": list(permutation),
                "sigma": list(sigma),
                "status": result.status,
                "paths": serialize_paths(result.paths),
            }
        )

    lifted: dict[str, Counter[str]] = {}
    lifted_examples: dict[tuple[int, tuple[int, ...]], dict[int, tuple[int, ...]]] = {}
    for ambient_dimension in (4, 5):
        statuses: Counter[str] = Counter()
        for representative in sorted(orbit_members):
            tau = lift_single_fiber(representative, ambient_dimension)
            sigma = near_antipodal(tau, ambient_dimension)
            result = solve_routing(
                ambient_dimension,
                sigma,
                shortest_only=True,
                timeout_ms=timeout_ms,
            )
            statuses[result.status] += 1
            if result.paths is not None:
                verify_paths(
                    ambient_dimension,
                    sigma,
                    result.paths,
                    shortest_only=True,
                )
                lifted_examples[(ambient_dimension, representative)] = result.paths
        lifted[f"q{ambient_dimension}"] = statuses

    # These deliberately put the nontrivial cycles in different fibers of the
    # coordinates they change.  They probe cases not represented by a
    # single-fiber lift, while remaining only a small structured sample.
    structured_q5_cycles = {
        "three_edge_transpositions_three_fibers": ((0, 1), (2, 3), (4, 5)),
        "edge_plus_distance_two_transposition": ((8, 9), (0, 6)),
        "edge_plus_length_two_path_three_cycle": ((8, 9), (0, 2, 6)),
        "edge_plus_square": ((8, 9), (0, 2, 6, 4)),
    }
    structured_q5 = []
    structured_q5_statuses: Counter[str] = Counter()
    for name, cycles in structured_q5_cycles.items():
        tau = permutation_from_cycles(5, cycles)
        if total_displacement(tau) != 6:
            raise RuntimeError(f"bad structured Delta=6 instance: {name}")
        sigma = near_antipodal(tau, 5)
        result = solve_routing(
            5,
            sigma,
            shortest_only=True,
            timeout_ms=timeout_ms,
        )
        structured_q5_statuses[result.status] += 1
        if result.paths is not None:
            verify_paths(5, sigma, result.paths, shortest_only=True)
        structured_q5.append(
            {
                "name": name,
                "cycles": [list(cycle) for cycle in cycles],
                "tau": list(tau),
                "sigma": list(sigma),
                "status": result.status,
                "elapsed_seconds": result.elapsed_seconds,
                "paths": serialize_paths(result.paths),
            }
        )

    orbit_records = []
    for representative, members in sorted(orbit_members.items()):
        cycles = nontrivial_cycles(representative)
        orbit_records.append(
            {
                "representative": list(representative),
                "cycles": [list(cycle) for cycle in cycles],
                "cycle_costs": [cycle_cost(cycle) for cycle in cycles],
                "metric_signature": [
                    [length, list(side_lengths)]
                    for length, side_lengths in cycle_metric_signature(representative)
                ],
                "orbit_size_within_delta_six": len(members),
                "q3_example_paths": serialize_paths(q3_example_paths.get(representative)),
                "q4_lift_example_paths": serialize_paths(
                    lifted_examples.get((4, representative))
                ),
                "q5_lift_example_paths": serialize_paths(
                    lifted_examples.get((5, representative))
                ),
            }
        )

    payload = {
        "scope": {
            "q3_delta_six_exhaustive": True,
            "q4_q5_single_fiber_orbit_lifts_only": True,
            "timeout_seconds_per_instance": args.timeout_seconds,
        },
        "counts": {
            "q3_delta_six_permutations": len(delta_six),
            "q3_cube_automorphism_orbits": len(orbit_members),
            "q3_metric_signatures": {
                repr(signature): count
                for signature, count in sorted(
                    Counter(cycle_metric_signature(permutation)
                            for permutation in delta_six).items(),
                    key=lambda item: repr(item[0]),
                )
            },
        },
        "solver_results": {
            "q3_all_delta_six": dict(sorted(q3_statuses.items())),
            **{
                key: dict(sorted(statuses.items()))
                for key, statuses in sorted(lifted.items())
            },
            "q5_structured_multifiber": dict(
                sorted(structured_q5_statuses.items())
            ),
            "elapsed_seconds": monotonic() - started,
        },
        "q3_all_delta_six_certificates": q3_certificates,
        "orbits": orbit_records,
        "structured_q5_multifiber": structured_q5,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    compact = {
        key: value
        for key, value in payload.items()
        if key not in {
            "orbits",
            "q3_all_delta_six_certificates",
            "structured_q5_multifiber",
        }
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
