# Problem-selection record

The `do-a-breakthrough` selection protocol favors exact, finite, structurally
isolated counterexamples over famous conjectures with large hardness gravity.

The final shortlist was:

| Candidate | Primary source | Finite witness | Independent verifier | Main drawback |
|---|---|---:|---:|---|
| Multi-source amnesiac flooding with one delayed edge | Distributed Computing 2023, Open Problem 2 | excellent | excellent | open-status evidence was initially only medium-high |
| Directed hypercube routing | ITCS 2025, Conjecture 3 | excellent | excellent | first cases require a joint path-family feasibility certificate |
| Happy edges for parallel triangulation flips | SoCG 2026, Conjecture 3 | excellent | excellent | positive competition experiments |
| Group-labelled matroid proximity | ICALP 2025, Conjecture 1.1 | excellent | excellent | joint matroid and group-label search |
| Szymanski hypercube permutation routing | ICPP 1989 | good | good | `Q_5` begins with `32!` permutations |

Amnesiac flooding was selected because:

1. it is directly in distributed algorithms;
2. the conjectured universal behavior is refutable by one finite periodic
   execution;
3. the model has only Boolean directed-message state plus a finite delay
   pipeline;
4. known nontermination with two delayed edges supplies a nearby obstruction
   template;
5. multiple sources plausibly replace the phase memory lost when reducing from
   two delayed edges to one;
6. the expected smallest graph has only a handful of vertices;
7. a skeptical reader can verify the result from a ten-row table.

A bounded calibration search then produced the five-node witness. At that
point it dominated the other candidates: it was no longer merely tractable,
but had an explicit candidate solution with a cheap falsification path.

Primary sources:

- Hussak and Trehan, 2023:
  https://doi.org/10.1007/s00446-023-00448-y
- Chakrabarty and Seshadhri, 2025:
  https://doi.org/10.4230/LIPIcs.ITCS.2025.34
- Shadoks CG:SHOP team, 2026:
  https://doi.org/10.4230/LIPIcs.SoCG.2026.107
- Garamvölgyi et al., 2025:
  https://doi.org/10.4230/LIPIcs.ICALP.2025.85

