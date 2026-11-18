#!/usr/bin/env python3
"""Independent audit helpers for saved hypercube-routing experiments.

This module deliberately does not import ``routing``.  Its certificate checker
uses only the JSON witness data and the definition of a bidirected hypercube.
The optional alternate solver uses a Boolean degree formulation (pure
cardinality constraints) instead of the original arithmetic-flow encoding.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from time import monotonic
from typing import Any


def _validate_permutation(dimension: int, permutation: object) -> list[int]:
    if not isinstance(dimension, int) or dimension < 0:
        raise ValueError("dimension must be a nonnegative integer")
    if not isinstance(permutation, list):
        raise ValueError("permutation must be a JSON list")
    order = 1 << dimension
    if len(permutation) != order or any(
        not isinstance(value, int) for value in permutation
    ):
        raise ValueError("wrong permutation length or noninteger entry")
    if sorted(permutation) != list(range(order)):
        raise ValueError("not a permutation of the cube vertices")
    return permutation


def _distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def verify_certificate(record: dict[str, Any]) -> dict[str, int]:
    """Validate a SAT record without consulting its formula or solver."""
    dimension = record.get("dimension")
    permutation = _validate_permutation(dimension, record.get("permutation"))
    if "total_hamming_distance" in record and record["total_hamming_distance"] != sum(
        _distance(source, target) for source, target in enumerate(permutation)
    ):
        raise ValueError("recorded total_hamming_distance is incorrect")
    if (
        "directed_arc_count" in record
        and record["directed_arc_count"] != dimension * (1 << dimension)
    ):
        raise ValueError("recorded directed_arc_count is incorrect")
    paths = record.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("SAT record has no path map")
    order = 1 << dimension
    expected_keys = {str(source) for source in range(order)}
    if set(paths) != expected_keys:
        raise ValueError("path-map keys are not exactly the sources")

    used: dict[tuple[int, int], int] = {}
    used_count = 0
    for source, target in enumerate(permutation):
        path = paths[str(source)]
        if not isinstance(path, list) or not path:
            raise ValueError(f"source {source}: path is absent or empty")
        if any(not isinstance(vertex, int) for vertex in path):
            raise ValueError(f"source {source}: noninteger vertex")
        if path[0] != source or path[-1] != target:
            raise ValueError(f"source {source}: wrong endpoints")
        if len(set(path)) != len(path):
            raise ValueError(f"source {source}: repeated vertex")
        if source == target and path != [source]:
            raise ValueError(f"source {source}: fixed point uses an arc")
        if record.get("shortest_only") and len(path) - 1 != _distance(source, target):
            raise ValueError(f"source {source}: not shortest")
        for tail, head in zip(path, path[1:]):
            if not (0 <= tail < order and 0 <= head < order):
                raise ValueError(f"source {source}: vertex outside cube")
            if _distance(tail, head) != 1:
                raise ValueError(f"source {source}: non-cube arc {(tail, head)}")
            if (tail, head) in used:
                raise ValueError(
                    f"directed arc {(tail, head)} shared by {used[(tail, head)]} and {source}"
                )
            used[(tail, head)] = source
            used_count += 1
    return {"sources": order, "used_directed_arcs": used_count}


def _load_object(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_text())
    if not isinstance(parsed, dict):
        raise ValueError(f"{path}: JSON top level is not an object")
    return parsed


def audit_saved_certificates(results_dir: Path) -> dict[str, Any]:
    result_files = sorted(results_dir.glob("*.result.json"))
    outcomes: list[dict[str, Any]] = []
    checked_file_sats = 0
    for result_path in result_files:
        record = _load_object(result_path)
        status = record.get("status")
        outcome: dict[str, Any] = {"file": result_path.name, "status": status}
        if status == "sat":
            instance_name = result_path.name.removesuffix(".result.json") + ".instance.json"
            instance = _load_object(results_dir / instance_name)
            if (
                record.get("dimension") != instance.get("dimension")
                or record.get("permutation") != instance.get("permutation")
            ):
                raise ValueError(f"{result_path.name}: mismatch with {instance_name}")
            outcome.update(verify_certificate(record))
            checked_file_sats += 1
        elif status not in {"unknown", "unsat"}:
            raise ValueError(f"{result_path.name}: unexpected status {status!r}")
        outcomes.append(outcome)

    summary = _load_object(results_dir / "summary.json")
    summary_sats = 0
    for record in summary.get("records", []):
        if not isinstance(record, dict):
            raise ValueError("summary has a non-object record")
        if record.get("status") == "sat":
            verify_certificate(record)
            summary_sats += 1

    status_counts = Counter(str(item["status"]) for item in outcomes)
    return {
        "checker": "independent_verify.py (stdlib JSON/cube validator; no routing import)",
        "result_files": len(result_files),
        "status_counts": dict(sorted(status_counts.items())),
        "sat_certificates_checked_in_result_files": checked_file_sats,
        "sat_certificates_checked_in_summary": summary_sats,
        "non_sat_records": [item for item in outcomes if item["status"] != "sat"],
        "all_checked_certificates_valid": True,
    }


def alternate_boolean_degree_solve(
    dimension: int, permutation: list[int], timeout_seconds: float
) -> dict[str, Any]:
    """Solve with a pure-Boolean degree encoding and the QF_FD engine.

    For an active commodity, a source has exactly one outgoing and no incoming
    selected arc; a target has exactly one incoming and no outgoing; and every
    other vertex has either degree pair (0,0) or (1,1).  A selected support is
    hence a source-target path plus optional directed cycles.  This is an exact
    formulation of unrestricted routing, not a path-length restriction.
    """
    import z3

    permutation = _validate_permutation(dimension, permutation)
    order = 1 << dimension
    arcs = tuple(
        (tail, tail ^ (1 << coordinate))
        for coordinate in range(dimension)
        for tail in range(order)
    )
    active = sorted(
        (source for source, target in enumerate(permutation) if source != target),
        key=lambda source: (-_distance(source, permutation[source]), source),
    )
    # ``SolverFor`` retains finite-domain cardinality constraints for the
    # dedicated QF_FD engine.  The eager ``qffd`` tactic expanded this instance
    # too aggressively on this host, so use the direct engine instead.
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=round(timeout_seconds * 1000))
    variables: dict[tuple[int, int, int], z3.BoolRef] = {}
    outgoing: dict[tuple[int, int], list[z3.BoolRef]] = {}
    incoming: dict[tuple[int, int], list[z3.BoolRef]] = {}
    for source in active:
        for tail, head in arcs:
            variable = z3.Bool(f"audit_x_{source}_{tail}_{head}")
            variables[(source, tail, head)] = variable
            outgoing.setdefault((source, tail), []).append(variable)
            incoming.setdefault((source, head), []).append(variable)

    def exactly(values: list[z3.BoolRef], number: int) -> z3.BoolRef:
        return z3.PbEq([(value, 1) for value in values], number)

    for source in active:
        target = permutation[source]
        for vertex in range(order):
            ins = incoming[(source, vertex)]
            outs = outgoing[(source, vertex)]
            solver.add(z3.AtMost(*ins, 1), z3.AtMost(*outs, 1))
            if vertex == source:
                solver.add(exactly(outs, 1), exactly(ins, 0))
            elif vertex == target:
                solver.add(exactly(outs, 0), exactly(ins, 1))
            else:
                solver.add(exactly(outs, 1) == exactly(ins, 1))

    for tail, head in arcs:
        solver.add(
            z3.AtMost(
                *(variables[(source, tail, head)] for source in active), 1
            )
        )

    started = monotonic()
    outcome = solver.check()
    elapsed = monotonic() - started
    rendered: dict[str, Any] = {
        "method": "QF_FD Boolean degree encoding, coordinate-major arcs, demand-descending commodities",
        "z3_version": z3.get_version_string(),
        "dimension": dimension,
        "permutation": permutation,
        "timeout_seconds": timeout_seconds,
        "elapsed_seconds": elapsed,
        "status": str(outcome),
        "reason_unknown": solver.reason_unknown() if outcome == z3.unknown else None,
    }
    if outcome != z3.sat:
        return rendered

    model = solver.model()
    paths: dict[str, list[int]] = {}
    for source, target in enumerate(permutation):
        if source == target:
            paths[str(source)] = [source]
            continue
        successor: dict[int, int] = {}
        for tail, head in arcs:
            if z3.is_true(model.eval(variables[(source, tail, head)], model_completion=True)):
                successor[tail] = head
        path = [source]
        while path[-1] != target:
            if path[-1] not in successor or len(path) > order:
                raise RuntimeError("alternate model has no simple source-target path")
            path.append(successor[path[-1]])
        paths[str(source)] = path
    rendered["paths"] = paths
    verify_certificate(rendered)
    return rendered


def randomized_shortest_path_search(
    dimension: int, permutation: list[int], timeout_seconds: float, seed: int
) -> dict[str, Any]:
    """Seek a certificate by selecting whole shortest paths, without a solver.

    This is deliberately only a constructive sub-search.  A returned witness
    proves unrestricted routability; exhaustion says nothing about it.
    """
    permutation = _validate_permutation(dimension, permutation)
    order = 1 << dimension
    path_options: dict[int, list[tuple[int, ...]]] = {}
    for source, target in enumerate(permutation):
        differing = [bit for bit in range(dimension) if (source ^ target) & (1 << bit)]
        options: list[tuple[int, ...]] = []
        for bit_order in itertools.permutations(differing):
            path = [source]
            for bit in bit_order:
                path.append(path[-1] ^ (1 << bit))
            options.append(tuple(path))
        path_options[source] = options or [(source,)]

    rng = random.Random(seed)
    started = monotonic()
    trials = 0
    best_assigned = 0
    active = [source for source in range(order) if source != permutation[source]]
    while monotonic() - started < timeout_seconds:
        trials += 1
        used: set[tuple[int, int]] = set()
        selected: dict[int, tuple[int, ...]] = {
            source: (source,) for source in range(order) if source == permutation[source]
        }
        pending = set(active)
        while pending:
            viable_by_source: dict[int, list[tuple[int, ...]]] = {}
            for source in pending:
                viable = [
                    path
                    for path in path_options[source]
                    if all(arc not in used for arc in zip(path, path[1:]))
                ]
                if not viable:
                    viable_by_source = {}
                    break
                viable_by_source[source] = viable
            if not viable_by_source:
                break
            source = min(
                viable_by_source,
                key=lambda item: (len(viable_by_source[item]), rng.random()),
            )
            candidates = viable_by_source[source]
            # Prefer a random candidate from the least frequently available
            # directed arcs, retaining random restarts rather than claiming
            # completeness for this path-selection search.
            arc_frequency: Counter[tuple[int, int]] = Counter(
                arc
                for paths in viable_by_source.values()
                for path in paths
                for arc in zip(path, path[1:])
            )
            candidates.sort(
                key=lambda path: (
                    sum(arc_frequency[arc] for arc in zip(path, path[1:])),
                    rng.random(),
                )
            )
            path = candidates[0]
            selected[source] = path
            used.update(zip(path, path[1:]))
            pending.remove(source)
        best_assigned = max(best_assigned, len(selected))
        if not pending:
            paths = {str(source): list(selected[source]) for source in range(order)}
            rendered: dict[str, Any] = {
                "method": "randomized whole-shortest-path packing with dynamic MRV",
                "dimension": dimension,
                "permutation": permutation,
                "shortest_only": True,
                "timeout_seconds": timeout_seconds,
                "seed": seed,
                "elapsed_seconds": monotonic() - started,
                "trials": trials,
                "status": "sat",
                "paths": paths,
            }
            verify_certificate(rendered)
            return rendered
    return {
        "method": "randomized whole-shortest-path packing with dynamic MRV",
        "dimension": dimension,
        "permutation": permutation,
        "shortest_only": True,
        "timeout_seconds": timeout_seconds,
        "seed": seed,
        "elapsed_seconds": monotonic() - started,
        "trials": trials,
        "best_assigned_sources": best_assigned,
        "status": "inconclusive",
        "interpretation": "bounded heuristic exhaustion is not an UNSAT result",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("certificates")
    audit.add_argument("results_dir", type=Path)
    audit.add_argument("--output", type=Path, required=True)
    solve = subparsers.add_parser("alternate-solve")
    solve.add_argument("instance", type=Path)
    solve.add_argument("--timeout-seconds", type=float, default=240.0)
    solve.add_argument("--output", type=Path, required=True)
    paths = subparsers.add_parser("path-search")
    paths.add_argument("instance", type=Path)
    paths.add_argument("--timeout-seconds", type=float, default=240.0)
    paths.add_argument("--seed", type=int, default=1989)
    paths.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "certificates":
        payload = audit_saved_certificates(args.results_dir)
    elif args.command == "alternate-solve":
        if not 0 < args.timeout_seconds < 300:
            parser.error("timeout must be in (0, 300) seconds")
        instance = _load_object(args.instance)
        payload = alternate_boolean_degree_solve(
            instance.get("dimension"), instance.get("permutation"), args.timeout_seconds
        )
    else:
        if not 0 < args.timeout_seconds < 300:
            parser.error("timeout must be in (0, 300) seconds")
        instance = _load_object(args.instance)
        payload = randomized_shortest_path_search(
            instance.get("dimension"),
            instance.get("permutation"),
            args.timeout_seconds,
            args.seed,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in payload.items() if key != "paths"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
