"""Independent stdlib audit of ``slack_six.py`` output.

This checker deliberately does not import the routing solver.  It reconstructs
the exhaustive Q_3 Delta=6 population, recomputes cube-automorphism orbits,
and validates every stored path certificate directly from cube adjacency.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Sequence


def distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def displacement(permutation: Sequence[int]) -> int:
    return sum(distance(source, target)
               for source, target in enumerate(permutation))


def complement_after(permutation: Sequence[int], dimension: int) -> tuple[int, ...]:
    mask = (1 << dimension) - 1
    return tuple(mask ^ target for target in permutation)


def check_paths(
    dimension: int,
    permutation: Sequence[int],
    paths: dict[str, list[int]],
) -> int:
    order = 1 << dimension
    if sorted(permutation) != list(range(order)):
        raise ValueError("target list is not a permutation")
    if set(paths) != {str(source) for source in range(order)}:
        raise ValueError("path keys are not exactly the cube vertices")
    used: set[tuple[int, int]] = set()
    for source, target in enumerate(permutation):
        path = paths[str(source)]
        if not path or path[0] != source or path[-1] != target:
            raise ValueError("wrong or missing path endpoint")
        if len(set(path)) != len(path):
            raise ValueError("path repeats a vertex")
        if len(path) - 1 != distance(source, target):
            raise ValueError("path is not shortest")
        for arc in zip(path, path[1:]):
            if distance(*arc) != 1:
                raise ValueError("path uses a non-cube arc")
            if arc in used:
                raise ValueError("directed arc is used twice")
            used.add(arc)
    return len(used)


def map_vertex(
    vertex: int,
    coordinate_permutation: Sequence[int],
    translation: int,
) -> int:
    mapped = translation
    for source_coordinate, target_coordinate in enumerate(
        coordinate_permutation
    ):
        if vertex & (1 << source_coordinate):
            mapped ^= 1 << target_coordinate
    return mapped


def canonical_conjugate(permutation: Sequence[int], dimension: int) -> tuple[int, ...]:
    order = 1 << dimension
    candidates: list[tuple[int, ...]] = []
    for coordinate_permutation in itertools.permutations(range(dimension)):
        for translation in range(order):
            vertex_map = tuple(
                map_vertex(vertex, coordinate_permutation, translation)
                for vertex in range(order)
            )
            conjugate = [0] * order
            for source, target in enumerate(permutation):
                conjugate[vertex_map[source]] = vertex_map[target]
            candidates.append(tuple(conjugate))
    return min(candidates)


def lift(
    local_permutation: Sequence[int],
    ambient_dimension: int,
) -> tuple[int, ...]:
    result = list(range(1 << ambient_dimension))
    result[:8] = local_permutation
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())

    expected = {
        tuple(permutation)
        for permutation in itertools.permutations(range(8))
        if displacement(permutation) == 6
    }
    records = payload["q3_all_delta_six_certificates"]
    recorded = {tuple(record["tau"]) for record in records}
    if len(records) != len(recorded):
        raise ValueError("duplicate exhaustive Q3 certificate")
    if recorded != expected:
        raise ValueError("stored Q3 population is not exactly Delta=6")

    certificates_checked = 0
    arcs_checked = 0
    for record in records:
        tau = tuple(record["tau"])
        sigma = complement_after(tau, 3)
        if record["status"] != "sat" or tuple(record["sigma"]) != sigma:
            raise ValueError("bad Q3 solver record")
        arcs_checked += check_paths(3, sigma, record["paths"])
        certificates_checked += 1

    orbit_keys = {canonical_conjugate(permutation, 3) for permutation in expected}
    stored_orbits = payload["orbits"]
    stored_representatives = {
        tuple(record["representative"]) for record in stored_orbits
    }
    if stored_representatives != orbit_keys:
        raise ValueError("stored orbit representatives are incomplete or noncanonical")

    for orbit in stored_orbits:
        representative = tuple(orbit["representative"])
        for dimension, path_key in (
            (3, "q3_example_paths"),
            (4, "q4_lift_example_paths"),
            (5, "q5_lift_example_paths"),
        ):
            tau = representative if dimension == 3 else lift(
                representative, dimension
            )
            sigma = complement_after(tau, dimension)
            arcs_checked += check_paths(dimension, sigma, orbit[path_key])
            certificates_checked += 1

    for record in payload["structured_q5_multifiber"]:
        tau = tuple(record["tau"])
        if displacement(tau) != 6:
            raise ValueError("structured Q5 tau does not have Delta=6")
        sigma = complement_after(tau, 5)
        if record["status"] != "sat" or tuple(record["sigma"]) != sigma:
            raise ValueError("bad structured Q5 record")
        arcs_checked += check_paths(5, sigma, record["paths"])
        certificates_checked += 1

    result = {
        "checker": "audit_slack_six.py (stdlib only; no routing import)",
        "q3_delta_six_population": len(expected),
        "q3_cube_automorphism_orbits": len(orbit_keys),
        "certificates_checked": certificates_checked,
        "directed_arc_occurrences_checked": arcs_checked,
        "all_checks_passed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
