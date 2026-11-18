# Exact solution contract

Status: **source-checked; candidate counterexample found**

## Primary problem

Hussak and Trehan ask:

> Does amnesiac flooding from multiple sources on a bipartite graph, where
> there is a fixed time of message transit greater than one round along a
> single edge, terminate?

Source: Section 5, Open Problem 2, *Termination of amnesiac flooding*,
Distributed Computing 36 (2023), 193-207.
https://doi.org/10.1007/s00446-023-00448-y

The publisher's current full-text page still displayed the problem as open on
2026-07-23. Exact-title and citation searches found no correction or later
resolution. This is bibliographic evidence, not proof that unpublished work
does not exist.

## Normalized model

Let `G=(V,E)` be a finite connected undirected bipartite graph and let
`I subset V`, with `|I| >= 2`, be the simultaneous source set. One undirected
edge `e*` has fixed transit time `tau > 1` in both directions. Every other edge
has transit time one.

Rounds use the timing convention in Section 4.2 of the primary paper:

1. In round 1, every source sends the message to every neighbor.
2. A message sent in round `r` on an edge of transit time `w` is delivered in
   round `r+w-1`.
3. In round `r>1`, a node that received the message in round `r-1` sends it to
   all and only the neighbors from which it did not receive in round `r-1`.
4. Messages travelling in opposite directions along a delayed edge pass one
   another at an internal tick. They do not cancel there.
5. A full flooding state contains all directed deliveries in the current round
   and all directed messages still in transit, including their remaining
   transit positions.

The process terminates only when this full state becomes empty.

## What a negative solution must exhibit

A counterexample must provide:

1. an explicit finite connected bipartite graph;
2. at least two simultaneous sources;
3. exactly one fixed, persistent, bidirectional delayed edge, with integer
   transit time greater than one;
4. a finite sequence of valid full flooding states;
5. two equal nonempty full states at distinct rounds.

The update rule is deterministic, so item 5 proves that the execution is
periodic and never terminates.

## Active witness

Use vertices `{a,b,c,d,e}`, edges

```text
ab, bc, cd, da, ae,
```

the bipartition `{a,c} | {b,d,e}`, sources `{c,e}`, transit time two on `ab`,
and transit time one on every other edge.

The completion criterion is the exact equality `S_5 = S_10`, with the common
state nonempty. The detailed certificate is in [witness.md](witness.md).

## Variant exclusions

- This is fixed-delay amnesiac flooding, not the adversarial
  Round-Delayed Amnesiac Flooding model introduced in 2026.
- The delayed edge is not replaced by an ordinary subdivision vertex. The
  paper explicitly explains why those dynamics differ.
- Delays are fixed, persistent, integer-valued, symmetric, and present on
  exactly one edge.
- Sources act simultaneously in round 1 and subsequently follow the same
  amnesiac forwarding rule as every other node.
- A round with no deliveries is not termination if a message remains in
  transit.
- The witness uses one message from multiple sources, not multiple distinct
  messages.
- The direct witness uses two nonadjacent sources. It therefore does not depend
  on any special interpretation of messages exchanged by adjacent sources.

## Verification plan

Correctness:

1. Check the graph, bipartition, source count, edge weights, and unique delayed
   edge directly.
2. Verify every transition in the round table by hand.
3. Run a dependency-free deterministic simulator that retains the complete
   delayed pipeline.
4. Assert the expected table and `S_5 = S_10`, rather than merely trusting the
   simulator's generic cycle detector.
5. Reimplement the transition independently and compare the resulting state
   sequence.
6. Reproduce Figure 6 of the source paper, including its stated repetition in
   rounds 5 and 13, to calibrate timing and tick semantics.

Novelty:

1. Search exact problem text, title, theorem number, citations, author pages,
   repositories, and errata.
2. Search the final graph, source pattern, and period, not only the paper title.
3. Ask the authors or a specialist to check the model interpretation, state
   table, theorem-proof diagnosis, and prior art before publication.

## Results that do not count

- a run that omits in-transit messages from the repeated state;
- a simulation using ordinary subdivision-node semantics;
- nontermination with two delayed edges, variable delay, message loss, or an
  asynchronous adversary;
- a non-bipartite graph;
- floating timing conventions that have not reproduced a published example;
- a search log without an explicit witness and transition certificate;
- a novelty claim based only on search-engine silence.

