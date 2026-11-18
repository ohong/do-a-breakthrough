# Multirate Clos counterexample program

Search date: 2026-07-23

This directory is the durable research record for an attempted counterexample to
the Chung--Ross weighted bipartite edge-colouring conjecture, also called the
multirate Clos rearrangeability conjecture.

The active target is `n = 3`. The initially selected `n = 2` frontier was
retired after a primary-source audit found Ngo and Vu's 2003 proof that
`m(2,r) = 3`. A successful witness is now a finite rationally weighted
bipartite multigraph whose incident weights can be packed into three unit bins
at every vertex, but whose edges cannot be assigned to five global colours with
load at most one per vertex and colour.

No result in this directory should be called a breakthrough until:

1. the witness passes two independent exact verifiers;
2. the exhaustive non-colourability claim has a checkable certificate;
3. a fresh literature search and an expert establish novelty.

See [contract.md](contract.md) for the exact completion criteria and
[ledger.md](ledger.md) for the live status.

Final status for this run: **no counterexample and no resolution of the full
conjecture**. See [handoff.md](handoff.md) for the strongest proved reductions,
the exact tested frontier, and the first remaining blocker.
