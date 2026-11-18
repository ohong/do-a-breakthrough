# Hostile verification audit: `search_n3.py`

Date: 2026-07-23

Status: **sound on the searched domain after one isolated-vertex fix**.

## Finding and fix

The original isolated-vertex branch added `False` directly to the master. This
made every topology containing an isolate UNSAT, even when another component
was locally three-packable and not two-packable. A concrete regression was:

```text
topology matrix: 4;0
weights: 2/3, 1/4, 1/2, 3/4
expected exact-n=3 master result: SAT
original result: UNSAT
```

The four weighted edges fit into three bins as
`(3/4 + 1/4), (2/3), (1/2)` and have total weight greater than two, so they
cannot fit into two bins. The isolated `L1` is harmless.

The branch now contributes `False` only to the per-vertex disjunction saying
that some vertex is not two-packable. It no longer makes the whole topology
infeasible. This defect did not affect the completed CLI searches:
`--mode fixed` rejects disconnected topologies and the survey sampler produces
connected topologies with no isolates.

`two_bin_partitions(())` itself was already correct: it emits the single
empty/empty partition. Degree-one vertices were also correct and cannot witness
exact \(n=3\).

## Encoding audit

For every edge, the master uses an exact real weight in `(0, 1]`. At each
endpoint incidence it independently chooses one of three local bins and limits
each bin load to one. Fixing the first incident edge to bin zero is safe:
every three-bin packing has a representative obtained by renaming that
vertex's bins. Endpoint packings remain independent.

For a nonempty incident edge set of degree \(d\),
`two_bin_partitions` enumerates all \(2^{d-1}\) unordered two-bin partitions by
fixing the first edge in bin zero. A vertex is declared not two-packable only
when every partition has a bin load strictly greater than one. This is exactly
the negation of a two-bin packing whose loads are each at most one. Requiring
at least one such vertex, while all vertices have explicit three-bin packings,
correctly encodes exact local parameter three.

The checker assigns one of five colours to every edge and constrains every
vertex/colour load to at most one. `colour[0] == 0` is a safe global colour-name
symmetry break.

For a checker colouring, the block clause requires at least one of its
vertex/colour loads to be strictly greater than one under future weights. This
is exactly the negation of that colouring's feasibility. Empty colour classes
are safely omitted because they cannot overload. The clause is invariant under
a global permutation of colour names, so one checker representative blocks its
entire colour orbit.

There are finitely many colour partitions. Consequently, master UNSAT after
the accumulated exact block clauses rules out a counterexample for that fixed
topology and the full encoded weight domain. Unlike the earlier \(n=2\)
search, `search_n3.py` has no mixed-weight or denominator restriction:
`UNSAT_TOPOLOGY` covers all positive weights at most one that satisfy exact
local \(n=3\).

The independent `Fraction` backtracker orders edges by decreasing weight and
uses a restricted-growth colour sequence: an edge may reuse an introduced
colour or introduce the next colour. This enumerates every colouring up to a
global colour permutation. It checks exact rational loads at both endpoints,
so its SAT/UNSAT result is independent of the SMT checker.

## Sampling and canonicalization

`canonical_key` takes the minimum multiplicity matrix under every row and
column permutation, so it safely deduplicates vertex relabelings. It does not
canonicalize transposition for square matrices. This can retain a topology and
its bipartition-swapped copy, wasting survey capacity, but cannot omit a class
or create a false result.

The connected sampler preserved requested edge counts, multiplicity at most
three, and nonisolated connected vertices in testing. Its topology frontier is
explicitly incomplete:

- only shapes `3x3`, `3x4`, and `4x4`;
- only 8 through 12 edges;
- multiplicity at most three;
- a finite random pool, ranked heuristically;
- at most the selected number of isomorphism classes per bucket.

Therefore `UNSAT_TOPOLOGY` is exhaustive in weights only for one returned fixed
topology. Survey completion is not evidence that the full \(n=3\) conjecture
has been exhausted.

## Verification

Compilation and built-in controls:

```text
python3 -m py_compile \
  research/weighted-clos-counterexample/code/search_n3.py

python3 research/weighted-clos-counterexample/code/search_n3.py \
  --mode controls --solver-timeout-ms 10000 --topology-seconds 30 \
  --max-iterations 500 --progress-every 0
```

Result: compilation exited zero and controls returned `passed: true`. The
synthetic two-colour case produced `SAT_WITNESS`; the target five-colour case
produced `UNSAT_TOPOLOGY`.

The fixed unrestricted-weight control:

```text
python3 research/weighted-clos-counterexample/code/search_n3.py \
  --mode fixed --matrix 3 --solver-timeout-ms 10000 \
  --topology-seconds 30 --max-iterations 100 --progress-every 0
```

Result: `UNSAT_TOPOLOGY` after one blocked colouring.

The isolated regression after the fix returned:

```text
isolated-only, matrix 0:                   UNSAT
degree-one, matrix 1 with weight 1:        UNSAT
exact component plus isolate, matrix 4;0: SAT
```

A deterministic inline differential harness, seed `20260723`, tested 250 tiny
random bipartite multigraphs with 1–7 edges and weights from
`{1/4, 1/3, 1/2, 2/3, 3/4, 1}`. Sixty cases contained isolates. Results:

```text
exact-n=3 master vs naive 3-bin/2-bin enumeration: 250/250
five-colour SMT checker vs naive 5^|E| enumeration: 250/250
Fraction backtracker vs naive enumeration:          250/250
production block clause vs its definition:            69/69
canonical key under random row/column relabeling:    250/250
```

The same harness tested 120 random connected sampler outputs and a 30-topology
sampled frontier for connectivity, edge count, multiplicity bounds, and
canonical-key uniqueness. All passed.

A separate negative five-colour test used six parallel unit edges. The SMT
checker, Fraction backtracker, and naive enumeration all returned
uncolourable.

`git diff --check` passed after the fix.

## Residual limitations

- Z3 UNSAT has no retained DRAT, LRAT, or other independently checkable proof
  artifact. It depends on trusting Z3 and the audited encoding.
- The survey topology frontier is sampled and materially incomplete, as
  detailed above.
- Deadline checks in the Fraction backtracker occur every 4096 visited nodes,
  so runtime limits are approximate rather than hard. This affects scheduling,
  not logical answers.
- Fixed mode exits zero for `UNKNOWN`; callers must inspect the JSON `status`.
