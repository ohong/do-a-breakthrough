# Exact \(n=3\) CEGAR search

Date: 2026-07-23

Status: **tested, no counterexample found**

## Why the frontier moved

Ngo and Vu prove \(m(2,r)=3\), so \(n=2\) is settled. They also prove
\(m(n,2)\le\lceil 3n/2\rceil\). At \(n=3\), a counterexample requiring six
colours must therefore have at least three nonisolated vertices in each
bipartition (apply the result to either side). Their paper reports
\(m(3,r)\le6\), with the proof omitted.

Primary source: Hung Q. Ngo and Van H. Vu, *Multirate Rearrangeable Clos
Networks and a Generalized Edge Coloring Problem*, SODA 2003 / SIAM J.
Comput. 2003, Theorem 4.1 and Corollary 5.1:
https://cse.buffalo.edu/~hungngo/papers/soda03.pdf

## Exact encoding

`code/search_n3.py` uses exact Z3 rationals.

- Every edge weight is in \((0,1]\).
- Every vertex has an explicit assignment of incident edges to three unit
  bins.
- For at least one vertex, every unordered two-bin partition overloads a bin.
  This proves the instance parameter is exactly \(n=3\).
- A second solver searches for a valid global five-colouring.
- Each discovered colouring orbit is permanently blocked in the weight master.
- `UNSAT_TOPOLOGY` exhausts the continuous rational weight space for that one
  topology. `UNKNOWN` records a real limit and is not upgraded to UNSAT.
- A candidate is emitted only after both SMT UNSAT and an exact
  `fractions.Fraction` backtracker find no five-colouring.

Controls:

```sh
python3 research/weighted-clos-counterexample/code/search_n3.py \
  --mode controls --seed 20260723 --topology-seconds 10 --progress-every 0
```

Result: passed. Three parallel edges with exact local bin number three defeat
the synthetic two-colour checker (`SAT_WITNESS`), while the same topology is
exhaustively harmless under five colours (`UNSAT_TOPOLOGY`).

## Focused sampled search

Command:

```sh
python3 research/weighted-clos-counterexample/code/search_n3.py \
  --mode survey \
  --seed 20260723 \
  --pool-per-bucket 300 \
  --selected-per-bucket 2 \
  --max-multiplicity 3 \
  --topology-seconds 6 \
  --total-seconds 220 \
  --solver-timeout-ms 5000 \
  --max-iterations 20000 \
  --progress-every 1000 \
  --output /tmp/weighted-clos-n3-focused.json
```

Frontier:

- shapes: \(3\times3\), \(3\times4\), \(4\times4\);
- edge counts: 8, 9, 10, 11, 12;
- 300 deterministic connected samples generated per shape/edge-count bucket;
- two high-degree-biased, row/column-isomorphism-distinct topologies selected
  per bucket;
- 30 selected and searched topologies total;
- topology selection is sampled, not exhaustive;
- each reported UNSAT topology has an exact, unrestricted positive-rational
  weight search subject only to the contract.

Results:

- 26 `UNSAT_TOPOLOGY`;
- 4 `UNKNOWN`, all 12-edge cases that hit the six-second topology limit;
- 0 `SAT_WITNESS`;
- 45.411 seconds total.

Unknown topology matrices:

1. `0,2,1;2,3,2;0,1,1` (\(3\times3\), 124 CEGAR iterations);
2. `1,0,2;1,2,3;1,0,2` (\(3\times3\), 83 iterations);
3. `2,3,2,1;0,1,0,1;0,0,0,2` (\(3\times4\), 98 iterations);
4. `0,0,1,0;0,0,2,2;2,1,3,1` (\(3\times4\), 133 iterations).

## First unsupported assumption and next step

There is no proved bound placing a minimum \(n=3\) counterexample within these
shapes, edge counts, multiplicities, or sampled topology scores. Search failure
therefore gives no general theorem. Also, Z3 topology-level UNSAT responses do
not yet have independently checkable proof certificates.

The next bounded computation should resume the four 12-edge unknowns with
longer per-topology limits, then increase topology diversity rather than merely
raising the degree-bias score.

## Resumed unknowns

The four unknowns were rerun sequentially with the same seed, 45 seconds per
topology, a 30-second solver-call timeout, and 100,000 maximum CEGAR iterations:

```sh
python3 research/weighted-clos-counterexample/code/search_n3.py \
  --mode fixed --matrix '<matrix>' \
  --seed 20260723 \
  --topology-seconds 45 \
  --total-seconds 235 \
  --solver-timeout-ms 30000 \
  --max-iterations 100000 \
  --progress-every 2000 \
  --output /tmp/n3-resume-<name>.json
```

All four closed as `UNSAT_TOPOLOGY`:

| Matrix | Blocked colouring orbits | Seconds |
|---|---:|---:|
| `0,2,1;2,3,2;0,1,1` | 139 | 13.101 |
| `1,0,2;1,2,3;1,0,2` | 129 | 10.778 |
| `2,3,2,1;0,1,0,1;0,0,0,2` | 101 | 11.078 |
| `0,0,1,0;0,0,2,2;2,1,3,1` | 136 | 11.890 |

No witness was emitted.

## Diversity-biased follow-up sample

With all unknowns closed early, a separate deterministic sample used seed
20260724. For each of the \(3\times3\), \(3\times4\), and \(4\times4\) shapes,
600 connected matrices with 9--13 edges were generated. Selection did not use
the degree score: one deterministic seeded matrix was chosen, then two more
were chosen by maximizing their minimum entrywise \(L_1\) matrix distance from
the already selected matrices. Row/column canonical keys removed isomorphic
duplicates.

The nine selected fixed-mode runs used 12 seconds per topology, a 10-second
solver timeout, and 100,000 maximum iterations. All nine returned
`UNSAT_TOPOLOGY`; no run timed out and no witness was emitted.

| Shape | Matrix | Blocked orbits | Seconds |
|---|---|---:|---:|
| \(3\times3\) | `0,1,1;1,0,2;2,1,2` | 24 | 0.299 |
| \(3\times3\) | `2,0,3;2,0,2;1,2,0` | 70 | 1.340 |
| \(3\times3\) | `0,1,3;3,0,0;2,1,1` | 36 | 0.480 |
| \(3\times4\) | `2,1,1,1;1,1,1,0;1,1,1,2` | 25 | 0.397 |
| \(3\times4\) | `0,0,3,0;0,1,0,0;2,1,2,1` | 34 | 0.718 |
| \(3\times4\) | `3,0,0,2;0,0,2,2;2,1,1,0` | 103 | 1.614 |
| \(4\times4\) | `1,2,1,0;0,1,2,1;1,0,1,0;0,1,1,0` | 43 | 0.604 |
| \(4\times4\) | `0,0,0,1;1,2,1,1;0,1,0,0;2,0,2,2` | 118 | 2.082 |
| \(4\times4\) | `0,0,1,2;1,1,0,0;0,0,0,2;1,1,0,1` | 11 | 0.112 |

These are exact results for thirteen individual topologies, not an exhaustive
topology frontier. The unsupported size-bound and solver-certificate gaps
remain unchanged.

## Exhaustive simple \(3\times3\) topology frontier

The final bounded run exhaustively generated every connected simple
\(3\times3\) bipartite topology with no isolates. Canonicalization quotiented
independent row permutations, independent column permutations, and transposing
the matrix (swapping the two bipartitions). There are 13 classes before the
transpose quotient and 10 after it.

The ephemeral harness used:

```sh
# Generate with search_cegar.generate_topologies(3,3,3,3,5,9,1),
# quotient transpose using search_n3.canonical_key, then for every topology:
N3CegarSearch(
    topology,
    SearchConfig(
        colour_count=5,
        seed=20260723,
        solver_timeout_ms=15000,
        topology_seconds=20,
        max_iterations=100000,
        progress_every=5000,
    ),
).run()
```

Exact output was retained at
`/tmp/n3-simple-3x3-exhaustive.json`.

| Edges | Canonical topologies | `UNSAT_TOPOLOGY` | `UNKNOWN` | `SAT_WITNESS` |
|---:|---:|---:|---:|---:|
| 5 | 3 | 3 | 0 | 0 |
| 6 | 3 | 3 | 0 | 0 |
| 7 | 2 | 2 | 0 | 0 |
| 8 | 1 | 1 | 0 | 0 |
| 9 | 1 | 1 | 0 | 0 |
| **Total** | **10** | **10** | **0** | **0** |

Runtime was 0.338 seconds. Thus the topology frontier is exhaustive for
connected simple \(3\times3\) bipartite graphs, and the continuous rational
weight space was exact for every UNSAT topology. This does not cover parallel
edges or larger bipartitions. No further search expansion was performed.
