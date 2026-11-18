# Solver and auditor prompts

## Source-verification prompt

Identify every credible mathematical statement called Szymanski's or
Szymański's Conjecture. For the hypercube-routing candidate, distinguish
rearrangeability by arbitrary directed paths from the refuted shortest-path
variant. Give primary-source citations, exact quantifiers, definitions,
parameter ranges, and current-status evidence. Do not attempt a proof.

## Contract-audit prompt

Compare `contract.md` against Szymanski (1989), Baudon-Fertin-Havel (2001), and
the REGS problem statement. Report every altered quantifier, domain,
definition, orientation convention, path condition, or parameter endpoint.
Check especially whether opposite orientations of one cube edge are separate
capacities, whether paths may share vertices, whether fixed points use empty
paths, and whether shortest paths are required. Do not solve the conjecture
until the contract is repaired.

## Solver kickoff prompt

Act as the primary mathematical researcher. Work against `contract.md`, not a
remembered version of the conjecture.

Begin with at least three incompatible approach families. For each, state:

1. its mechanism;
2. its first falsifiable lemma or construction target;
3. a quick counterexample test;
4. the concrete artifact you will produce next; and
5. what would make the route theorem-strength blocked.

Then pursue the two best routes far enough to produce mathematics, not a status
report. Record unsupported steps explicitly. Do not call a reduction,
numerical evidence, shortest-path counterexample, non-permutation request, or
conditional result a solution.

