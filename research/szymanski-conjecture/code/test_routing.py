from __future__ import annotations

import itertools
import random
import unittest

from metric_search import maximum_assignment
from routing import solve_routing, validate_permutation, verify_paths


class RoutingTests(unittest.TestCase):
    def test_rejects_non_permutation(self) -> None:
        with self.assertRaises(ValueError):
            validate_permutation(2, [0, 1, 1, 3])

    def test_all_q2_permutations_route_in_both_modes(self) -> None:
        for permutation in itertools.permutations(range(4)):
            for shortest_only in (False, True):
                result = solve_routing(
                    2, permutation, shortest_only=shortest_only
                )
                self.assertEqual(result.status, "sat", permutation)
                self.assertIsNotNone(result.paths)

    def test_fixed_points_use_no_arcs(self) -> None:
        result = solve_routing(3, list(range(8)))
        self.assertEqual(result.paths, {source: (source,) for source in range(8)})

    def test_opposite_arc_directions_have_separate_capacity(self) -> None:
        permutation = [1, 0, 2, 3]
        result = solve_routing(2, permutation, shortest_only=True)
        self.assertEqual(result.status, "sat")
        self.assertEqual(result.paths[0], (0, 1))
        self.assertEqual(result.paths[1], (1, 0))

    def test_independent_verifier_rejects_shared_directed_arc(self) -> None:
        permutation = [1, 3, 2, 0]
        bad_paths = {0: (0, 1), 1: (1, 0, 2, 3), 2: (2,), 3: (3, 1, 0)}
        with self.assertRaisesRegex(ValueError, "used by"):
            verify_paths(2, permutation, bad_paths)

    def test_independent_verifier_rejects_non_shortest(self) -> None:
        permutation = [1, 0, 2, 3]
        paths = {0: (0, 2, 3, 1), 1: (1, 0), 2: (2,), 3: (3,)}
        verify_paths(2, permutation, paths)
        with self.assertRaisesRegex(ValueError, "not shortest"):
            verify_paths(2, permutation, paths, shortest_only=True)

    def test_exact_maximum_assignment(self) -> None:
        weights = [[9, 2, 7], [6, 4, 3], [5, 8, 1]]
        value, permutation = maximum_assignment(weights)
        self.assertEqual(value, 21)
        self.assertEqual(len(set(permutation)), 3)

    def test_hungarian_matches_exhaustive_assignment(self) -> None:
        rng = random.Random(1989)
        for _ in range(10):
            weights = [[rng.randrange(20) for _ in range(4)] for _ in range(4)]
            expected = max(
                sum(weights[row][permutation[row]] for row in range(4))
                for permutation in itertools.permutations(range(4))
            )
            actual, _ = maximum_assignment(weights)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
