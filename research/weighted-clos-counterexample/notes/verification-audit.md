# Hostile verification audit

Date: 2026-07-23

Status: **the active `n=2` research target is already solved affirmatively**.

Hung Q. Ngo and Van H. Vu, *Multirate Rearrangeable Clos Networks and a
Generalized Edge-Coloring Problem on Bipartite Graphs*, SIAM Journal on
Computing 32(4):1040–1049 (2003), DOI
[10.1137/S0097539702408235](https://doi.org/10.1137/S0097539702408235),
prove \(m(2,r)=3\). Their proof starts with exactly the local partition of each
vertex's incident edges into two unit-capacity groups and constructs three
global colour classes. Thus the exact finite frontier in `contract.md` cannot
contain a counterexample. The full Chung--Ross conjecture remains a different,
larger-\(n\) question. The contract's open-status section missed this prior
result.

## Code audit

The following parts of `code/search_cegar.py` are logically sound:

- A local-bin Boolean is attached separately to each endpoint incidence.
  Independent local partitions are therefore represented correctly. Fixing the
  first incidence at each vertex to bin zero only removes the symmetry that
  swaps the two bins at that vertex.
- Requiring some incident total to be strictly greater than one, together with
  explicit two-bin constraints, establishes exact \(n=2\).
- `colour[0] == 0` is a safe global-colour permutation break.
- A checker colouring is blocked by requiring at least one of its
  vertex/colour loads to be strictly greater than one. This is precisely the
  negation of feasibility for that colouring; equality at one remains feasible.
  The disjunction is invariant under a global permutation of colour names.
- There are finitely many colouring orbits. Hence master UNSAT after the
  accumulated exact block clauses rules out a counterexample for the encoded
  topology and **the active master domain**.
- Row/column canonicalization only relabels the two bipartition sides.
  Restricting to connected graphs is safe: a non-colourable disconnected
  instance has a non-colourable component, and a component with local parameter
  one is trivially one-colourable.

One reporting error was found and fixed. With the default mixed-weight
restriction, the master additionally requires a weight \(>1/2\) and a weight
\(\leq1/2\). `UNSAT_TOPOLOGY` previously claimed exhaustion of all local
exact-\(n=2\) weights. It only exhausted that slice. Results now contain:

- `search_scope: "mixed_weight_slice"` and an explicitly scoped reason, or
- `search_scope: "all_positive_weights"` when
  `--no-enforce-mixed-weights` is used.

No lemma in the audited record justifies excluding the all-\(\leq1/2\) domain.
Therefore only the second scope can rule out the whole positive-weight domain
for a topology.

`code/verify_exact.py` now accepts both its native
`weighted-clos-n2-v1` schema and the
`weighted-clos-counterexample-v1` schema emitted by the CEGAR search, directly
or inside a fixed/survey `witness` wrapper. It independently validates the
multiplicity matrix against separately identified edges, normalizes integer
edge IDs, verifies the reported exact-two-bin vertices, and then runs its own
exact exhaustive three-colour search.

## Controls and differential checks

Commands and observed results:

```text
python3 -m py_compile \
  research/weighted-clos-counterexample/code/search_cegar.py \
  research/weighted-clos-counterexample/code/verify_exact.py
```

Result: exit 0.

```text
python3 research/weighted-clos-counterexample/code/search_cegar.py \
  --mode controls --solver-timeout-ms 10000 --topology-seconds 30 \
  --max-iterations 100 --progress-every 0
```

Result: `passed: true`. The synthetic one-colour case produced
`SAT_WITNESS`; the three-colour two-parallel-edge case produced
`UNSAT_TOPOLOGY` with `search_scope: "all_positive_weights"`.

```text
python3 research/weighted-clos-counterexample/code/search_cegar.py \
  --mode fixed --matrix 2 --solver-timeout-ms 10000 \
  --topology-seconds 30 --max-iterations 100 --progress-every 0 \
  --enforce-mixed-weights

python3 research/weighted-clos-counterexample/code/search_cegar.py \
  --mode fixed --matrix 2 --solver-timeout-ms 10000 \
  --topology-seconds 30 --max-iterations 100 --progress-every 0 \
  --no-enforce-mixed-weights
```

Result: both returned `UNSAT_TOPOLOGY`. The first was explicitly scoped to
`mixed_weight_slice`; the second to `all_positive_weights`.

An inline deterministic Python differential harness used seed `20260723` and
250 random connected \(2\times2\) multigraph instances with 3–7 edges and
weights from
\(\{1/4,1/3,1/2,2/3,3/4,1\}\). It compared:

```text
CEGAR Z3 checker vs naive 3^|E| enumeration:       250/250 passed
CEGAR exact self-check vs naive enumeration:       250/250 passed
local master encoding vs naive two-bin enumeration: 250/250 passed
each generated block clause vs its definition:    250/250 passed
independent verifier vs naive enumeration:         250/250 passed
```

A wrapped CEGAR-schema \(K_{2,2}\) instance with all four weights \(2/3\) was
parsed successfully and rejected with the valid colouring
`{'0': 0, '1': 1, '2': 1, '3': 0}`. Changing its multiplicity matrix from four
edges to an inconsistent one was rejected before colouring with
`multiplicity matrix disagrees`.

## Residual limitations

- Z3 UNSAT is not accompanied by a DRAT/LRAT or other retained proof artifact.
  It is exact rational SMT evidence but still depends on trusting Z3 and the
  encoding. `UNSAT_TOPOLOGY` is not an independently checkable certificate.
- The fixed-mode process exits zero for `UNKNOWN`; automation must inspect the
  JSON `status`, not only the process exit code.
- Computational controls validate the tooling but cannot revive the closed
  `n=2` target or establish novelty.
