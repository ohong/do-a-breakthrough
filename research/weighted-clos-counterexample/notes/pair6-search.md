# Route A3 pair-conflict search: retired before execution

## Status

**Closed by theorem. No search run was performed.**

An unexecuted prototype targeted a pair-conflict graph that was not
5-colourable. The target cannot exist, so the dead prototype was removed.

## Closing argument

For a locally \(n\)-bin-packable weighted bipartite multigraph, call an
original edge heavy when its weight is greater than \(1/2\), and light
otherwise.

1. At most \(n\) heavy edges are incident with any original vertex, because
   two heavy edges cannot occupy the same local unit bin. The heavy-edge
   subgraph is therefore bipartite with maximum degree at most \(n\).
2. By König's line-colouring theorem, its heavy edges have a proper
   \(n\)-edge-colouring.
3. In the pair-conflict graph, two light edges never conflict: their weights
   sum to at most one. Give every light edge one additional colour.
4. The heavy and light palettes are disjoint. Hence the full pair-conflict
   graph is \((n+1)\)-colourable.

At \(n=3\), every representable pair-conflict graph is therefore
4-colourable, much stronger than the earlier six-colour bound. In particular,
a 6-chromatic or merely non-5-colourable pair-conflict witness is impossible.
Pairwise conflicts cannot supply the desired counterexample.

This does **not** prove that four weighted colours suffice: a colour class of
three or more pairwise compatible light edges can still overload a vertex.
Any remaining obstruction must use such higher-order load constraints.

## Retired search design

The proposed search used the exact alphabet

\[
\{1/4,1/3,2/5,1/2,3/5,2/3,3/4\},
\]

explicit local three-bin certificates, deterministic equal-weight stub
matching on \(3\times3\) through \(5\times5\) bipartitions, and exact DSATUR
for five-colourability. It was stopped before compilation or sampling once
the theorem above was identified. This section records the abandoned
construction route; no code or computation from it is evidence.
