#!/usr/bin/env python3
"""Exact CEGAR search for an n=3 Chung--Ross counterexample.

For a fixed bipartite multigraph the master chooses exact rational weights and
an explicit local packing into three unit bins at every vertex.  It additionally
enforces that at least one vertex has no packing into two bins, so the instance
parameter is exactly n=3.  The checker seeks a proper global five-colouring.
Every discovered colouring orbit is blocked until:

* ``SAT_WITNESS``: concrete weights have no five-colouring;
* ``UNSAT_TOPOLOGY``: no exact-n=3 weights on that topology defeat five colours;
* ``UNKNOWN``: a solver, iteration, or time limit was reached.

Topology surveys are sampled and make no completeness claim.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterator, Sequence

import z3

from search_cegar import (
    Edge,
    Topology,
    fraction_text,
    is_connected,
    model_fraction,
    permuted_matrix,
    sum_arith,
    topology_from_multiplicities,
    z3_fraction,
)


TARGET_N = 3
TARGET_COLOURS = 5
CAPACITY = Fraction(1)


@dataclass(frozen=True)
class SearchConfig:
    colour_count: int
    seed: int
    solver_timeout_ms: int
    topology_seconds: float
    max_iterations: int
    progress_every: int


@dataclass(frozen=True)
class Candidate:
    weights: tuple[Fraction, ...]
    local_bins: tuple[int, ...]


@dataclass(frozen=True)
class SearchResult:
    status: str
    topology_id: str
    iterations: int
    blocked_colourings: int
    elapsed_seconds: float
    reason: str
    witness: dict[str, object] | None

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "status": self.status,
            "topology_id": self.topology_id,
            "iterations": self.iterations,
            "blocked_colourings": self.blocked_colourings,
            "elapsed_seconds": round(self.elapsed_seconds, 6),
            "reason": self.reason,
        }
        if self.witness is not None:
            payload["witness"] = self.witness
        return payload


def vertices(topology: Topology) -> Iterator[tuple[str, int]]:
    for left in range(topology.left_count):
        yield ("L", left)
    for right in range(topology.right_count):
        yield ("R", right)


def two_bin_partitions(incident: Sequence[int]) -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    """All unordered two-bin partitions, fixing the first edge in bin zero."""

    if not incident:
        yield ((), ())
        return
    first = incident[0]
    remaining = incident[1:]
    for mask in range(1 << len(remaining)):
        bin_zero = [first]
        bin_one: list[int] = []
        for index, edge_id in enumerate(remaining):
            if mask & (1 << index):
                bin_one.append(edge_id)
            else:
                bin_zero.append(edge_id)
        yield (tuple(bin_zero), tuple(bin_one))


class N3CegarSearch:
    def __init__(self, topology: Topology, config: SearchConfig) -> None:
        self.topology = topology
        self.config = config
        self.master = z3.Solver()
        self.master.set("timeout", config.solver_timeout_ms)
        self.master.set("random_seed", config.seed)
        self.weights = tuple(z3.Real(f"w_{edge.edge_id}") for edge in topology.edges)
        self.local_bin_variables: list[z3.IntNumRef | z3.ArithRef] = []
        self.local_bin_offsets: dict[tuple[str, int, int], int] = {}
        self._add_master_constraints()

    def _add_master_constraints(self) -> None:
        for weight in self.weights:
            self.master.add(weight > 0, weight <= 1)

        vertices_not_two_packable: list[z3.BoolRef] = []
        for side, vertex in vertices(self.topology):
            incident = self.topology.incident_edges(side, vertex)
            if not incident:
                vertices_not_two_packable.append(z3.BoolVal(False))
                continue
            local_variables: list[z3.ArithRef] = []
            for edge_id in incident:
                variable = z3.Int(f"local_bin_{side}_{vertex}_{edge_id}")
                self.local_bin_offsets[(side, vertex, edge_id)] = len(
                    self.local_bin_variables
                )
                self.local_bin_variables.append(variable)
                local_variables.append(variable)
                self.master.add(variable >= 0, variable < TARGET_N)
            # Local bin names are symmetric, so every packing has a
            # representative in which its first incident edge is in bin zero.
            self.master.add(local_variables[0] == 0)
            for bin_index in range(TARGET_N):
                load = sum_arith(
                    [
                        z3.If(
                            variable == bin_index,
                            self.weights[edge_id],
                            z3.RealVal(0),
                        )
                        for variable, edge_id in zip(local_variables, incident)
                    ]
                )
                self.master.add(load <= 1)

            partition_failures: list[z3.BoolRef] = []
            for bin_zero, bin_one in two_bin_partitions(incident):
                load_zero = sum_arith([self.weights[edge_id] for edge_id in bin_zero])
                load_one = sum_arith([self.weights[edge_id] for edge_id in bin_one])
                partition_failures.append(z3.Or(load_zero > 1, load_one > 1))
            vertices_not_two_packable.append(z3.And(partition_failures))

        # At least one vertex has local bin number exactly three.  Every vertex
        # is already constrained to have an explicit three-bin packing.
        self.master.add(z3.Or(vertices_not_two_packable))

    def _candidate(self, model: z3.ModelRef) -> Candidate:
        weights = tuple(model_fraction(model, weight) for weight in self.weights)
        bins = tuple(
            model.evaluate(variable, model_completion=True).as_long()
            for variable in self.local_bin_variables
        )
        return Candidate(weights, bins)

    def _find_colouring(
        self,
        candidate: Candidate,
        remaining_ms: int,
    ) -> tuple[str, tuple[int, ...] | None, str]:
        checker = z3.Solver()
        checker.set(
            "timeout",
            max(1, min(self.config.solver_timeout_ms, remaining_ms)),
        )
        checker.set("random_seed", self.config.seed)
        colours = tuple(z3.Int(f"colour_{edge.edge_id}") for edge in self.topology.edges)
        for colour in colours:
            checker.add(colour >= 0, colour < self.config.colour_count)
        if colours:
            checker.add(colours[0] == 0)
        for side, vertex in vertices(self.topology):
            incident = self.topology.incident_edges(side, vertex)
            for colour_index in range(self.config.colour_count):
                load = sum_arith(
                    [
                        z3.If(
                            colours[edge_id] == colour_index,
                            z3_fraction(candidate.weights[edge_id]),
                            z3.RealVal(0),
                        )
                        for edge_id in incident
                    ]
                )
                checker.add(load <= 1)
        result = checker.check()
        if result == z3.sat:
            model = checker.model()
            return (
                "SAT",
                tuple(
                    model.evaluate(colour, model_completion=True).as_long()
                    for colour in colours
                ),
                "",
            )
        if result == z3.unsat:
            return ("UNSAT", None, "")
        return ("UNKNOWN", None, checker.reason_unknown())

    def _block_colouring(self, colouring: tuple[int, ...]) -> None:
        overloads: list[z3.BoolRef] = []
        for side, vertex in vertices(self.topology):
            incident = self.topology.incident_edges(side, vertex)
            for colour_index in range(self.config.colour_count):
                same_colour = [
                    self.weights[edge_id]
                    for edge_id in incident
                    if colouring[edge_id] == colour_index
                ]
                if same_colour:
                    overloads.append(sum_arith(same_colour) > 1)
        # Invalidity is invariant under globally permuting colour names.
        self.master.add(z3.Or(overloads))

    def _is_two_packable(
        self,
        incident: Sequence[int],
        weights: Sequence[Fraction],
    ) -> bool:
        for bin_zero, bin_one in two_bin_partitions(incident):
            load_zero = sum((weights[edge_id] for edge_id in bin_zero), Fraction(0))
            load_one = sum((weights[edge_id] for edge_id in bin_one), Fraction(0))
            if load_zero <= CAPACITY and load_one <= CAPACITY:
                return True
        return False

    def _self_check_local(self, candidate: Candidate) -> tuple[bool, list[str], str]:
        if any(weight <= 0 or weight > 1 for weight in candidate.weights):
            return (False, [], "weight outside (0,1]")
        exact_vertices: list[str] = []
        for side, vertex in vertices(self.topology):
            incident = self.topology.incident_edges(side, vertex)
            loads = [Fraction(0) for _index in range(TARGET_N)]
            for edge_id in incident:
                offset = self.local_bin_offsets[(side, vertex, edge_id)]
                bin_index = candidate.local_bins[offset]
                if not 0 <= bin_index < TARGET_N:
                    return (False, [], f"invalid local bin at {side}{vertex}")
                loads[bin_index] += candidate.weights[edge_id]
            if any(load > CAPACITY for load in loads):
                return (False, [], f"local three-bin overload at {side}{vertex}")
            if not self._is_two_packable(incident, candidate.weights):
                exact_vertices.append(f"{side}{vertex}")
        if not exact_vertices:
            return (False, [], "every vertex is two-bin-packable")
        return (True, exact_vertices, "")

    def _exhaustive_colouring(
        self,
        candidate: Candidate,
        deadline: float,
    ) -> tuple[bool | None, int, tuple[int, ...] | None]:
        order = sorted(
            range(self.topology.edge_count),
            key=lambda edge_id: (-candidate.weights[edge_id], edge_id),
        )
        assignment = [-1] * self.topology.edge_count
        loads: dict[tuple[str, int, int], Fraction] = {}
        nodes = 0

        def visit(position: int, used_colours: int) -> tuple[int, ...] | None:
            nonlocal nodes
            nodes += 1
            if nodes % 4096 == 0 and time.monotonic() >= deadline:
                raise TimeoutError
            if position == len(order):
                return tuple(assignment)
            edge_id = order[position]
            edge = self.topology.edges[edge_id]
            colour_limit = min(self.config.colour_count, used_colours + 1)
            for colour in range(colour_limit):
                left_key = ("L", edge.left, colour)
                right_key = ("R", edge.right, colour)
                old_left = loads.get(left_key, Fraction(0))
                old_right = loads.get(right_key, Fraction(0))
                new_left = old_left + candidate.weights[edge_id]
                new_right = old_right + candidate.weights[edge_id]
                if new_left > CAPACITY or new_right > CAPACITY:
                    continue
                loads[left_key] = new_left
                loads[right_key] = new_right
                assignment[edge_id] = colour
                found = visit(position + 1, max(used_colours, colour + 1))
                if found is not None:
                    return found
                assignment[edge_id] = -1
                loads[left_key] = old_left
                loads[right_key] = old_right
            return None

        try:
            colouring = visit(0, 0)
        except TimeoutError:
            return (None, nodes, None)
        return (colouring is not None, nodes, colouring)

    def _witness(
        self,
        candidate: Candidate,
        exact_vertices: Sequence[str],
        iteration: int,
        blocked: int,
        exhaustive_nodes: int,
    ) -> dict[str, object]:
        edge_payload = [
            {
                "id": edge.edge_id,
                "left": f"L{edge.left}",
                "right": f"R{edge.right}",
                "weight": fraction_text(candidate.weights[edge.edge_id]),
            }
            for edge in self.topology.edges
        ]
        local_bins: dict[str, list[list[int]]] = {}
        for side, vertex in vertices(self.topology):
            bins = [[] for _index in range(TARGET_N)]
            for edge_id in self.topology.incident_edges(side, vertex):
                offset = self.local_bin_offsets[(side, vertex, edge_id)]
                bins[candidate.local_bins[offset]].append(edge_id)
            local_bins[f"{side}{vertex}"] = bins
        return {
            "schema": "weighted-clos-counterexample-n3-v1",
            "target_n": TARGET_N,
            "global_colours": self.config.colour_count,
            "topology": {
                "left_count": self.topology.left_count,
                "right_count": self.topology.right_count,
                "multiplicity_matrix": [
                    list(
                        self.topology.multiplicities[
                            left * self.topology.right_count :
                            (left + 1) * self.topology.right_count
                        ]
                    )
                    for left in range(self.topology.left_count)
                ],
            },
            "edges": edge_payload,
            "local_three_bins": local_bins,
            "vertices_not_two_bin_packable": list(exact_vertices),
            "search": {
                "seed": self.config.seed,
                "cegar_iterations": iteration,
                "colouring_orbits_blocked": blocked,
                "exhaustive_self_check_nodes": exhaustive_nodes,
            },
        }

    def run(self) -> SearchResult:
        started = time.monotonic()
        deadline = started + self.config.topology_seconds
        blocked = 0
        for iteration in range(1, self.config.max_iterations + 1):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return self._result(
                    "UNKNOWN", iteration - 1, blocked, started, "topology time limit"
                )
            self.master.set(
                "timeout",
                max(1, min(self.config.solver_timeout_ms, int(remaining * 1000))),
            )
            master_result = self.master.check()
            if master_result == z3.unsat:
                return self._result(
                    "UNSAT_TOPOLOGY",
                    iteration - 1,
                    blocked,
                    started,
                    "exact master exhausted all locally three-packable exact-n=3 weights",
                )
            if master_result == z3.unknown:
                return self._result(
                    "UNKNOWN",
                    iteration - 1,
                    blocked,
                    started,
                    f"master solver: {self.master.reason_unknown()}",
                )
            candidate = self._candidate(self.master.model())
            local_ok, exact_vertices, local_reason = self._self_check_local(candidate)
            if not local_ok:
                return self._result(
                    "INTERNAL_ERROR",
                    iteration,
                    blocked,
                    started,
                    local_reason,
                )
            checker_status, colouring, checker_reason = self._find_colouring(
                candidate,
                max(1, int((deadline - time.monotonic()) * 1000)),
            )
            if checker_status == "UNKNOWN":
                return self._result(
                    "UNKNOWN",
                    iteration,
                    blocked,
                    started,
                    f"colour checker: {checker_reason}",
                )
            if checker_status == "UNSAT":
                colourable, nodes, found = self._exhaustive_colouring(
                    candidate, deadline
                )
                if colourable is None:
                    return self._result(
                        "UNKNOWN",
                        iteration,
                        blocked,
                        started,
                        "exhaustive exact checker timed out after SMT UNSAT",
                    )
                if colourable:
                    return self._result(
                        "INTERNAL_ERROR",
                        iteration,
                        blocked,
                        started,
                        f"exact checker found missed colouring {found}",
                    )
                return self._result(
                    "SAT_WITNESS",
                    iteration,
                    blocked,
                    started,
                    (
                        "SMT checker and exact Fraction backtracker found no "
                        f"{self.config.colour_count}-colouring"
                    ),
                    self._witness(
                        candidate,
                        exact_vertices,
                        iteration,
                        blocked,
                        nodes,
                    ),
                )
            if colouring is None:
                return self._result(
                    "INTERNAL_ERROR",
                    iteration,
                    blocked,
                    started,
                    "checker SAT without colouring",
                )
            self._block_colouring(colouring)
            blocked += 1
            if (
                self.config.progress_every > 0
                and iteration % self.config.progress_every == 0
            ):
                print(
                    json.dumps(
                        {
                            "event": "n3_cegar_progress",
                            "topology_id": self.topology.topology_id,
                            "iteration": iteration,
                            "blocked": blocked,
                            "elapsed_seconds": round(time.monotonic() - started, 3),
                        },
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
        return self._result(
            "UNKNOWN",
            self.config.max_iterations,
            blocked,
            started,
            "CEGAR iteration limit",
        )

    def _result(
        self,
        status: str,
        iterations: int,
        blocked: int,
        started: float,
        reason: str,
        witness: dict[str, object] | None = None,
    ) -> SearchResult:
        return SearchResult(
            status=status,
            topology_id=self.topology.topology_id,
            iterations=iterations,
            blocked_colourings=blocked,
            elapsed_seconds=time.monotonic() - started,
            reason=reason,
            witness=witness,
        )


def run_controls(config: SearchConfig) -> dict[str, object]:
    topology = topology_from_multiplicities(1, 1, (3,))
    positive_config = SearchConfig(
        colour_count=2,
        seed=config.seed,
        solver_timeout_ms=config.solver_timeout_ms,
        topology_seconds=config.topology_seconds,
        max_iterations=config.max_iterations,
        progress_every=0,
    )
    negative_config = SearchConfig(
        colour_count=TARGET_COLOURS,
        seed=config.seed,
        solver_timeout_ms=config.solver_timeout_ms,
        topology_seconds=config.topology_seconds,
        max_iterations=config.max_iterations,
        progress_every=0,
    )
    positive = N3CegarSearch(topology, positive_config).run()
    negative = N3CegarSearch(topology, negative_config).run()
    return {
        "mode": "controls",
        "passed": (
            positive.status == "SAT_WITNESS"
            and negative.status == "UNSAT_TOPOLOGY"
        ),
        "positive_control": {
            "description": (
                "three parallel edges, exact local bin number three, synthetic "
                "two-colour checker"
            ),
            **positive.to_json(),
        },
        "negative_control": {
            "description": (
                "the same topology under the target five colours is always colourable"
            ),
            **negative.to_json(),
        },
    }


def canonical_key(topology: Topology) -> tuple[int, ...]:
    best = topology.multiplicities
    for left_permutation in itertools.permutations(range(topology.left_count)):
        for right_permutation in itertools.permutations(range(topology.right_count)):
            candidate = permuted_matrix(
                topology.multiplicities,
                topology.left_count,
                topology.right_count,
                left_permutation,
                right_permutation,
            )
            if candidate < best:
                best = candidate
    return best


def random_connected_topology(
    left_count: int,
    right_count: int,
    edge_count: int,
    max_multiplicity: int,
    generator: random.Random,
) -> Topology:
    cells = [
        (left, right)
        for left in range(left_count)
        for right in range(right_count)
    ]
    generator.shuffle(cells)
    parent = list(range(left_count + right_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    chosen: list[int] = []
    for left, right in cells:
        left_root = find(left)
        right_root = find(left_count + right)
        if left_root == right_root:
            continue
        parent[right_root] = left_root
        chosen.append(left * right_count + right)
        if len(chosen) == left_count + right_count - 1:
            break
    multiplicities = [0] * (left_count * right_count)
    for cell in chosen:
        multiplicities[cell] = 1
    extra_slots = [
        cell
        for cell in range(len(multiplicities))
        for _copy in range(max_multiplicity - multiplicities[cell])
    ]
    generator.shuffle(extra_slots)
    remaining = edge_count - len(chosen)
    if remaining < 0 or remaining > len(extra_slots):
        raise ValueError("edge count incompatible with connected bounded multiplicities")
    for cell in extra_slots[:remaining]:
        multiplicities[cell] += 1
    topology = topology_from_multiplicities(
        left_count, right_count, multiplicities
    )
    if not is_connected(topology):
        raise RuntimeError("spanning-tree sampler produced disconnected topology")
    return topology


def topology_score(topology: Topology) -> tuple[int, int, int]:
    degrees = [
        len(topology.incident_edges(side, vertex))
        for side, count in (
            ("L", topology.left_count),
            ("R", topology.right_count),
        )
        for vertex in range(count)
    ]
    partition_constraints = sum(1 << max(0, degree - 1) for degree in degrees)
    triple_opportunities = sum(
        math.comb(degree, 3) for degree in degrees if degree >= 3
    )
    return (partition_constraints, triple_opportunities, max(degrees))


def sampled_topologies(
    seed: int,
    pool_per_bucket: int,
    selected_per_bucket: int,
    max_multiplicity: int,
) -> tuple[list[Topology], dict[str, object]]:
    generator = random.Random(seed)
    # Ngo--Vu, Theorem 4.1 / Corollary 5.1, prove
    # m(n, 2) <= ceil(3n/2).  At n=3 this is five, so a counterexample
    # needing six colours must have at least three nonisolated vertices on
    # each side.  Bipartition symmetry makes the same bound apply to L and R.
    buckets = [
        (left, right, edge_count)
        for left, right in ((3, 3), (3, 4), (4, 4))
        for edge_count in range(max(8, left + right - 1), 13)
    ]
    selected_buckets: list[list[Topology]] = []
    sampling: dict[str, object] = {}
    for left, right, edge_count in buckets:
        labelled: dict[tuple[int, ...], Topology] = {}
        for _sample in range(pool_per_bucket):
            topology = random_connected_topology(
                left, right, edge_count, max_multiplicity, generator
            )
            labelled[topology.multiplicities] = topology
        ranked = sorted(
            labelled.values(),
            key=lambda topology: (topology_score(topology), topology.multiplicities),
            reverse=True,
        )
        keys: set[tuple[int, ...]] = set()
        selected: list[Topology] = []
        for topology in ranked:
            key = canonical_key(topology)
            if key in keys:
                continue
            keys.add(key)
            selected.append(topology)
            if len(selected) == selected_per_bucket:
                break
        selected_buckets.append(selected)
        sampling[f"{left}x{right}-m{edge_count}"] = {
            "sample_attempts": pool_per_bucket,
            "distinct_labelled": len(labelled),
            "selected_isomorphism_classes": len(selected),
        }

    interleaved: list[Topology] = []
    maximum = max((len(bucket) for bucket in selected_buckets), default=0)
    for rank in range(maximum):
        for bucket in selected_buckets:
            if rank < len(bucket):
                interleaved.append(bucket[rank])
    return (interleaved, sampling)


def run_survey(args: argparse.Namespace, config: SearchConfig) -> dict[str, object]:
    started = time.monotonic()
    deadline = started + args.total_seconds
    topologies, sampling = sampled_topologies(
        args.seed,
        args.pool_per_bucket,
        args.selected_per_bucket,
        args.max_multiplicity,
    )
    sampling_seconds = time.monotonic() - started
    results: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    witness: dict[str, object] | None = None
    stop_reason = "sample exhausted"
    for index, topology in enumerate(topologies, start=1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            stop_reason = "hard total runtime reached"
            break
        per_topology = SearchConfig(
            colour_count=TARGET_COLOURS,
            seed=config.seed,
            solver_timeout_ms=min(
                config.solver_timeout_ms, max(1, int(remaining * 1000))
            ),
            topology_seconds=min(config.topology_seconds, remaining),
            max_iterations=config.max_iterations,
            progress_every=config.progress_every,
        )
        result = N3CegarSearch(topology, per_topology).run()
        payload = result.to_json()
        payload["left_count"] = topology.left_count
        payload["right_count"] = topology.right_count
        payload["edge_count"] = topology.edge_count
        payload["score"] = list(topology_score(topology))
        results.append(payload)
        counts[result.status] = counts.get(result.status, 0) + 1
        print(
            json.dumps(
                {
                    "event": "n3_topology_complete",
                    "index": index,
                    "shape": f"{topology.left_count}x{topology.right_count}",
                    "edges": topology.edge_count,
                    "status": result.status,
                    "iterations": result.iterations,
                    "elapsed_seconds": round(result.elapsed_seconds, 3),
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        if result.status == "SAT_WITNESS":
            witness = result.witness
            stop_reason = "candidate witness found"
            break
    return {
        "mode": "survey",
        "target": {"n": TARGET_N, "global_colours": TARGET_COLOURS},
        "seed": args.seed,
        "frontier": {
            "topology_sampling_is_exhaustive": False,
            "shapes": ["3x3", "3x4", "4x4"],
            "edge_counts": [8, 9, 10, 11, 12],
            "selected_topologies": len(topologies),
            "searched_topologies": len(results),
            "weight_space_per_UNSAT_topology_is_exact": True,
            "safe_side_lower_bound": (
                "at least 3 nonisolated vertices per side, from Ngo--Vu "
                "m(3,2) <= 5 and bipartition symmetry"
            ),
        },
        "sampling": sampling,
        "sampling_seconds": round(sampling_seconds, 6),
        "status_counts": counts,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "stop_reason": stop_reason,
        "witness": witness,
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("controls", "fixed", "survey"), default="survey")
    parser.add_argument("--matrix", default="3")
    parser.add_argument("--seed", type=int, default=20260723)
    parser.add_argument("--pool-per-bucket", type=int, default=300)
    parser.add_argument("--selected-per-bucket", type=int, default=2)
    parser.add_argument("--max-multiplicity", type=int, default=3)
    parser.add_argument("--max-iterations", type=int, default=20000)
    parser.add_argument("--solver-timeout-ms", type=int, default=5000)
    parser.add_argument("--topology-seconds", type=float, default=6.0)
    parser.add_argument("--total-seconds", type=float, default=220.0)
    parser.add_argument("--progress-every", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    return parser


def parse_matrix(text: str) -> Topology:
    rows = [tuple(int(token) for token in row.split(",")) for row in text.split(";")]
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("matrix rows must be nonempty and equal length")
    return topology_from_multiplicities(
        len(rows), len(rows[0]), tuple(value for row in rows for value in row)
    )


def validate_args(args: argparse.Namespace) -> None:
    for name in (
        "pool_per_bucket",
        "selected_per_bucket",
        "max_multiplicity",
        "max_iterations",
        "solver_timeout_ms",
    ):
        if getattr(args, name) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    if args.topology_seconds <= 0:
        raise ValueError("--topology-seconds must be positive")
    if not 0 < args.total_seconds <= 235:
        raise ValueError("--total-seconds must be in (0,235]")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        validate_args(args)
    except ValueError as error:
        parser.error(str(error))
    config = SearchConfig(
        colour_count=TARGET_COLOURS,
        seed=args.seed,
        solver_timeout_ms=args.solver_timeout_ms,
        topology_seconds=args.topology_seconds,
        max_iterations=args.max_iterations,
        progress_every=args.progress_every,
    )
    if args.mode == "controls":
        payload = run_controls(config)
        exit_code = 0 if payload["passed"] is True else 1
    elif args.mode == "fixed":
        try:
            topology = parse_matrix(args.matrix)
        except ValueError as error:
            parser.error(str(error))
        if not is_connected(topology):
            parser.error("fixed matrix must be connected with no isolates")
        result = N3CegarSearch(topology, config).run()
        payload = {"mode": "fixed", **result.to_json()}
        exit_code = 1 if result.status == "INTERNAL_ERROR" else 0
    else:
        payload = run_survey(args, config)
        exit_code = 0
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
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
