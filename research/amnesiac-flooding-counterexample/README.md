# A five-node counterexample to delayed multi-source amnesiac flooding

Research date: 2026-07-23

This directory records a candidate negative solution to Open Problem 2 in:

Walter Hussak and Amitabh Trehan, *Termination of amnesiac flooding*,
Distributed Computing 36 (2023), 193-207.
https://doi.org/10.1007/s00446-023-00448-y

The open problem asks whether amnesiac flooding from multiple simultaneous
sources always terminates on a finite connected bipartite graph when exactly one
edge has a fixed bidirectional transit time greater than one round.

The answer appears to be **no**. A five-vertex graph, two nonadjacent sources,
and one edge of transit time two enter an exact period-five orbit. The repeated
full state includes both delivered and in-transit messages.

The core witness is:

```text
      e
      |
      a ==2== b
      |       |
      d ----- c
```

All unlabeled edges have transit time one. The simultaneous sources are `c` and
`e`. The full flooding state in round 5 recurs in round 10.

This package also records a four-cycle witness with three sources. That smaller
instance appears to refute Theorem 4.3 of the same paper, but the five-node
answer to Open Problem 2 does not rely on the theorem or on the proposed
diagnosis of its proof.

Run the standalone verifier with:

```sh
node research/amnesiac-flooding-counterexample/code/cli.js
node --test research/amnesiac-flooding-counterexample/code/simulator.test.js
```

The CLI checks two equivalent labelings of the direct witness and separately
prints a `CALIBRATION` result for Figure 6 of the source paper. That calibration
has one source and two delayed edges, so the target-witness validator explicitly
rejects it.

Current claim strength:

- the state transition and period have been checked by two independently
  written simulators and a manual round table;
- the primary paper's published two-delay example was reproduced exactly as a
  model-calibration check;
- no correction or prior resolution was found in a search through 2026-07-23;
- the result has **not** yet been checked by the authors or an independent
  distributed-computing expert.

Do not present this as peer-reviewed or established until that external review
has happened. See [contract.md](contract.md), [witness.md](witness.md), and
[ledger.md](ledger.md).
