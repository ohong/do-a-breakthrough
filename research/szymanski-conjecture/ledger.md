# Research ledger

Last integrated: 2026-07-23

Labels: `literature`, `proved/audited`, `source-pending`, `tested/audited`,
`refuted`, `repaired`, `unverified`, `frontier`, or `blocked`.
“Proved/audited” means the written argument passed the hostile internal audit,
not that it has external peer review or is novel. `source-pending` means the
mathematics passed but an external dependency has not met the contract's
primary-source requirement.

## Contract and literature status

- `tested/audited`: the target is arbitrary-path, directed-arc-congestion-one
  rearrangeability for every permutation of \(\overleftrightarrow{Q_d}\),
  \(d\ge1\). See `contract.md`.
- `literature`: the ordinary conjecture is proved through \(d=4\), while its
  shortest-path strengthening is false. See `notes/source-status.md`.
- `tested/audited`: no accepted resolution for \(d\ge5\) was found in the
  targeted 2026-07-23 search. This is not exhaustive bibliographic or novelty
  certification; the 1989 full text was not obtained.

## Audited positive results and exact scope

| ID | Claim | Status | Scope / artifact |
|---|---|---|---|
| T1 | Cycle deletion converts a routing walk to a simple path without creating an arc conflict. | proved/audited | `notes/theory-audit.md` item 2; fixed points separately use the adopted empty-path convention. |
| T2 | Every ordinary directed vertex-cut condition is automatic for a permutation demand; equality is classified by coordinate halfcubes. | proved/audited | `notes/solver-structural.md` C1--C3; `notes/structural-audit.md`. Necessary only. |
| T3 | \(U+E=\Delta\) slack conservation, Eulerian unused arcs, and the complete \(\Delta\in\{0,2,4\}\) classification with shortest routings. | proved/audited | `notes/solver-structural.md` S1--S4; `notes/structural-audit.md`. Proper subclass only. |
| T4 | Directed-metric inequalities exactly characterize fractional multiflow feasibility; a strict rational violation is a checkable obstruction. | proved/audited | `notes/solver-structural.md` M1--M3; `notes/structural-audit.md`. Does not yield integral routing. |
| T5 | Single nontrivial cycles of length \(2\le k\le d+1\) are routable. | proved/audited after repair | `notes/solver-theory.md` B3--B5; the fan paths must pairwise meet only at the hub. |
| T6 | Conditional portal and Beneš split lemmas, ordered-trail formulation, translations, direct products, and skew products. | proved/audited where conditional | `notes/solver-theory.md`, `notes/coordinator-observations.md`, and `notes/theory-audit.md`. None supplies universal induction. |
| T7 | Every \(\sigma\) with \(\Delta=d2^d-\sum_x h(x,\sigma(x))\le6\) has a directed-arc-disjoint shortest routing. | proved/audited; source-pending | `notes/slack-six.md` and `notes/slack-six-audit.md`. Uses the strong \(Q_p\), \(p\le3\), result explicitly reported by Baudon--Fertin--Havel (2001); the original Szymanski (1989) proof was not retrieved. No novelty claim. |

## Computation

| ID | Result | Status | Evidence |
|---|---|---|---|
| C1 | Original 84-instance run: `83 SAT / 0 UNSAT / 1 unknown`. | tested/audited | `results/2026-07-23-exact-routing/summary.json`; 20-second per-instance bound. |
| C2 | All 83 original SAT witnesses independently validate. | tested/audited | `code/independent_verify.py` and `results/2026-07-23-exact-routing/audit-certificate-verification.json`. |
| C3 | The sole original unknown, Q5 high-distance mutation A, has an independently constructed shortest-path packing. | tested/audited | `results/2026-07-23-exact-routing/audit-q5-high-distance-random-a-shortest-path-search-240s.json`. |
| C4 | Therefore all 84 experiment instances are known routable, including all 8 Q5 candidates. | tested/audited | C1 plus C3. This is neither a Q5 proof nor a meaningful fraction of \(32!\). |
| C5 | 2,006 sampled Q5 directed metrics found no strict dual obstruction. | tested/audited | `results/2026-07-23-exact-routing/metric-search.json`. Bounded negative evidence only. |

## Repairs and failures

1. `repaired`: the contract no longer implies a shortest-path requirement;
   it explicitly treats fixed points as an adopted empty-path convention and
   separates sourced facts from inferences.
2. `repaired`: the path-order proof must send the final route along the
   \(x_1\)-to-\(x_k\) subpath in reverse, not necessarily all of its ambient
   path.
3. `repaired`: the hub-fan theorem requires supporting paths to intersect
   pairwise only at the hub. “Internally vertex-disjoint” alone is ambiguous
   and insufficient under the weak reading.
4. `refuted`: universal one-crossing portal induction. A routable Q3
   permutation defeats every such cut embedding.
5. `refuted`: universal Beneš/cycle-flip split satisfiability. It already
   fails for restricted architectures on routable Q2 and Q3 examples.
6. `refuted`: naive sequential composition of routable factors, already in
   Q1, because it can reuse each directed arc.
7. `unverified`: connectedness of a tail-switch intersection graph suffices;
   no cube certificate or proof is present.

## Live blockers and bounded-probe outcomes

- `blocked`: cube cut sufficiency for integral multicommodity routing would be
  the full conjecture in different words.
- `blocked`: universal fractional feasibility and, separately,
  fractional-to-integral rounding.
- `blocked`: packing arbitrary ordered trails for multiple permutation cycles.
- `frontier`: the next possible slack obstruction is \(\Delta=8\). The active-
  coordinate proof for \(\Delta\le6\) would require the false strong Q4
  statement if extended mechanically, so a new idea is needed.
- `blocked`: the first uncovered single-cycle case, a single
  \((d+2)\)-cycle. The paired-branch construction needs a prescribed
  terminal-avoiding path plus \(d-1\) disjoint terminal branches; the ordinary
  fan lemma does not provide this, and contracting the prescribed path does
  not preserve the needed connectivity. A simpler one-bridge split is
  refuted by the explicit \(Q_3\) order in `notes/d-plus-two-probe.md`.

No entry in this ledger proves or disproves Szymanski’s Conjecture.
