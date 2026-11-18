# Route B: exact computation

Status: **bounded computation audited; no counterexample**

Date: 2026-07-23
Primary run: Z3 4.15.4, Python API
Primary artifacts: `../results/2026-07-23-exact-routing/`

## Exact formulation

Vertices of \(Q_d\) are integers \(0,\ldots,2^d-1\), with directed arcs

\[
A_d=\{(v,v\mathbin{\mathsf{xor}}2^i):0\le v<2^d,\ 0\le i<d\}.
\]

For every non-fixed demand \(s\mapsto t\) and directed arc \(a\), the
original model has a Boolean variable \(f_{s,a}\). It enforces flow balance
\(+1\) at \(s\), \(-1\) at \(t\), and zero elsewhere; at most one selected
incoming and outgoing arc per commodity at a vertex; and capacity at most one
over commodities on every directed arc. Opposite orientations of an ordinary
cube edge have distinct capacities. Fixed points use the adopted zero-arc
path convention.

The unrestricted model permits every directed cube arc and has no path-length
bound. The `--shortest-only` control permits only arcs that strictly decrease
Hamming distance to the target; it is calibration only and says nothing about
the ordinary conjecture.

The hostile audit found the formulation exact. Selected support contains an
\(s\)-to-\(t\) walk by the usual reachable-set balance argument; deleting
cycles and repeated-vertex segments leaves a simple path and cannot create a
new capacity conflict. `verify_paths` then independently checks every
extracted witness for endpoints, adjacency, simplicity, fixed points, optional
shortestness, and global directed-arc uniqueness.

## Original run, retained exactly

`summary.json` records the first 84-instance batch with a 20-second limit per
instance:

| status | count |
|---|---:|
| SAT | 83 |
| UNSAT | 0 |
| unknown | 1 |

The 76 \(d\le4\) checks were all SAT. The \(d\le2\) component is exhaustive;
the \(d=3,4\) component is structured calibration, not a new proof. The
eight unrestricted Q5 candidates were antipodal and several mutations,
coordinate-rotation complements, and two seeded high-distance permutations.
Seven were SAT. Q5 high-distance mutation A, with total Hamming distance 136,
timed out both at 20 seconds and in a logged 120-second retry. Those two
records remain `unknown`: a timeout is not infeasibility evidence.

## Audit correction: all 84 experiment instances are now routed

The computational audit used a distinct whole-shortest-path packing search,
not the original flow encoding, on the one original unknown. It found a
32-demand certificate in 0.030414 seconds. The 136 used directed arcs equal
the sum of the demands’ Hamming distances, so every route is shortest. The
certificate is stored in
`../results/2026-07-23-exact-routing/audit-q5-high-distance-random-a-shortest-path-search-240s.json`.

`independent_verify.py` imports neither the original routing code nor Z3. It
independently reconstructed the cube, permutation, endpoints, adjacency,
simplicity, shortestness where declared, and directed-arc capacities. It
accepted all 83 original SAT certificates and the new shortest-path certificate.

Therefore the correct integrated statement is:

- the original time-limited batch remains **83 SAT, 1 unknown**;
- subsequently, all **84 experiment instances are known routable**;
- in particular, all **eight Q5 candidates are routable**;
- neither fact proves Q5 or yields information about the other \(32!\) input
  permutations sufficient for a counterexample search.

The alternate QF_FD encoding also timed out after 240 seconds on the same Q5
instance before the constructive certificate was found. It is retained as
another honest `unknown`, not negative evidence.

## Directed-metric search

For nonnegative directed-arc lengths \(\ell\), any arc-disjoint routing obeys

\[
\sum_v \operatorname{dist}_\ell(v,\sigma(v))
\le \sum_{a\in A_d}\ell(a).
\]

A strict reverse inequality is a checkable fractional, hence integral,
infeasibility certificate. The search tested uniform lengths, five
coordinate-cut metrics, and 2,000 seeded random integer metrics on Q5. No
strict certificate appeared; the best gap was zero for uniform lengths
(\(160-160\)). This finite sample has no universal implication.

## Reproduction

From `research/szymanski-conjecture/code/`:

```sh
python3 -m unittest -v test_routing.py
python3 independent_verify.py certificates ../results/2026-07-23-exact-routing \
  --output ../results/2026-07-23-exact-routing/audit-certificate-verification.json
python3 independent_verify.py path-search \
  ../results/2026-07-23-exact-routing/q5-high-distance-random-a.instance.json \
  --timeout-seconds 240 --seed 1989 \
  --output ../results/2026-07-23-exact-routing/audit-q5-high-distance-random-a-shortest-path-search-240s.json
```

All eight focused unit tests passed during the hostile audit. No computation
here is an UNSAT certificate, exhaustive Q5 search, or a solution.
