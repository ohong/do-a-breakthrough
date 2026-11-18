# Closing the representable pair-conflict route

## Main theorem

### Pair-conflict graphs need at most \(n+1\) colours

**Status: proved.**

Let \(G\) be a finite bipartite multigraph with edge weights in \((0,1]\).
Suppose the incident weights at every original vertex pack into \(n\) unit
bins. Form the pair-conflict graph \(C_w\):

- \(V(C_w)=E(G)\);
- two vertices of \(C_w\) are adjacent exactly when the corresponding
  original edges share an endpoint and their weights sum to more than one.

Then

\[
 \chi(C_w)\le n+1.
\tag{1}
\]

In particular, for the active \(n=3\) case,

\[
 \chi(C_w)\le4.
\tag{2}
\]

**Proof.** Split the original edges into

\[
 E_H=\{e:w(e)>1/2\},
 \qquad
 E_L=\{e:w(e)\le1/2\}.
\]

Two heavy edges cannot occupy one unit bin. Hence the heavy-edge subgraph
\(G_H=(L\mathbin{\dot\cup}R,E_H)\) has maximum degree at most \(n\).
König's line-colouring theorem for bipartite multigraphs gives a proper
ordinary edge-colouring

\[
 c_H:E_H\to\{1,\ldots,n\}.
\]

Use these same colours on the corresponding heavy vertices of \(C_w\), and
give every light vertex of \(C_w\) the single new colour \(n+1\).

This is proper:

1. two conflicting heavy edges share an original endpoint, so their
   \(c_H\)-colours differ;
2. a heavy-light conflict has colours from disjoint palettes;
3. two light edges never conflict, because their sum is at most one.

Thus (1) holds. \(\square\)

The proof uses the weights shared across the two endpoint partitions in the
strongest possible way: “heavy” is a global property of an original edge,
not a separately chosen local centre label.

## Consequence for A3

**Status: proved.**

There is no 5-chromatic or 6-chromatic representable pair-conflict graph at
\(n=3\). The former A3 search for a representable 6-critical graph is empty
and should be retired.

Pair conflicts alone therefore cannot obstruct a weighted five-colouring.
Indeed, they cannot obstruct even four colours. Any failure of five weighted
colours must be caused by a monochromatic overloaded set of at least three
pairwise compatible edges.

This does **not** prove the arbitrary-weight \(n=3\) conjecture. A proper
colouring of \(C_w\) controls only pairs. For example, three edges of weight
\(2/5\) are pairwise nonconflicting but have total weight \(6/5\).

## Audit of the double-centre absorption route

The previous six-colour proof discarded the global heavy/light dichotomy. It
treated each endpoint block only as an abstract graph with a two-vertex
cover, peeled degree-four vertices, and partitioned the remaining core into

\[
 A_1,A_2,B_1,B_2,D_0,D_1.
\]

Here \(D_0,D_1\) are the two parts of a double-centre graph that is a union
of two matchings.

### Tempting fixed-partition claim

> One of \(D_0,D_1\) can always be merged into one of the four one-sided
> centre classes without recolouring the other classes.

**Status: unsupported and unnecessary.**

The abstract centre proof supplies no missing adjacency: a double-centre
vertex may have conflict neighbours among one-sided centres and among local
non-centres whose other endpoint makes them one-sided centres. The fact that
\(D_0,D_1\) are independent internally says nothing about their complete
adjacency to \(A_1,A_2,B_1,B_2\). The earlier local heavy triangle already
shows that the whole double-centre set \(D\) need not be independent.

No fixed-class absorption lemma is needed. The theorem performs a global
repartition:

\[
\underbrace{M_1,M_2,M_3}_{\text{heavy-edge matchings}}
\quad\dot\cup\quad
\underbrace{E_L}_{\text{all light edges}}.
\tag{3}
\]

Every natural local cover centre is heavy, but (3) also handles heavy
non-centres. It ignores whether an edge was labelled \(A\), \(B\), or \(D\)
and recolours the original heavy subgraph directly.

Thus the double-centre issue was an artifact of forgetting which vertices
of \(C_w\) came from weights greater than \(1/2\).

## Hostile checks

### Weight exactly \(1/2\)

**Status: checked.**

Such an edge is light. Two weight-\(1/2\) edges sum to exactly one, which is
feasible and does not create a conflict because adjacency requires a sum
strictly greater than one.

### Three heavy edges at one endpoint

**Status: checked.**

They occupy three separate local bins and form a triangle in \(C_w\).
König's colouring assigns them three distinct colours. No fourth heavy edge
can occur at that endpoint.

### Parallel edges

**Status: checked.**

Parallel heavy edges are adjacent in the original multigraph and receive
distinct ordinary edge colours. Parallel light edges remain mutually
nonconflicting. A heavy-light parallel pair uses disjoint palettes.

### Many light edges

**Status: checked.**

There is no combinatorial degree bound on light edges, but none is needed.
All light vertices of \(C_w\) form an independent set, even when many share
one original endpoint.

### Pair-conflict colouring implies weighted colouring

**Status: refuted.**

The three \(2/5\)-edges example shows the implication fails. The theorem
closes only the pairwise obstruction route and makes no arbitrary-weight
five-colour claim.

## Search consequence

Do not enumerate 5-critical or 6-critical candidate pair-conflict graphs.
For every proposed weighted topology, the colouring in the theorem is an
explicit four-colour certificate for its pair constraints.

Future exact searches must encode minimal overloaded triples and larger
sets. A pairwise-only SAT or chromatic-number objective cannot find a
counterexample to the \(n=3\), five-colour statement.

No novelty claim is made for (1) without a separate literature check; the
argument is elementary and is used here solely to close this research route.
