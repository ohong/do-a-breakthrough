#!/usr/bin/env python3
"""Independent finite checks for the structural-route audit.

This deliberately reconstructs the low-slack permutations and the S4 path
families from the mathematical descriptions, without importing routing.py or
any solver-structural helper.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter
from collections.abc import Iterable


Arc = tuple[int, int]
Path = tuple[int, ...]


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def flip_path(source: int, order: tuple[int, ...]) -> Path:
    path = [source]
    for coordinate in order:
        path.append(path[-1] ^ (1 << coordinate))
    return tuple(path)


def cycles_on_support(tau: tuple[int, ...]) -> list[tuple[int, ...]]:
    seen: set[int] = set()
    cycles: list[tuple[int, ...]] = []
    for start, image in enumerate(tau):
        if image == start or start in seen:
            continue
        cycle: list[int] = []
        vertex = start
        while vertex not in seen:
            seen.add(vertex)
            cycle.append(vertex)
            vertex = tau[vertex]
        cycles.append(tuple(cycle))
    return cycles


def generate_low_slack_taus(dimension: int) -> Iterable[tuple[int, ...]]:
    size = 1 << dimension
    identity = tuple(range(size))
    yield identity
    vertices = range(size)
    for support_size in range(2, min(4, size) + 1):
        for support in itertools.combinations(vertices, support_size):
            for images in itertools.permutations(support):
                if any(source == target for source, target in zip(support, images)):
                    continue
                tau = list(identity)
                for source, target in zip(support, images):
                    tau[source] = target
                tau_tuple = tuple(tau)
                displacement = sum(
                    hamming(source, target)
                    for source, target in enumerate(tau_tuple)
                )
                if displacement in (2, 4):
                    yield tau_tuple


def splice_transposition(
    standard: dict[int, Path],
    routes: dict[int, Path],
    a: int,
    b: int,
    order: tuple[int, ...],
) -> None:
    differing = {i for i in order if ((a ^ b) >> i) & 1}
    positions = [i for i, coordinate in enumerate(order) if coordinate in differing]
    assert positions == list(range(positions[0], positions[-1] + 1))
    first, after = positions[0], positions[-1] + 1
    assert standard[a][first] == standard[b][after]
    assert standard[b][first] == standard[a][after]
    routes[a] = standard[a][: first + 1] + standard[b][after + 1 :]
    routes[b] = standard[b][: first + 1] + standard[a][after + 1 :]


def construct_routes(dimension: int, tau: tuple[int, ...]) -> dict[int, Path]:
    size = 1 << dimension
    all_mask = size - 1
    cycles = cycles_on_support(tau)
    displacement = sum(hamming(source, target) for source, target in enumerate(tau))

    if not cycles:
        order = tuple(range(dimension))
        return {source: flip_path(source, order) for source in range(size)}

    if len(cycles) in (1, 2) and all(len(cycle) == 2 for cycle in cycles):
        first_cycle = cycles[0]
        differing_first = tuple(
            i for i in range(dimension) if ((first_cycle[0] ^ first_cycle[1]) >> i) & 1
        )
        if len(cycles) == 1 and displacement == 4:
            order = tuple(i for i in range(dimension) if i not in differing_first)
            order += differing_first
        else:
            order = tuple(range(dimension))
        standard = {source: flip_path(source, order) for source in range(size)}
        routes = dict(standard)
        for a, b in cycles:
            splice_transposition(standard, routes, a, b, order)
        return routes

    assert len(cycles) == 1
    cycle = cycles[0]
    assert len(cycle) in (3, 4)
    if len(cycle) == 3:
        for rotation in range(3):
            rotated = cycle[rotation:] + cycle[:rotation]
            if hamming(rotated[0], rotated[1]) == hamming(rotated[1], rotated[2]) == 1:
                cycle = rotated
                break
        else:
            raise AssertionError(f"unclassified 3-cycle: {cycle}")
    a, b, c = cycle[:3]
    p_mask = a ^ b
    q_mask = b ^ c
    assert p_mask.bit_count() == q_mask.bit_count() == 1
    p = p_mask.bit_length() - 1
    q = q_mask.bit_length() - 1
    assert p != q
    other = tuple(i for i in range(dimension) if i not in (p, q))
    prefix = {source: flip_path(source, other) for source in range(size)}
    order = other + (p, q)
    routes = {source: flip_path(source, order) for source in range(size)}

    a_star = prefix[a][-1]
    b_star = prefix[b][-1]
    c_star = prefix[c][-1]
    routes[a] = prefix[a] + (a_star ^ (1 << q),)
    routes[b] = prefix[b] + (b_star ^ (1 << p),)
    routes[c] = prefix[c]
    if len(cycle) == 4:
        r = cycle[3]
        r_star = prefix[r][-1]
        routes[c] = prefix[c] + (c_star ^ (1 << q),)
        routes[r] = prefix[r] + (r_star ^ (1 << p),)

    expected = {source: all_mask ^ tau[source] for source in range(size)}
    assert all(routes[source][-1] == expected[source] for source in range(size))
    return routes


def verify_routes(dimension: int, tau: tuple[int, ...], routes: dict[int, Path]) -> None:
    size = 1 << dimension
    all_mask = size - 1
    used: set[Arc] = set()
    assert set(routes) == set(range(size))
    for source, path in routes.items():
        target = all_mask ^ tau[source]
        assert path[0] == source
        assert path[-1] == target
        assert len(path) - 1 == hamming(source, target)
        assert len(set(path)) == len(path)
        for arc in zip(path, path[1:]):
            assert hamming(*arc) == 1
            assert arc not in used
            used.add(arc)


def check_cut_equality(dimension: int) -> int:
    size = 1 << dimension
    equality_count = 0
    for subset_mask in range(1, (1 << size) - 1):
        subset = {v for v in range(size) if (subset_mask >> v) & 1}
        boundary = sum(
            1
            for v in subset
            for coordinate in range(dimension)
            if (v ^ (1 << coordinate)) not in subset
        )
        smaller = min(len(subset), size - len(subset))
        assert boundary >= smaller
        if boundary != smaller:
            continue
        equality_count += 1
        is_halfcube = any(
            subset == {v for v in range(size) if ((v >> coordinate) & 1) == bit}
            for coordinate in range(dimension)
            for bit in (0, 1)
        )
        assert is_halfcube
    return equality_count


def check_benes_example() -> None:
    # Q2 coordinate-swap permutation, split on either coordinate.
    sigma = (0, 2, 1, 3)
    for split in (0, 1):
        remaining = 1 - split
        edges: list[tuple[int, int, int, int]] = []
        for source, target in enumerate(sigma):
            input_pair = (source >> remaining) & 1
            output_pair = (target >> remaining) & 1
            source_side = (source >> split) & 1
            target_side = (target >> split) & 1
            edges.append((input_pair, output_pair, source_side, target_side))

        safe_colorings = 0
        # Independently enumerate every coloring that gives one edge of each
        # color at each input and output pair. (For this one cycle there are
        # exactly two.)
        alternating_colorings = 0
        for colors in itertools.product((0, 1), repeat=4):
            if any(
                sorted(colors[i] for i, edge in enumerate(edges) if edge[side] == pair)
                != [0, 1]
                for side in (0, 1)
                for pair in (0, 1)
            ):
                continue
            alternating_colorings += 1
            safe = True
            for pair in (0, 1):
                source_zero = next(
                    i
                    for i, edge in enumerate(edges)
                    if edge[0] == pair and edge[2] == 0
                )
                target_zero = next(
                    i
                    for i, edge in enumerate(edges)
                    if edge[1] == pair and edge[3] == 0
                )
                input_swap = colors[source_zero] == 1
                output_swap = colors[target_zero] == 1
                safe &= not (input_swap and output_swap)
            safe_colorings += int(safe)
        assert alternating_colorings == 2
        assert safe_colorings == 0

    paths = ((1, 0, 2), (2, 3, 1))
    arcs = [arc for path in paths for arc in zip(path, path[1:])]
    assert len(arcs) == len(set(arcs))
    assert all(hamming(*arc) == 1 for arc in arcs)
    assert paths[0][0] == 1 and paths[0][-1] == sigma[1]
    assert paths[1][0] == 2 and paths[1][-1] == sigma[2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-dimension", type=int, default=4)
    args = parser.parse_args()

    expected = {
        1: Counter({0: 1, 2: 1}),
        2: Counter({0: 1, 2: 4, 4: 14}),
        3: Counter({0: 1, 2: 12, 4: 114}),
        4: Counter({0: 1, 2: 32, 4: 688}),
    }
    for dimension in range(1, args.max_dimension + 1):
        counts: Counter[int] = Counter()
        seen: set[tuple[int, ...]] = set()
        for tau in generate_low_slack_taus(dimension):
            assert tau not in seen
            seen.add(tau)
            displacement = sum(
                hamming(source, target) for source, target in enumerate(tau)
            )
            counts[displacement] += 1
            routes = construct_routes(dimension, tau)
            verify_routes(dimension, tau, routes)
        assert counts == expected[dimension], (dimension, counts)
        print(f"d={dimension}: verified {sum(counts.values())} low-slack routings {dict(counts)}")

    for dimension in range(1, min(args.max_dimension, 4) + 1):
        equalities = check_cut_equality(dimension)
        assert equalities == 2 * dimension
        print(f"d={dimension}: checked every subset, {equalities} nontrivial equality cuts")

    check_benes_example()
    print("Q2 Beneš example: both coordinate splits fail; explicit routing verified")


if __name__ == "__main__":
    main()
