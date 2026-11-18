"""Exact Z3 feasibility model for permutation routing in a bidirected cube.

Vertices are integers in ``range(2**dimension)``.  Bit ``i`` is cube
coordinate ``i`` and the directed cube arcs are ``(v, v ^ (1 << i))``.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Iterable, Literal, Sequence

import z3

Status = Literal["sat", "unsat", "unknown"]


@dataclass(frozen=True)
class RoutingResult:
    status: Status
    dimension: int
    permutation: tuple[int, ...]
    shortest_only: bool
    elapsed_seconds: float
    paths: dict[int, tuple[int, ...]] | None
    reason_unknown: str | None
    solver_statistics: dict[str, object]
    smt2: str | None = None


def cube_arcs(dimension: int) -> tuple[tuple[int, int], ...]:
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    order = 1 << dimension
    return tuple(
        (vertex, vertex ^ (1 << coordinate))
        for vertex in range(order)
        for coordinate in range(dimension)
    )


def validate_permutation(
    dimension: int, permutation: Sequence[int]
) -> tuple[int, ...]:
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    order = 1 << dimension
    normalized = tuple(permutation)
    if len(normalized) != order:
        raise ValueError(
            f"permutation has length {len(normalized)}, expected {order}"
        )
    if any(not isinstance(target, int) for target in normalized):
        raise ValueError("permutation entries must be integers")
    if sorted(normalized) != list(range(order)):
        raise ValueError(f"entries must be a permutation of 0..{order - 1}")
    return normalized


def hamming_distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def _statistics_dict(statistics: z3.Statistics) -> dict[str, object]:
    return {key: statistics.get_key_value(key) for key in statistics.keys()}


def _simple_path_in_support(
    source: int,
    target: int,
    support: Iterable[tuple[int, int]],
) -> tuple[int, ...]:
    """Return a simple source-target path from an integral flow support."""
    successors: dict[int, list[int]] = {}
    for tail, head in support:
        successors.setdefault(tail, []).append(head)

    parent: dict[int, int | None] = {source: None}
    queue = [source]
    for tail in queue:
        if tail == target:
            break
        for head in successors.get(tail, ()):
            if head not in parent:
                parent[head] = tail
                queue.append(head)

    if target not in parent:
        raise RuntimeError(
            f"model support has no path from {source} to {target}"
        )

    reversed_path = [target]
    while reversed_path[-1] != source:
        predecessor = parent[reversed_path[-1]]
        if predecessor is None:
            raise RuntimeError("broken path predecessor chain")
        reversed_path.append(predecessor)
    return tuple(reversed(reversed_path))


def verify_paths(
    dimension: int,
    permutation: Sequence[int],
    paths: dict[int, Sequence[int]],
    *,
    shortest_only: bool = False,
) -> None:
    """Independently check a routing witness; raise ``ValueError`` on failure."""
    normalized = validate_permutation(dimension, permutation)
    order = 1 << dimension
    if set(paths) != set(range(order)):
        raise ValueError("paths must contain exactly one entry per source")

    used_arcs: dict[tuple[int, int], int] = {}
    for source, target in enumerate(normalized):
        path = tuple(paths[source])
        if not path:
            raise ValueError(f"path for source {source} is empty")
        if path[0] != source or path[-1] != target:
            raise ValueError(f"wrong endpoints for source {source}: {path}")
        if len(set(path)) != len(path):
            raise ValueError(f"path for source {source} is not simple")
        if target == source and path != (source,):
            raise ValueError(f"fixed point {source} must use the empty arc path")
        if shortest_only and len(path) - 1 != hamming_distance(source, target):
            raise ValueError(f"path for source {source} is not shortest")

        for tail, head in zip(path, path[1:]):
            if not (0 <= tail < order and 0 <= head < order):
                raise ValueError(f"vertex outside Q_{dimension}: {(tail, head)}")
            if hamming_distance(tail, head) != 1:
                raise ValueError(f"not a cube arc: {(tail, head)}")
            if (tail, head) in used_arcs:
                other = used_arcs[(tail, head)]
                raise ValueError(
                    f"directed arc {(tail, head)} used by {other} and {source}"
                )
            used_arcs[(tail, head)] = source


def solve_routing(
    dimension: int,
    permutation: Sequence[int],
    *,
    shortest_only: bool = False,
    timeout_ms: int | None = None,
    include_smt2: bool = False,
) -> RoutingResult:
    """Decide exact feasibility, subject only to an optional solver timeout.

    Each non-fixed commodity has a binary variable on each allowed directed arc.
    At every vertex, outgoing flow minus incoming flow is 1 at the source, -1
    at the target, and 0 elsewhere.  Across commodities, each directed arc has
    capacity one.

    These constraints are equivalent to unrestricted arc-disjoint path routing.
    Paths give feasible binary flows.  Conversely, in the support of a feasible
    commodity flow, its target is reachable from its source: otherwise summing
    conservation over the source-reachable set gives net outflow 1, while that
    set has no supported outgoing arc.  A simple source-target path can therefore
    be selected from the support.  Discarding all other arcs, including cycles,
    cannot create an arc conflict.  Fixed points are represented by their
    length-zero path and have no variables.
    """
    normalized = validate_permutation(dimension, permutation)
    if timeout_ms is not None and timeout_ms <= 0:
        raise ValueError("timeout_ms must be positive")

    arcs = cube_arcs(dimension)
    active_sources = [
        source
        for source, target in enumerate(normalized)
        if source != target
    ]
    allowed: dict[int, tuple[tuple[int, int], ...]] = {}
    variables: dict[tuple[int, int, int], z3.BoolRef] = {}
    solver = z3.Solver()
    if timeout_ms is not None:
        solver.set(timeout=timeout_ms)

    for source in active_sources:
        target = normalized[source]
        commodity_arcs = tuple(
            (tail, head)
            for tail, head in arcs
            if not shortest_only
            or hamming_distance(head, target) < hamming_distance(tail, target)
        )
        allowed[source] = commodity_arcs
        for tail, head in commodity_arcs:
            variables[(source, tail, head)] = z3.Bool(
                f"f_{source}_{tail}_{head}"
            )

        for vertex in range(1 << dimension):
            outgoing = [
                variables[(source, tail, head)]
                for tail, head in commodity_arcs
                if tail == vertex
            ]
            incoming = [
                variables[(source, tail, head)]
                for tail, head in commodity_arcs
                if head == vertex
            ]
            balance = 1 if vertex == source else -1 if vertex == target else 0
            solver.add(z3.Sum(outgoing) - z3.Sum(incoming) == balance)
            # A simple path never enters or leaves a vertex more than once.
            # These valid strengthening constraints rule out branching flows
            # while still allowing removable disjoint cycles.
            if outgoing:
                solver.add(z3.PbLe([(variable, 1) for variable in outgoing], 1))
            if incoming:
                solver.add(z3.PbLe([(variable, 1) for variable in incoming], 1))

    for tail, head in arcs:
        users = [
            variables[(source, tail, head)]
            for source in active_sources
            if (source, tail, head) in variables
        ]
        if users:
            solver.add(z3.PbLe([(variable, 1) for variable in users], 1))

    smt2 = solver.to_smt2() if include_smt2 else None
    started = monotonic()
    check = solver.check()
    elapsed = monotonic() - started
    statistics = _statistics_dict(solver.statistics())

    if check == z3.unsat:
        return RoutingResult(
            "unsat",
            dimension,
            normalized,
            shortest_only,
            elapsed,
            None,
            None,
            statistics,
            smt2,
        )
    if check == z3.unknown:
        return RoutingResult(
            "unknown",
            dimension,
            normalized,
            shortest_only,
            elapsed,
            None,
            solver.reason_unknown(),
            statistics,
            smt2,
        )

    model = solver.model()
    paths: dict[int, tuple[int, ...]] = {}
    for source, target in enumerate(normalized):
        if source == target:
            paths[source] = (source,)
            continue
        support = [
            (tail, head)
            for tail, head in allowed[source]
            if z3.is_true(model.eval(variables[(source, tail, head)]))
        ]
        paths[source] = _simple_path_in_support(source, target, support)

    verify_paths(
        dimension, normalized, paths, shortest_only=shortest_only
    )
    return RoutingResult(
        "sat",
        dimension,
        normalized,
        shortest_only,
        elapsed,
        paths,
        None,
        statistics,
        smt2,
    )
