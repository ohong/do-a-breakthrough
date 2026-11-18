# Exact solution contract

Status: **source-checked**

## Problem intake

Problem title: Chung--Ross weighted bipartite edge-colouring conjecture
(multirate Clos rearrangeability).

Primary statement:

> "Given an instance of the weighted bipartite edge coloring problem, there is a
> proper weighted coloring using at most \(2n-1\) colors where \(n\) denotes the
> maximum over all the vertices of the number of unit-sized bins needed to pack
> the weights of edges incident at the vertex."

Source: Uriel Feige and Mohit Singh, *Edge Coloring and Decompositions of
Weighted Graphs*, ESA 2008, Conjecture 1.1, pp. 1--2.
https://www.wisdom.weizmann.ac.il/~feige/mypapers/edgecoloring.pdf

Current open-status evidence:

Miguel Alves Ferreira, Nirav Atre, Justine Sherry, and João Luís Sobrinho,
*Impossibility Results for Data-Center Routing with Congestion Control and
Unsplittable Flows*, PODC 2024, §6, calls it a "popular conjecture" and states
that a Clos network is multirate rearrangeable iff \(m\ge 2n-1\), with best
reported lower and upper bounds \(\lceil 5n/4\rceil\) and
\(\lceil 20n/9\rceil\).
https://doi.org/10.1145/3662158.3662777

Open status was searched again on 2026-07-23. No later resolution was found.
That is bibliographic evidence, not proof that unpublished work does not exist.

Small-parameter correction:

Hung Q. Ngo and Van H. Vu, *Multirate Rearrangeable Clos Networks and a
Generalized Edge-Coloring Problem on Bipartite Graphs*, SIAM Journal on
Computing 32(4), 2003, prove \(m(2,r)=3\). They also report
\(m(3,r)\le 6\), while the Chung--Ross bound at \(n=3\) would be five.
Consequently \(n=2\) is closed and the first unresolved finite frontier used by
this project is \(n=3\).
https://doi.org/10.1137/S0097539702408235

## Definitions and conventions

Let \(G=(L\mathbin{\dot\cup}R,E)\) be a finite bipartite multigraph. Parallel
edges are allowed and loops are not. Each edge \(e\) has a weight
\(w(e)\in[0,1]\).

A `k`-colour weighted edge-colouring is a function
\(c:E\to\{0,\ldots,k-1\}\). It is **proper** when

\[
  \sum_{\substack{e\ni v\\c(e)=i}} w(e)\le 1
\]

for every vertex \(v\) and colour \(i\).

For a vertex \(v\), let \(b(v)\) be the minimum number of unit-capacity bins
needed to pack the multiset \(\{w(e):e\ni v\}\). The conjecture's parameter is
\(n=\max_v b(v)\).

Zero-weight edges may be deleted without changing feasibility. A final witness
must therefore use strictly positive rational weights. Isolated vertices may
also be deleted.

## Normalized formal statement

For every finite bipartite multigraph \(G=(L\dot\cup R,E)\), every weighting
\(w:E\to[0,1]\), and every positive integer \(n\), if each vertex's incident
weights can be partitioned into at most \(n\) subsets, each of total weight at
most one, then there exists a proper weighted edge-colouring
\(c:E\to\{0,\ldots,2n-2\}\).

The active finite frontier is \(n=3\).

## What an affirmative solution must establish

A complete affirmative solution of the full conjecture must construct or prove
the existence of such a \((2n-1)\)-colouring for every allowed finite
\((G,w,n)\). Proving only the \(n=3\) case is useful partial progress but does
not solve the full conjecture. The \(n=2\) case is already known.

## What a negative solution must exhibit

A complete counterexample at \(n=3\) must provide:

1. an explicit finite bipartite multigraph, including each parallel edge as a
   separately identified edge;
2. a strictly positive rational weight in \((0,1]\) for every edge;
3. for every vertex, an explicit partition of its incident edges into three bins,
   each having total weight at most one;
4. evidence that at least one vertex cannot be packed into two bins, so the
   instance's parameter is exactly \(n=3\);
5. a proof that every map \(c:E\to\{0,1,2,3,4\}\) violates the unit-load condition
   for at least one vertex and colour.

Items 1--5 negate the universal statement exactly: local three-bin routing is
possible, while routing through \(2n-1=5\) shared middle switches is impossible.

## Edge cases and variant exclusions

- Equality with capacity one is feasible; overload means strictly greater than
  one.
- Colours are global. The three-bin packing used to establish \(b(v)\le3\) may be
  different at each vertex and is not itself a global colouring.
- Multiple flows between the same input/output pair are distinct parallel
  edges.
- The graph must be bipartite. The Petersen-graph obstruction in Feige--Singh
  is deliberately outside the conjecture.
- The target is Feige--Singh Conjecture 1.1. Their Conjecture 1.2 uses only a
  total-incident-weight parameter and is stronger. Refuting 1.2 alone does not
  automatically refute this contract.
- A fractional, split-flow, preemptive, or per-endpoint colouring is not a
  proper weighted edge-colouring.

## Results that do not count

- a graph requiring six colours when some vertex needs four local bins;
- a counterexample only to the total-weight strengthening;
- floating-point weights without exact rational reconstruction and slack;
- failure of a heuristic colouring algorithm;
- testing many colourings without exhaustive coverage;
- an SMT or SAT result without the instance, encoding specification, and a
  separately checkable certificate;
- a counterexample in a non-bipartite graph;
- a special-case proof at \(n=3\), presented as resolution of all \(n\).

## Verification plan

Correctness:

1. A small standard-library verifier parses the witness as integers/rationals,
   confirms bipartiteness, checks all three local bins, and exhaustively
   backtracks over all five-colour assignments using exact arithmetic.
2. An independently written SMT/SAT encoding checks the same witness from the
   mathematical specification, not by importing verifier 1.
3. For non-colourability, retain either a solver proof certificate or a compact
   exhaustive search certificate whose coverage checker is independent of the
   search code.
4. A hostile audit recomputes every vertex load and attempts to find a missed
   colouring, capacity equality, edge identity, or parallel-edge error.

Novelty:

1. Search exact and equivalent formulations in current primary literature,
   bibliographic databases, author pages, and code repositories.
2. Search the final weight multiset, graph topology, and obstruction mechanism,
   not just the conjecture's title.
3. Ask the conjecture's recent authors or an expert in weighted edge colouring
   to check both prior art and correctness before any public claim.

## Source-comparison audit

The normalized statement preserves the primary statement's universal instance,
weighted bipartite graph, unit-bin definition of \(n\), proper weighted
colouring, and \(2n-1\) bound.

Two clarifications were added, not altered:

- Feige--Singh state elsewhere that their results and conjectures make no
  distinction between bipartite graphs and bipartite multigraphs.
- "At most \(n\) bins locally" is the quantified form of
  \(n=\max_v b(v)\).

The active \(n=3\) restriction is a search specialization. A counterexample
there refutes the full universal statement; a proof there alone would not prove
the full statement.
