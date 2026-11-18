# Handoff

## Result

The five-node, two-source instance in [witness.md](witness.md) enters a
nonempty period-five orbit. Under the published fixed-delay semantics, it gives
a negative answer to Hussak--Trehan Open Problem 2.

## Next required action

Send the compact witness, round table, and verifier to Walter Hussak, Amitabh
Trehan, or another distributed-algorithms expert. Ask them to check:

1. the round timing and source semantics;
2. the equality `S_5=S_10`;
3. whether the result or an erratum already exists off-index;
4. the separate proposed counterexample and proof defect for Theorem 4.3.

Do not lead with a broad novelty claim. Lead with the explicit state table and
ask for falsification.

## Publication path if confirmed

1. freeze the verifier output and its source hash;
2. add an independently maintained second implementation;
3. write a short note separating the direct answer to Open Problem 2 from the
   correction to Theorem 4.3;
4. include the complete transition certificate in the paper, not only a link
   to code;
5. credit the primary authors and invite them to co-audit the correction.

## Scope

No claim is made about:

- all minimal counterexamples;
- variable or adversarial delays;
- multiple distinct messages;
- a replacement positive characterization of terminating instances.

