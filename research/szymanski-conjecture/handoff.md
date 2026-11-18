# Blocked handoff: Szymanski's Conjecture

Integration date: 2026-07-23

## Outcome

This run did **not** solve Szymanski’s Conjecture. No counterexample, complete
proof, or novelty claim is justified. The honest conclusion is that the
arbitrary-path, directed-arc-disjoint permutation-routing problem remains
open from dimension 5 onward, subject to the targeted-search caveat in
`notes/source-status.md`.

The target is fixed in `contract.md`. Do not accidentally substitute the
shortest-path strengthening, which is already false, or a non-bijective
2-to-1 request, which is a different problem.

## Audited progress

1. `notes/B-computation.md` and `notes/computational-audit.md` establish that
   all 84 experiment instances are routable. Preserve the distinction between
   the original batch (`83 SAT / 1 unknown`) and the later independent
   shortest-path witness that settles the sole unknown. Of these instances,
   eight are unrestricted Q5 candidates.
2. `notes/solver-structural.md` and `notes/structural-audit.md` prove the
   automatic directed-cut condition, slack conservation, and shortest routing
   for all \(\Delta\le4\) permutations. The metric LP is an exact fractional
   obstruction mechanism, not an integral proof method.
3. `notes/solver-theory.md` and `notes/theory-audit.md` validate the
   single-cycle theorem for \(2\le k\le d+1\), after strengthening the
   hub-fan intersection hypothesis. They also give explicit counterexamples
   to several restricted induction architectures, not to the conjecture.
4. `notes/slack-six.md` and `notes/slack-six-audit.md` prove that every
   permutation with \(\Delta\le6\) has a shortest routing. The mathematical
   proof passed hostile review, but its strong \(Q_p\), \(p\le3\), dependency
   is reported in Baudon--Fertin--Havel (2001); the original Szymanski (1989)
   proof was not retrieved. It is therefore source-pending under the strict
   primary-source contract, and no novelty claim is made.

## Repairs that must be retained

- In the path-order cycle criterion, reverse the relevant terminal subpath,
  not necessarily the whole ambient path.
- In the hub-fan criterion, supporting paths must pairwise intersect only at
  the hub.
- Tail-switched walks must be reduced to paths by cycle deletion before being
  called paths.
- Do not claim universal Beneš/cycle-flip satisfiability or sufficiency of a
  connected tail-switch intersection graph.
- Do not treat a solver timeout, metric-sampling failure, or finite SAT batch
  as a proof of infeasibility or a proof of the conjecture.

## Exact blockers

- Integral cut sufficiency for these demands is equivalent in force to the
  conjecture.
- Universal fractional feasibility and fractional-to-integral rounding are
  separate unproved steps.
- Constructing and packing arbitrary ordered trails for multiple cycles is
  theorem-strength.
- Naive factor composition can reuse directed arcs, already on Q1.
- The next possible slack obstruction is \(\Delta=8\). The active-coordinate
  reduction stops there because a mechanical extension would require the
  false strong Q4 statement.

## Final bounded-probe outcome

The single-\((d+2)\)-cycle probe ended **blocked**, not proved or refuted.
`notes/d-plus-two-probe.md` records the exact missing paired-branch lemma.
The ordinary fan lemma does not ensure that a prescribed terminal-avoiding
path can coexist with the other \(d-1\) terminal branches, and contracting
that path does not preserve the required connectivity. A simpler one-bridge
split is refuted by an explicit \(Q_3\) terminal order, but that refutes only
the construction.

## Re-entry commands

```sh
cd research/szymanski-conjecture/code
python3 -m unittest -v test_routing.py
python3 independent_verify.py certificates ../results/2026-07-23-exact-routing \
  --output ../results/2026-07-23-exact-routing/audit-certificate-verification.json
python3 audit_structural.py
python3 audit_slack_six.py \
  ../results/2026-07-23-slack-six/exhaustive-and-lifts.json \
  --output ../results/2026-07-23-slack-six/independent-audit.json
```

The research directory is intentionally ignored by git. Preserve its result
files: they are the evidence trail, not disposable scratch output.
