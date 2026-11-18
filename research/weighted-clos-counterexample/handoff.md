# Blocked research handoff

Date: 2026-07-23

## Outcome

No breakthrough is claimed. This run did **not** find a counterexample to the
Chung--Ross weighted bipartite edge-colouring conjecture and did not prove the
conjecture.

The selected problem remains worthy and current: it is a long-standing
generalization of bipartite edge colouring with a direct multirate Clos/data
centre routing interpretation. A 2024 PODC paper still calls the \(2n-1\)
statement a popular conjecture.

## Corrected target

The first contract incorrectly selected \(n=2\). Ngo and Vu proved
\(m(2,r)=3\) in 2003 under the same local two-bin premise. The corrected first
open finite target is:

> Find a finite rationally weighted bipartite multigraph whose incident
> weights pack into three unit bins at every vertex but whose edges admit no
> five-colour weighted edge-colouring.

A counterexample must have at least three nonisolated vertices in each
bipartition because Ngo--Vu prove \(m(n,2)\le\lceil3n/2\rceil\).

## What was proved in this run

These are rigorous reductions, not a resolution of the main conjecture.

1. **Pairwise overloads cannot be the obstruction.** At local parameter \(n\),
   the heavy-edge subgraph has maximum degree at most \(n\), so König's theorem
   gives it \(n\) proper edge colours. All light edges share one additional
   pair-conflict colour. Hence every pair-conflict graph is
   \((n+1)\)-colourable, and is four-colourable at \(n=3\). Any five-colour
   failure must use an overloaded set of at least three incident edges.

2. **The \(\{3/5,2/5\}\) alphabet is always five-colourable.** Properly
   six-edge-colour the light subgraph and merge two light matchings. Properly
   three-edge-colour the heavy subgraph into three unmerged global colours.
   The possible loads are at most \(3/5+2/5=1\) or \(2/5+2/5=4/5\).

3. **Minimal-counterexample restrictions.** A minimum \(n=3\) counterexample
   would be connected, deletion-minimal, have maximum degree at least six and
   heavy maximum degree at most three, exclude non-pendant bridges, and obey
   the deletion-saturation inequality recorded in
   `notes/higher-order-theory.md`.

The two short colouring theorems need expert novelty review before being
described as new. They are used here only as verified search reductions.

## Exact computation completed

The continuous rational CEGAR engine was audited against naive and independent
exact checkers.

- Every connected simple \(3\times3\) bipartite topology was exhausted:
  10 canonical classes, all `UNSAT_TOPOLOGY`.
- A 30-topology sampled frontier covered \(3\times3\), \(3\times4\), and
  \(4\times4\) multigraphs with 8--12 edges. The four initial timeouts all
  closed as `UNSAT_TOPOLOGY` on longer runs.
- Nine additional max-min-diverse multigraph topologies with 9--13 edges also
  closed as `UNSAT_TOPOLOGY`.
- The fixed \(\{3/5,2/5\}\) search scanned all \(22^4=234{,}256\) labelled
  \(2\times2\) multiplicity arrays. Exactly 3,512 passed the construction
  filters, and every one had a five-colouring.
- No run emitted a counterexample.

For a reported fixed topology, the Z3 search is exact over all positive
rational weights satisfying exact local bin number three. The topology
frontier is not complete beyond simple \(3\times3\), and the Z3 UNSAT results
do not carry independently checkable proof objects.

## Verification and repaired failure

A hostile audit found that direct use of the \(n=3\) search class incorrectly
made any topology with an isolated vertex UNSAT. The CLI's connected searches
were unaffected. The branch was repaired and regression-tested.

Post-fix differential checks passed:

- exact-\(n=3\) master: 250/250;
- five-colour checker: 250/250;
- exact `Fraction` backtracker: 250/250;
- block clauses: 69/69 applicable cases;
- canonicalization: 250/250;
- sampler invariants: 120/120.

## First remaining blocker

There is no proved finite normal form for an arbitrary-weight \(n=3\)
counterexample. The surviving mechanism is a higher-order overload hypergraph
using at least three distinct incident edges and a richer weight alphabet.
Neither the current theory nor the literature supplies a bound on graph size,
degree, denominators, or number of weight classes that would make the search
complete.

## Highest-value next experiments

1. Prove or refute a three-weight normal-form lemma for a minimum
   counterexample. This would convert the continuous search into a finite
   marked-hypergraph problem.
2. Encode the five-colour deletion-saturation signatures directly into the
   CEGAR master, especially the \(2+3\) endpoint blocking rule for weights at
   most \(1/3\).
3. Search topology templates derived from critical non-5-colourable
   higher-order hypergraphs, instead of ranking random multigraphs by degree.
4. Add independently checkable SMT proof production before treating
   topology-level UNSAT as publishable evidence.
5. Send the two reduction proofs and the corrected contract to a weighted
   edge-colouring expert before any novelty claim or public announcement.

## Reproduction map

- Exact contract: `contract.md`
- Live claims and gaps: `ledger.md`
- Continuous search and results: `code/search_n3.py`, `notes/n3-search.md`
- Hostile audit: `notes/n3-verification-audit.md`
- Structural reductions: `notes/higher-order-theory.md`
- Pair-conflict theorem: `notes/pair5-theory.md`
- Fixed-alphabet theorem and search:
  `notes/marked-b5-theory.md`, `notes/marked-b5-search.md`
- Retired \(n=2\) pilot: `results/n2-pilot.md`
