# Szymanski's Conjecture research record

Status: **blocked research handoff, not a solution**

Search and audit date: 2026-07-23

This record studies the surviving rearrangeability conjecture for the
bidirected hypercube: every permutation of the vertices should admit
pairwise directed-arc-disjoint routes. It does **not** study the stronger
shortest-path variant, which has counterexamples.

No proof of the full conjecture, counterexample, or novelty claim was
obtained. The project instead fixes the target, records bounded computation,
proves several audited proper subclasses and necessary conditions, and
records the exact points where the arguments stop.

## Target and status

The normalized target is stated in `contract.md`. The literature record in
`notes/source-status.md` supports the following cautious status: Szymanski
proved dimensions through 3; Baudon--Fertin--Havel proved dimension 4; the
arbitrary-path statement remains listed as open from dimension 5 onward.
The original 1989 full text was not retrievable in this run, and the later
literature search was targeted rather than exhaustive. Those limitations rule
out a novelty certification.

## What survived hostile review

- Exact computation found routings for all 84 bounded test instances. The
  original Z3 batch was honestly `83 SAT / 1 unknown`; an independently
  verified shortest-path certificate subsequently settled that one instance.
- Every ordinary directed vertex-cut condition is automatic for a permutation
  demand in a bidirected cube, but integral cut sufficiency remains exactly
  the missing theorem-strength step.
- Every permutation with
  \(\Delta=d2^d-\sum_x h(x,\sigma(x))\le6\) is shortest-path routable. The
  proof passed hostile mathematical review, but under the strict contract it
  is source-pending because its low-dimensional theorem is reported by
  Baudon--Fertin--Havel (2001) and the original Szymanski (1989) proof was not
  retrieved. The next possible slack obstruction is \(\Delta=8\).
- A weighted directed-metric violation is an exact certificate of fractional
  (hence integral) infeasibility; proving every such inequality would establish
  only fractional routability, not the required integral packing.
- Several restricted induction architectures are explicitly refuted without
  refuting the conjecture. A constructive single-cycle theorem survives for
  cycle lengths \(2\le k\le d+1\).

See `ledger.md` for the claim-by-claim audit status and `handoff.md` for the
next bounded targets.

## Files

- `contract.md`: exact completion criteria and adopted conventions.
- `notes/source-status.md`: sources, status, and literature caveats.
- `ledger.md`: audited claims, repairs, refuted methods, and blockers.
- `notes/B-computation.md`: exact encodings, results, and independent audit.
- `notes/slack-six.md`, `notes/slack-six-audit.md`: the \(\Delta\le6\)
  theorem, finite regression evidence, and hostile review.
- `notes/d-plus-two-probe.md`: the blocked first single-cycle case beyond the
  hub-fan theorem and its exact missing lemma.
- `notes/solver-theory.md`, `notes/solver-structural.md`: full derivations.
- `notes/theory-audit.md`, `notes/structural-audit.md`,
  `notes/computational-audit.md`: hostile reviews.
- `code/`: reproducible solvers and independent validators.
- `results/`: immutable experiment inputs, witnesses, and audit certificates.
- `handoff.md`: honest blocked handoff and next frontiers.
