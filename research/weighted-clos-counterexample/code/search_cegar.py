#!/usr/bin/env python3
"""Exact CEGAR search for an n=2 Chung--Ross counterexample.

The master solver chooses strictly positive rational edge weights and a local
two-bin packing at every vertex.  A checker then looks for a valid global
colouring of those concrete weights.  Every colouring found by the checker is
blocked in the master for all later weight assignments.  Thus:

* checker UNSAT gives a candidate counterexample for the fixed topology;
* master UNSAT proves that topology admits no counterexample under the encoded
  assumptions; and
* a timeout or iteration limit is reported as UNKNOWN, never as UNSAT.

The target search always uses three colours.  ``--mode controls`` also runs a
synthetic one-colour positive control to exercise the witness path.
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
from typing import Iterator, Sequence

import z3


CAPACITY = Fraction(1, 1)


@dataclass(frozen=True)
class Edge:
    edge_id: int
    left: int
    right: int


@dataclass(frozen=True)
class Topology:
    left_count: int
    right_count: int
    multiplicities: tuple[int, ...]
    edges: tuple[Edge, ...]

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def topology_id(self) -> str:
        rows = []
        for left in range(self.left_count):
            start = left * self.right_count
            row = self.multiplicities[start : start + self.right_count]
            rows.append(",".join(str(value) for value in row))
        return ";".join(rows)

    def incident_edges(self, side: str, vertex: int) -> tuple[int, ...]:
        if side == "L":
            return tuple(edge.edge_id for edge in self.edges if edge.left == vertex)
        if side == "R":
            return tuple(edge.edge_id for edge in self.edges if edge.right == vertex)
        raise ValueError(f"unknown side: {side}")


@dataclass(frozen=True)
class SearchConfig:
    colour_count: int
    seed: int
    solver_timeout_ms: int
    topology_seconds: float
    max_iterations: int
    enforce_mixed_weights: bool
    progress_every: int


@dataclass(frozen=True)
class ConcreteCandidate:
    weights: tuple[Fraction, ...]
    local_bin_one: tuple[bool, ...]


@dataclass(frozen=True)
class TopologyResult:
    status: str
    topology_id: str
    iterations: int
    colourings_blocked: int
    master_checks: int
    checker_checks: int
    elapsed_seconds: float
    reason: str
    search_scope: str
    witness: dict[str, object] | None

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "status": self.status,
            "topology_id": self.topology_id,
            "iterations": self.iterations,
            "colourings_blocked": self.colourings_blocked,
            "master_checks": self.master_checks,
            "checker_checks": self.checker_checks,
            "elapsed_seconds": round(self.elapsed_seconds, 6),
            "reason": self.reason,
            "search_scope": self.search_scope,
        }
        if self.witness is not None:
            payload["witness"] = self.witness
        return payload


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def z3_fraction(value: Fraction) -> z3.RatNumRef:
    return z3.RealVal(fraction_text(value))


def model_fraction(model: z3.ModelRef, expression: z3.ArithRef) -> Fraction:
    value = model.evaluate(expression, model_completion=True)
    if not isinstance(value, z3.RatNumRef):
        raise TypeError(f"expected exact rational model value, got {value}")
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def sum_arith(expressions: Sequence[z3.ArithRef]) -> z3.ArithRef:
    if not expressions:
        return z3.RealVal(0)
    return z3.Sum(expressions)


def topology_from_multiplicities(
    left_count: int,
    right_count: int,
    multiplicities: Sequence[int],
) -> Topology:
    expected = left_count * right_count
    if len(multiplicities) != expected:
        raise ValueError(f"expected {expected} cells, got {len(multiplicities)}")
    if any(value < 0 for value in multiplicities):
        raise ValueError("multiplicities must be non-negative")
    edges: list[Edge] = []
    for left in range(left_count):
        for right in range(right_count):
            multiplicity = multiplicities[left * right_count + right]
            for _parallel_index in range(multiplicity):
                edges.append(Edge(len(edges), left, right))
    return Topology(
        left_count=left_count,
        right_count=right_count,
        multiplicities=tuple(multiplicities),
        edges=tuple(edges),
    )


def parse_matrix(text: str) -> Topology:
    rows = [row.strip() for row in text.split(";") if row.strip()]
    if not rows:
        raise ValueError("matrix must have at least one row")
    parsed_rows = [
        tuple(int(token.strip()) for token in row.split(",") if token.strip())
        for row in rows
    ]
    right_count = len(parsed_rows[0])
    if right_count == 0 or any(len(row) != right_count for row in parsed_rows):
        raise ValueError("matrix rows must be nonempty and have equal length")
    flat = tuple(value for row in parsed_rows for value in row)
    return topology_from_multiplicities(len(parsed_rows), right_count, flat)


def is_connected(topology: Topology) -> bool:
    if topology.edge_count == 0:
        return False
    left_seen = {topology.edges[0].left}
    right_seen: set[int] = set()
    changed = True
    while changed:
        changed = False
        for edge in topology.edges:
            if edge.left in left_seen and edge.right not in right_seen:
                right_seen.add(edge.right)
                changed = True
            if edge.right in right_seen and edge.left not in left_seen:
                left_seen.add(edge.left)
                changed = True
    return (
        len(left_seen) == topology.left_count
        and len(right_seen) == topology.right_count
    )


def permuted_matrix(
    multiplicities: tuple[int, ...],
    left_count: int,
    right_count: int,
    left_permutation: tuple[int, ...],
    right_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        multiplicities[old_left * right_count + old_right]
        for old_left in left_permutation
        for old_right in right_permutation
    )


def is_row_column_canonical(topology: Topology) -> bool:
    """Remove only the safe symmetry from relabelling each bipartition."""

    original = topology.multiplicities
    for left_permutation in itertools.permutations(range(topology.left_count)):
        for right_permutation in itertools.permutations(range(topology.right_count)):
            candidate = permuted_matrix(
                original,
                topology.left_count,
                topology.right_count,
                left_permutation,
                right_permutation,
            )
            if candidate < original:
                return False
    return True


def bounded_compositions(
    total: int,
    length: int,
    maximum: int,
) -> Iterator[tuple[int, ...]]:
    prefix: list[int] = []

    def visit(remaining: int, position: int) -> Iterator[tuple[int, ...]]:
        if position == length:
            if remaining == 0:
                yield tuple(prefix)
            return
        cells_left = length - position - 1
        lower = max(0, remaining - cells_left * maximum)
        upper = min(maximum, remaining)
        for value in range(lower, upper + 1):
            prefix.append(value)
            yield from visit(remaining - value, position + 1)
            prefix.pop()

    yield from visit(total, 0)


def generate_topologies(
    left_min: int,
    left_max: int,
    right_min: int,
    right_max: int,
    edge_min: int,
    edge_max: int,
    max_multiplicity: int,
) -> Iterator[Topology]:
    for left_count in range(left_min, left_max + 1):
        for right_count in range(right_min, right_max + 1):
            # Swapping the bipartition is an isomorphism.  Keep L <= R only
            # when the swapped size pair is also inside the requested family.
            swapped_is_requested = (
                left_min <= right_count <= left_max
                and right_min <= left_count <= right_max
            )
            if left_count > right_count and swapped_is_requested:
                continue
            cell_count = left_count * right_count
            for edge_count in range(edge_min, edge_max + 1):
                if edge_count < left_count + right_count - 1:
                    continue
                if edge_count > cell_count * max_multiplicity:
                    continue
                for multiplicities in bounded_compositions(
                    edge_count, cell_count, max_multiplicity
                ):
                    topology = topology_from_multiplicities(
                        left_count, right_count, multiplicities
                    )
                    if not is_connected(topology):
                        continue
                    if not is_row_column_canonical(topology):
                        continue
                    yield topology


class CegarSearch:
    def __init__(self, topology: Topology, config: SearchConfig) -> None:
        self.topology = topology
        self.config = config
        self.master = z3.Solver()
        self.master.set("timeout", config.solver_timeout_ms)
        self.master.set("random_seed", config.seed)
        self.weights = tuple(
            z3.Real(f"w_{edge.edge_id}") for edge in topology.edges
        )
        # One Boolean per incidence.  Indexing is flattened vertex by vertex.
        self.bin_variables: list[z3.BoolRef] = []
        self.bin_offsets: dict[tuple[str, int, int], int] = {}
        self._add_master_base_constraints()

    def _vertices(self) -> Iterator[tuple[str, int]]:
        for left in range(self.topology.left_count):
            yield ("L", left)
        for right in range(self.topology.right_count):
            yield ("R", right)

    def _add_master_base_constraints(self) -> None:
        for weight in self.weights:
            self.master.add(weight > 0, weight <= 1)

        total_loads: list[z3.ArithRef] = []
        for side, vertex in self._vertices():
            incident = self.topology.incident_edges(side, vertex)
            if not incident:
                self.master.add(z3.BoolVal(False))
                continue
            bin_zero_terms: list[z3.ArithRef] = []
            bin_one_terms: list[z3.ArithRef] = []
            for edge_id in incident:
                bin_variable = z3.Bool(f"bin_{side}_{vertex}_{edge_id}")
                offset = len(self.bin_variables)
                self.bin_variables.append(bin_variable)
                self.bin_offsets[(side, vertex, edge_id)] = offset
                bin_one_terms.append(z3.If(bin_variable, self.weights[edge_id], 0))
                bin_zero_terms.append(
                    z3.If(bin_variable, z3.RealVal(0), self.weights[edge_id])
                )
            self.master.add(sum_arith(bin_zero_terms) <= 1)
            self.master.add(sum_arith(bin_one_terms) <= 1)
            # Complementing both bins at one vertex changes nothing.  Fixing
            # the first incidence to bin zero removes exactly that symmetry.
            first_offset = self.bin_offsets[(side, vertex, incident[0])]
            self.master.add(z3.Not(self.bin_variables[first_offset]))
            total_loads.append(sum_arith([self.weights[index] for index in incident]))

        # Together with the two-bin constraints, total load > 1 at some vertex
        # proves that the instance parameter is exactly n=2, not merely <= 2.
        self.master.add(z3.Or([load > 1 for load in total_loads]))

        if self.config.enforce_mixed_weights:
            self.master.add(z3.Or([weight > z3.RealVal("1/2") for weight in self.weights]))
            self.master.add(z3.Or([weight <= z3.RealVal("1/2") for weight in self.weights]))

    def _extract_candidate(self, model: z3.ModelRef) -> ConcreteCandidate:
        weights = tuple(model_fraction(model, weight) for weight in self.weights)
        bins = tuple(
            z3.is_true(model.evaluate(variable, model_completion=True))
            for variable in self.bin_variables
        )
        return ConcreteCandidate(weights, bins)

    def _find_colouring(
        self,
        candidate: ConcreteCandidate,
        remaining_ms: int,
    ) -> tuple[str, tuple[int, ...] | None, str]:
        checker = z3.Solver()
        checker.set("timeout", max(1, min(self.config.solver_timeout_ms, remaining_ms)))
        checker.set("random_seed", self.config.seed)
        colours = tuple(
            z3.Int(f"colour_{edge.edge_id}") for edge in self.topology.edges
        )
        for colour in colours:
            checker.add(colour >= 0, colour < self.config.colour_count)
        if colours:
            # Every colouring orbit under global colour permutation has a
            # representative with the first edge coloured zero.
            checker.add(colours[0] == 0)
        for side, vertex in self._vertices():
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
            assignment = tuple(
                model.evaluate(colour, model_completion=True).as_long()
                for colour in colours
            )
            return ("SAT", assignment, "")
        if result == z3.unsat:
            return ("UNSAT", None, "")
        return ("UNKNOWN", None, checker.reason_unknown())

    def _block_colouring(self, colouring: tuple[int, ...]) -> None:
        overloads: list[z3.BoolRef] = []
        for side, vertex in self._vertices():
            incident = self.topology.incident_edges(side, vertex)
            for colour_index in range(self.config.colour_count):
                colour_edges = [
                    self.weights[edge_id]
                    for edge_id in incident
                    if colouring[edge_id] == colour_index
                ]
                if colour_edges:
                    overloads.append(sum_arith(colour_edges) > 1)
        # This formula is invariant under a global permutation of colour names,
        # so one clause blocks the entire orbit represented by colour[0] = 0.
        self.master.add(z3.Or(overloads))

    def _local_bins(
        self, candidate: ConcreteCandidate
    ) -> tuple[dict[str, list[int]], list[str]]:
        bins: dict[str, list[int]] = {}
        exact_vertices: list[str] = []
        for side, vertex in self._vertices():
            key = f"{side}{vertex}"
            bin_zero: list[int] = []
            bin_one: list[int] = []
            incident = self.topology.incident_edges(side, vertex)
            for edge_id in incident:
                offset = self.bin_offsets[(side, vertex, edge_id)]
                if candidate.local_bin_one[offset]:
                    bin_one.append(edge_id)
                else:
                    bin_zero.append(edge_id)
            bins[key] = [*bin_zero, -1, *bin_one]
            total = sum((candidate.weights[index] for index in incident), Fraction(0))
            if total > 1:
                exact_vertices.append(key)
        return bins, exact_vertices

    def _self_check_local(self, candidate: ConcreteCandidate) -> tuple[bool, str]:
        if any(weight <= 0 or weight > 1 for weight in candidate.weights):
            return (False, "edge weight outside (0,1]")
        exact_n = False
        for side, vertex in self._vertices():
            zero_load = Fraction(0)
            one_load = Fraction(0)
            incident = self.topology.incident_edges(side, vertex)
            for edge_id in incident:
                offset = self.bin_offsets[(side, vertex, edge_id)]
                if candidate.local_bin_one[offset]:
                    one_load += candidate.weights[edge_id]
                else:
                    zero_load += candidate.weights[edge_id]
            if zero_load > CAPACITY or one_load > CAPACITY:
                return (False, f"local bin overload at {side}{vertex}")
            if zero_load + one_load > CAPACITY:
                exact_n = True
        if not exact_n:
            return (False, "no vertex needs two bins")
        return (True, "")

    def _exhaustive_colouring_check(
        self,
        candidate: ConcreteCandidate,
        deadline: float,
    ) -> tuple[bool | None, int, tuple[int, ...] | None]:
        """Return (colourable, visited nodes, colouring), or None on timeout."""

        edge_order = sorted(
            range(self.topology.edge_count),
            key=lambda edge_id: (
                -candidate.weights[edge_id],
                -len(self.topology.incident_edges("L", self.topology.edges[edge_id].left)),
                edge_id,
            ),
        )
        loads: dict[tuple[str, int, int], Fraction] = {}
        assignment = [-1] * self.topology.edge_count
        nodes = 0

        def visit(position: int, used_colours: int) -> tuple[int, ...] | None:
            nonlocal nodes
            nodes += 1
            if nodes % 4096 == 0 and time.monotonic() >= deadline:
                raise TimeoutError
            if position == len(edge_order):
                return tuple(assignment)
            edge_id = edge_order[position]
            edge = self.topology.edges[edge_id]
            # Canonical restricted-growth colours remove global permutation
            # symmetry without deleting any colouring orbit.
            colour_limit = min(self.config.colour_count, used_colours + 1)
            for colour in range(colour_limit):
                left_key = ("L", edge.left, colour)
                right_key = ("R", edge.right, colour)
                new_left = loads.get(left_key, Fraction(0)) + candidate.weights[edge_id]
                new_right = loads.get(right_key, Fraction(0)) + candidate.weights[edge_id]
                if new_left > CAPACITY or new_right > CAPACITY:
                    continue
                old_left = loads.get(left_key, Fraction(0))
                old_right = loads.get(right_key, Fraction(0))
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

    def _witness_json(
        self,
        candidate: ConcreteCandidate,
        iterations: int,
        blocked: int,
        self_check_nodes: int,
    ) -> dict[str, object]:
        bins, exact_vertices = self._local_bins(candidate)
        edge_payload: list[dict[str, object]] = []
        for edge in self.topology.edges:
            edge_payload.append(
                {
                    "id": edge.edge_id,
                    "left": f"L{edge.left}",
                    "right": f"R{edge.right}",
                    "weight": fraction_text(candidate.weights[edge.edge_id]),
                }
            )
        decoded_bins: dict[str, list[list[int]]] = {}
        for vertex, flattened in bins.items():
            separator = flattened.index(-1)
            decoded_bins[vertex] = [
                flattened[:separator],
                flattened[separator + 1 :],
            ]
        return {
            "schema": "weighted-clos-counterexample-v1",
            "target_n": 2,
            "global_colours": self.config.colour_count,
            "topology": {
                "left_vertices": [f"L{i}" for i in range(self.topology.left_count)],
                "right_vertices": [f"R{i}" for i in range(self.topology.right_count)],
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
            "local_two_bins": decoded_bins,
            "vertices_requiring_two_bins": exact_vertices,
            "search": {
                "seed": self.config.seed,
                "cegar_iterations": iterations,
                "colouring_orbits_blocked": blocked,
                "exhaustive_self_check_nodes": self_check_nodes,
                "mixed_weight_constraint": self.config.enforce_mixed_weights,
            },
        }

    def run(self) -> TopologyResult:
        started = time.monotonic()
        deadline = started + self.config.topology_seconds
        blocked = 0
        master_checks = 0
        checker_checks = 0

        for iteration in range(1, self.config.max_iterations + 1):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return self._result(
                    "UNKNOWN",
                    iteration - 1,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    "topology time limit",
                )
            self.master.set(
                "timeout",
                max(1, min(self.config.solver_timeout_ms, int(remaining * 1000))),
            )
            master_checks += 1
            master_result = self.master.check()
            if master_result == z3.unsat:
                if self.config.enforce_mixed_weights:
                    reason = (
                        "master exhausted locally two-packable exact-n=2 weights "
                        "within the mixed-weight slice (>1/2 exists and <=1/2 exists)"
                    )
                else:
                    reason = (
                        "master exhausted all positive locally two-packable "
                        "exact-n=2 weights for this topology"
                    )
                return self._result(
                    "UNSAT_TOPOLOGY",
                    iteration - 1,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    reason,
                )
            if master_result == z3.unknown:
                return self._result(
                    "UNKNOWN",
                    iteration - 1,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    f"master solver: {self.master.reason_unknown()}",
                )

            candidate = self._extract_candidate(self.master.model())
            local_ok, local_reason = self._self_check_local(candidate)
            if not local_ok:
                return self._result(
                    "INTERNAL_ERROR",
                    iteration,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    local_reason,
                )

            remaining_ms = max(1, int((deadline - time.monotonic()) * 1000))
            checker_checks += 1
            checker_status, colouring, checker_reason = self._find_colouring(
                candidate, remaining_ms
            )
            if checker_status == "UNKNOWN":
                return self._result(
                    "UNKNOWN",
                    iteration,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    f"colour checker: {checker_reason}",
                )
            if checker_status == "UNSAT":
                colourable, nodes, found = self._exhaustive_colouring_check(
                    candidate, deadline
                )
                if colourable is None:
                    return self._result(
                        "UNKNOWN",
                        iteration,
                        blocked,
                        master_checks,
                        checker_checks,
                        started,
                        "exact exhaustive self-check timed out after checker UNSAT",
                    )
                if colourable:
                    return self._result(
                        "INTERNAL_ERROR",
                        iteration,
                        blocked,
                        master_checks,
                        checker_checks,
                        started,
                        f"exhaustive self-check found missed colouring {found}",
                    )
                witness = self._witness_json(candidate, iteration, blocked, nodes)
                return self._result(
                    "SAT_WITNESS",
                    iteration,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    "checker UNSAT and exact exhaustive self-check found no colouring",
                    witness,
                )

            if colouring is None:
                return self._result(
                    "INTERNAL_ERROR",
                    iteration,
                    blocked,
                    master_checks,
                    checker_checks,
                    started,
                    "checker reported SAT without a colouring",
                )
            self._block_colouring(colouring)
            blocked += 1
            if (
                self.config.progress_every > 0
                and iteration % self.config.progress_every == 0
            ):
                progress = {
                    "event": "cegar_progress",
                    "topology_id": self.topology.topology_id,
                    "iteration": iteration,
                    "blocked": blocked,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                }
                print(json.dumps(progress, sort_keys=True), file=sys.stderr)

        return self._result(
            "UNKNOWN",
            self.config.max_iterations,
            blocked,
            master_checks,
            checker_checks,
            started,
            "CEGAR iteration limit",
        )

    def _result(
        self,
        status: str,
        iterations: int,
        blocked: int,
        master_checks: int,
        checker_checks: int,
        started: float,
        reason: str,
        witness: dict[str, object] | None = None,
    ) -> TopologyResult:
        return TopologyResult(
            status=status,
            topology_id=self.topology.topology_id,
            iterations=iterations,
            colourings_blocked=blocked,
            master_checks=master_checks,
            checker_checks=checker_checks,
            elapsed_seconds=time.monotonic() - started,
            reason=reason,
            search_scope=(
                "mixed_weight_slice"
                if self.config.enforce_mixed_weights
                else "all_positive_weights"
            ),
            witness=witness,
        )


def run_controls(config: SearchConfig) -> dict[str, object]:
    topology = topology_from_multiplicities(1, 1, (2,))
    positive_config = SearchConfig(
        colour_count=1,
        seed=config.seed,
        solver_timeout_ms=config.solver_timeout_ms,
        topology_seconds=config.topology_seconds,
        max_iterations=config.max_iterations,
        enforce_mixed_weights=False,
        progress_every=config.progress_every,
    )
    negative_config = SearchConfig(
        colour_count=3,
        seed=config.seed,
        solver_timeout_ms=config.solver_timeout_ms,
        topology_seconds=config.topology_seconds,
        max_iterations=config.max_iterations,
        enforce_mixed_weights=False,
        progress_every=config.progress_every,
    )
    positive = CegarSearch(topology, positive_config).run()
    negative = CegarSearch(topology, negative_config).run()
    passed = (
        positive.status == "SAT_WITNESS"
        and negative.status == "UNSAT_TOPOLOGY"
    )
    return {
        "mode": "controls",
        "passed": passed,
        "positive_control": {
            "description": (
                "synthetic one-colour case: two parallel positive edges can be "
                "locally split but cannot share one unit-capacity colour"
            ),
            **positive.to_json(),
        },
        "negative_control": {
            "description": (
                "target three-colour case: two parallel edges always receive "
                "different colours, so this topology cannot be a witness"
            ),
            **negative.to_json(),
        },
    }


def run_survey(
    topologies: Iterator[Topology],
    config: SearchConfig,
    max_topologies: int,
    total_seconds: float,
) -> dict[str, object]:
    started = time.monotonic()
    results: list[dict[str, object]] = []
    status_counts: dict[str, int] = {}
    generated = 0
    witness: dict[str, object] | None = None
    stop_reason = "topology iterator exhausted"

    for topology in topologies:
        if generated >= max_topologies:
            stop_reason = "topology limit"
            break
        remaining = total_seconds - (time.monotonic() - started)
        if remaining <= 0:
            stop_reason = "survey time limit"
            break
        generated += 1
        per_topology = SearchConfig(
            colour_count=config.colour_count,
            seed=config.seed,
            solver_timeout_ms=config.solver_timeout_ms,
            topology_seconds=min(config.topology_seconds, remaining),
            max_iterations=config.max_iterations,
            enforce_mixed_weights=config.enforce_mixed_weights,
            progress_every=config.progress_every,
        )
        result = CegarSearch(topology, per_topology).run()
        result_json = result.to_json()
        results.append(result_json)
        status_counts[result.status] = status_counts.get(result.status, 0) + 1
        progress = {
            "event": "topology_complete",
            "index": generated,
            "topology_id": topology.topology_id,
            "edge_count": topology.edge_count,
            "status": result.status,
            "iterations": result.iterations,
            "elapsed_seconds": round(result.elapsed_seconds, 3),
        }
        print(json.dumps(progress, sort_keys=True), file=sys.stderr)
        if result.status == "SAT_WITNESS":
            witness = result.witness
            stop_reason = "witness found"
            break

    return {
        "mode": "survey",
        "target": {"n": 2, "global_colours": config.colour_count},
        "search_scope": (
            "mixed_weight_slice"
            if config.enforce_mixed_weights
            else "all_positive_weights"
        ),
        "seed": config.seed,
        "generated_topologies": generated,
        "status_counts": status_counts,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "stop_reason": stop_reason,
        "witness": witness,
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("controls", "fixed", "survey"),
        default="survey",
    )
    parser.add_argument(
        "--matrix",
        default="2",
        help="fixed multiplicity matrix, for example '2,1;1,2'",
    )
    parser.add_argument("--left-min", type=int, default=1)
    parser.add_argument("--left-max", type=int, default=3)
    parser.add_argument("--right-min", type=int, default=1)
    parser.add_argument("--right-max", type=int, default=3)
    parser.add_argument("--edge-min", type=int, default=2)
    parser.add_argument("--edge-max", type=int, default=8)
    parser.add_argument("--max-multiplicity", type=int, default=3)
    parser.add_argument("--max-topologies", type=int, default=100)
    parser.add_argument("--max-iterations", type=int, default=5000)
    parser.add_argument("--solver-timeout-ms", type=int, default=5000)
    parser.add_argument("--topology-seconds", type=float, default=15.0)
    parser.add_argument("--total-seconds", type=float, default=120.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=100)
    parser.add_argument(
        "--enforce-mixed-weights",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="require at least one weight > 1/2 and at least one <= 1/2",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write the exact JSON result to this path instead of stdout",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    positive_names = (
        "left_min",
        "left_max",
        "right_min",
        "right_max",
        "edge_min",
        "edge_max",
        "max_multiplicity",
        "max_topologies",
        "max_iterations",
        "solver_timeout_ms",
    )
    for name in positive_names:
        if getattr(args, name) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    if args.left_min > args.left_max or args.right_min > args.right_max:
        raise ValueError("minimum side size cannot exceed maximum")
    if args.edge_min > args.edge_max:
        raise ValueError("--edge-min cannot exceed --edge-max")
    if args.topology_seconds <= 0 or args.total_seconds <= 0:
        raise ValueError("time limits must be positive")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        validate_args(args)
    except ValueError as error:
        parser.error(str(error))

    config = SearchConfig(
        colour_count=3,
        seed=args.seed,
        solver_timeout_ms=args.solver_timeout_ms,
        topology_seconds=args.topology_seconds,
        max_iterations=args.max_iterations,
        enforce_mixed_weights=args.enforce_mixed_weights,
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
            parser.error("--matrix must describe a connected topology with no isolates")
        result = CegarSearch(topology, config).run()
        payload = {"mode": "fixed", **result.to_json()}
        exit_code = 0 if result.status != "INTERNAL_ERROR" else 1
    else:
        topologies = generate_topologies(
            args.left_min,
            args.left_max,
            args.right_min,
            args.right_max,
            args.edge_min,
            args.edge_max,
            args.max_multiplicity,
        )
        payload = run_survey(
            topologies,
            config,
            args.max_topologies,
            args.total_seconds,
        )
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
