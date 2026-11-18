# Higher-order theory after the \(n=2\) pivot

## Scope correction

**Status: proved elsewhere; not a novelty claim here.**

The \(n=2\) case is not an open frontier. Ngo--Vu (2003) proved the relevant
three-colour statement, commonly written \(m(2,r)=3\). The active target in
this note is therefore:

> incident weights pack locally into three unit bins, while a global weighted
> edge-colouring is sought with five colours.

A negative result must require at least six colours. This note does not
re-prove or claim novelty for the \(n=2\) theorem. The earlier C4 lemma,
that a union of two star forests is 3-colourable, survives only as a model
for the pair-conflict analysis below.

Throughout, \(G=(L\mathbin{\dot\cup}R,E)\) is a finite bipartite multigraph,
\(w(e)\in(0,1]\), and every incident multiset has a packing into three unit
bins. A *heavy* edge has weight greater than \(1/2\).

## Route registry

| ID | Mechanism | Rigorous output | First unresolved target | Status |
|---|---|---|---|---|
| A | Pair-conflict hypergraph and core colouring | local two-centre lemma; global six-colour bound | representable 6-chromatic conflict graph, or a five-colour theorem | proved / blocked |
| B | \(3/5\)-heavy, \(2/5\)-light decomposition | exact marked-graph equivalence and two sufficient colouring lemmas | smallest unsatisfiable marked bipartite graph | proved / conjectured target |
| C | Minimal counterexample and charging | five-colour deletion saturation and density orientation | turn local density into a global contradiction or finite degree bound | proved / blocked |

The three routes are logically independent. Route A can yield a counterexample
using pair conflicts alone. Route B deliberately fixes the weights and removes
linear arithmetic. Route C applies to arbitrary real weights.

## A. Pair conflicts and higher-order hyperedges

Let \(C_w\) have vertex set \(E(G)\), with two original edges adjacent when
they share an endpoint and their weights sum to more than one. Every valid
weighted colouring is a proper colouring of \(C_w\), but the converse can
fail because three pairwise compatible weights may sum to more than one.

### A1. Every local pair-conflict graph has a vertex cover of size at most two

**Status: proved.**

Fix an original vertex \(v\). Every conflict contains a heavy edge, since two
weights at most \(1/2\) have sum at most one. There are at most three heavy
edges at \(v\), because distinct heavy edges require distinct local bins.

If there are at most two heavy edges, they cover every conflict. Otherwise
write the three heavy weights as

\[
 h_1\ge h_2\ge h_3>1/2.
\]

No light edge \(x\) can conflict with \(h_3\). If it did, it would also
conflict with \(h_1,h_2\), so it could share none of the three bins occupied
by the heavy edges. This contradicts the supplied three-bin packing.
Consequently \(\{h_1,h_2\}\) covers every conflict: it covers the heavy
triangle, and every heavy-light conflict not incident with \(h_1\) or \(h_2\)
would have to meet \(h_3\). \(\square\)

This is the \(n=3\) replacement for the local “star plus isolates” lemma at
\(n=2\). Each local conflict graph is in fact a threshold graph, but the
two-vertex-cover statement is the property used below.

### A2. Pair-conflict graphs are always 6-colourable

**Status: proved.**

More generally, suppose a graph \(H=F_1\cup F_2\), where each \(F_i\) is a
disjoint union of graphs having vertex cover at most two. Then
\(\chi(H)\le6\).

**Proof.** Repeatedly delete vertices of current degree at most four, and let
\(K\) be the induced subgraph left. In each nontrivial component of
\(F_i[K]\), choose a vertex cover of size at most two and label its members
centre 1 and centre 2; a one-element cover uses only label 1. A vertex outside
the chosen cover has \(F_i[K]\)-degree at most two.

If \(K\ne\varnothing\), then \(\delta(K)\ge5\). Hence every vertex of \(K\)
is a chosen centre on at least one side. Otherwise its two componentwise
degrees would sum to at most four.

For \(j\in\{1,2\}\), let \(A_j\) be the vertices labelled centre \(j\) only
in \(F_1[K]\), and let \(B_j\) be the vertices labelled centre \(j\) only in
\(F_2[K]\). Each \(A_j\) is independent: two such vertices cannot be the same
labelled cover member in one \(F_1[K]\)-component, distinct components do not
interact, and two non-cover vertices have no edge in \(F_2[K]\). The same
argument applies to each \(B_j\).

Let \(D\) contain the vertices chosen as centres on both sides. Within
\(F_i[K][D]\), a centre can be adjacent to at most the other chosen centre
of its component. Thus \(F_i[K][D]\) is a matching. The union of two
matchings is bipartite: its components are paths and even cycles. Two new
colours therefore colour \(D\). Together,

\[
 A_1,\ A_2,\ B_1,\ B_2,\ \text{and the two parts of }D
\]

give six colours for \(K\). Restore the deleted vertices in reverse order.
Each has at most four already coloured neighbours, so one of six colours is
available. \(\square\)

By A1, every \(n=3\) pair-conflict graph satisfies A2.

### A3. Exact pairwise obstruction target

**Status: conjectured construction target.**

A pairwise counterexample at \(n=3\) is obtained by finding a weighted
bipartite instance whose \(C_w\) is 6-chromatic. A2 shows that six is the
largest chromatic number this route can produce, so the target is exact.

The topology-first search object is:

1. a 6-critical graph \(H\);
2. two partitions of \(V(H)\), representing the original \(L\)- and
   \(R\)-endpoints of each edge-variable;
3. on every block, a threshold graph with clique number at most three and a
   vertex cover of size at most two;
4. the union of all block graphs is \(H\);
5. one shared rational weight \(x_p\in(0,1]\) per \(p\in V(H)\), satisfying
   \(x_p+x_q>1\) exactly for the desired conflicts inside every block;
6. an explicit three-bin packing of the weights in every block.

The two partitions reconstruct a bipartite multigraph: \(p\) becomes the
original edge joining its left block to its right block. Parallel edges are
allowed.

Before solving weights, the search should run the A2 proof as a rejection
test. If some legal choice of the two local covers makes the double-centre
set \(D\) independent, then the same proof uses only five colours and the
topology cannot be 6-chromatic.

**First central blocker in Route A.** It is unknown here whether the
six-colour bound in A2 improves to five for the representable threshold
subclass. Proving that would eliminate every pairwise counterexample, but
would still leave higher-order overloads.

### A4. Two tempting inferences fail

**“A pair-conflict-free colouring is weighted-valid.” Status: refuted.**

Three edges of weight \(2/5\) at one vertex may receive the same colour.
Every pair has sum \(4/5\), but the colour load is \(6/5\).

**“The C4 centre proof generalizes by making the double-centre class
independent.” Status: refuted as a proof mechanism.**

A local triangle of three heavy edges is allowed by three bins. Choosing two
vertices as its cover centres leaves an edge between those centres. Taking
the same triangle on both sides makes those two vertices double-centres, so
\(D\) is not independent. The graph itself is only a triangle and is easily
coloured; the example kills the inference, not the desired five-colour bound.

## B. The exact \(3/5,2/5\) marked-graph model

Fix weights

\[
 w(e)=
 \begin{cases}
 3/5,&e\in M,\\
 2/5,&e\notin M,
 \end{cases}
\]

where \(M\) is the marked heavy-edge set. Write \(h(v)\) and \(\ell(v)\) for
the heavy and light degrees.

### B1. Local feasibility and global colouring become integral constraints

**Status: proved.**

The incident weights at \(v\) pack into three bins whenever

\[
 h(v)\le3,\qquad \ell(v)\le6-h(v).
\tag{B.1}
\]

Indeed, pair each heavy edge with at most one light edge, then place the
remaining light edges two per unused bin or remaining slot. Conversely these
inequalities are necessary: each heavy needs its own bin, and a bin holds at
most two lights, or one heavy and one light.

A five-colour weighted edge-colouring is exactly a partition

\[
 E(G)=Q_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}Q_5
\tag{B.2}
\]

such that, for every \(i\),

\[
 \Delta(Q_i)\le2
 \quad\text{and}\quad
 M\cap Q_i\text{ is a matching}.
\tag{B.3}
\]

Necessity follows because three light edges weigh \(6/5\), two heavy edges
weigh \(6/5\), and any three incident edges have weight greater than one.
For sufficiency, a colour has at most two incident edges, and its only
possible pairs are light-light of weight \(4/5\) or heavy-light of weight
one. \(\square\)

Thus this entire weight family is an exact finite marked-edge partition
problem, with no numerical tolerance or strict-inequality ambiguity.

### B2. Separate edge-colourings give a strong sufficient condition

**Status: proved.**

If

\[
 \Delta(G[M])+\Delta(G-M)\le6,
\tag{B.4}
\]

then the marked instance has a valid five-colouring.

**Proof.** By König's line-colouring theorem, edge-colour the heavy subgraph
with \(p=\Delta(G[M])\) matching colours and the light subgraph with
\(q=\Delta(G-M)\) matching colours. If both subgraphs are nonempty, merge one
heavy matching colour with one light matching colour. At every vertex the
merged colour contains at most a heavy-light pair, of load one. This uses
\(p+q-1\le5\) colours. If one subgraph is empty, the nonempty graph has
maximum degree at most six. In the all-light case, a six-edge-colouring can
be reduced to five by merging any two matching colours; in the all-heavy
case local feasibility gives maximum degree at most three. \(\square\)

Therefore a marked counterexample must satisfy

\[
 \Delta(G[M])+\Delta(G-M)\ge7.
\tag{B.5}
\]

The maxima must occur at different vertices, since (B.1) gives
\(h(v)+\ell(v)\le6\) pointwise.

### B3. Saturated regular marked instances are colourable

**Status: proved.**

Suppose \(G\) is 6-regular and every vertex has the same heavy degree
\(r\in\{0,1,2,3\}\). Then the marked instance is five-colourable.

For \(1\le r\le3\), the heavy and light subgraphs are respectively
\(r\)-regular and \((6-r)\)-regular bipartite graphs. Factor each into perfect
matchings, then merge one heavy factor with one light factor. This uses
\(r+(6-r)-1=5\) valid colours. For \(r=0\), factor the all-light graph into
six matchings and merge any two.

This refutes the attractive claim that a 6-regular heavy-light mixture is
automatically a hard topology. Any saturated candidate must have nonconstant
heavy degree.

### B4. Uniform triple overloads do not suffice

**Status: proved.**

If every edge has one common weight \(q\in(1/3,1/2]\), local three-bin
packability implies \(\Delta(G)\le6\). A proper ordinary six-edge-colouring
exists. Merge two colour classes; their combined load at a vertex is at most
\(2q\le1\). The result is a weighted five-colouring.

Hence the smallest local triple obstruction, three equal \(2/5\) edges, must
be coupled to unequal weights or heavy edges before it can matter globally.

### B5. Smallest exact marked-topology target

**Status: conjectured construction target.**

Search connected bipartite marked multigraphs in increasing order of

\[
 (|E|,\ |L|+|R|,\ \text{number of parallel pairs})
\]

subject to:

1. (B.1) at every vertex;
2. some vertex has degree six, since \(\Delta(G)\le5\) has an ordinary
   five-edge-colouring;
3. (B.5);
4. nonconstant heavy degree if the graph is 6-regular;
5. no partition satisfying (B.2)--(B.3).

The smallest nontrivial topology class is
\(|L|=|R|=2\) with parallel edges allowed; a one-vertex side is a star and
its local three-bin packing itself gives a global three-colouring.

For exact SAT, use Boolean variables \(X_{e,i}\), \(i=1,\ldots,5\):

- exactly one \(X_{e,i}\) is true for each edge;
- for every vertex, colour, and triple of incident edges, forbid all three
  \(X_{e,i}\) simultaneously;
- for every vertex, colour, and pair of incident heavy edges, forbid both
  \(X_{e,i}\) simultaneously.

Unsatisfiability is exactly the failure of (B.2)--(B.3), not merely a
relaxation. A hand-checkable output consists of the marked edge list, the
three local bins at every vertex, and either an independently checkable
unsatisfiability certificate or a complete symmetry-reduced case split.

This is the primary concrete construction target delivered by this note. If
it is satisfiable for \(2\times2\), continue with \(2\times3\), \(3\times3\),
then simple graphs before expanding the weight alphabet.

**Small hostile test: tested negative, not proved.** An ephemeral exhaustive
enumeration represented a \(2\times2\) marked multigraph by the eight
heavy/light multiplicities in its four endpoint cells. After the exact local,
degree-six, (B.5), and connectedness filters, 3,512 labeled multiplicity
matrices remained. Exact backtracking found a five-colouring for every one.
The code and a coverage certificate were not retained, so this is search
guidance only. A reproducible solver should re-run \(2\times2\) before moving
to \(2\times3\).

## C. Minimal-counterexample and density route

Assume conditionally that a counterexample to five colours exists, and choose
one with the minimum number of positive-weight edges.

### C1. Five-colour deletion saturation

**Status: proved.**

Let \(e=uv\) have weight \(x\), and five-colour \(G-e\). For endpoint
\(z\in\{u,v\}\) and colour \(i\), let \(L_z(i)\) be the load of colour \(i\)
at \(z\). Every colour is blocked at at least one endpoint:

\[
 L_u(i)>1-x\quad\text{or}\quad L_v(i)>1-x.
\tag{C.1}
\]

Otherwise \(e\) could receive that colour. One endpoint blocks at least
three colours. At that endpoint \(z\),

\[
 s(z):=\sum_{f\ni z}w(f)>x+3(1-x)=3-2x.
\tag{C.2}
\]

Thus every edge of weight \(x\) touches a vertex with incident total in

\[
 (3-2x,3].
\tag{C.3}
\]

This is an exact pruning rule for arbitrary-weight searches.

### C2. Light-edge blocking signatures

**Status: proved.**

If one endpoint blocks \(r\) colours, then its remaining incident total is
strictly greater than \(r(1-x)\), but at most \(3-x\). Hence blocking \(r\)
colours there is impossible whenever

\[
 r(1-x)\ge3-x.
\tag{C.4}
\]

Consequently:

- if \(x\le1/2\), neither endpoint can block all five colours;
- if \(x\le1/3\), neither endpoint can block four or five colours.

For \(x\le1/3\), the two endpoint blocking sets cover five colours and each
has size at most three. Therefore both endpoints block at least two colours,
and at least one blocks three. Any deletion-colouring certificate that
violates this \(2+3\) coverage pattern rejects the candidate immediately.

### C3. Density orientation

**Status: proved.**

Define the local deficit \(d(v)=3-s(v)\ge0\). By C1, orient every edge
\(e=uv\) toward an endpoint \(z\) satisfying

\[
 d(z)<2w(e).
\tag{C.5}
\]

Thus a very light edge can only point into a nearly weight-saturated vertex.
Equivalently, no edge of weight at most \(d(v)/2\) may be oriented toward
\(v\).

This converts deletion saturation into a finite orientation constraint. It
does not yet yield a global contradiction: a dense vertex may receive many
tiny edges while remaining within three bins.

### C4. Topological necessities

**Status: proved.**

Every counterexample satisfies:

- it is connected after discarding irrelevant components;
- every proper edge deletion is five-colourable;
- \(\Delta(G)\ge6\), since a bipartite multigraph of maximum degree at most
  five has an ordinary five-edge-colouring;
- the heavy-edge subgraph has maximum degree at most three;
- every non-pendant bridge is excluded by colouring the two sides separately,
  permuting the five colour names to align the bridge colour, and gluing.

These are the \(n=3\) analogues of the elementary minimality reductions. They
do not eliminate pendant bridges or bound the maximum degree from above.

### C5. Two false discharging shortcuts

**“Local three-bin feasibility implies degree at most six.” Status:
refuted.**

A star with twelve incident edges of weight \(1/4\) packs four edges in each
of three bins. Local bin count controls weight, not combinatorial degree.
Therefore a discharging proof cannot silently reduce to 6-regular topology.

**“Minimality forces tight bins.” Status: refuted as a normalization.**

If a counterexample exists, there is a positive minimum overload margin over
the finitely many five-colour assignments. There is also a positive minimum
margin by which every two-bin partition fails at any fixed vertex that
actually needs three bins, since that vertex has only finitely many
partitions. Scale all weights slightly downward, close enough to preserve
both margins, then perturb to nearby rationals. This makes every chosen local
three-bin sum strict while preserving uncolourability and exact bin number.
Equality at capacity may be useful computationally, but it is not without
loss of generality.

### C6. First blocked lemma

**Status: blocked.**

The density orientation (C.5) becomes useful only with an additional
invariant limiting how many edges can point into a vertex as a function of
their weights. The naive indegree bound is false by the twelve-\(1/4\)-edge
star. A viable next lemma must charge *weight* rather than edge count and
must use both endpoints or the bipartite cycle structure; using only
\(s(v)\le3\) merely restates local feasibility.

## What survived hostile audit

1. Route A proves a six-colour ceiling for pair-conflict graphs, but not the
   required five-colour bound.
2. Route B gives an exact, arithmetic-free counterexample language. Any
   unsatisfiable marked graph satisfying (B.1) is an explicit rational
   \(n=3\) counterexample.
3. Route C forces every deleted edge to have a dense endpoint and sharply
   constrains the blocking pattern of weights at most \(1/3\).
4. Uniform \(2/5\) triple constraints and regular heavy-light mixtures are
   rigorously colourable, so an exact search should not waste time on them.

No full proof or counterexample is claimed. The next decisive artifact should
be an exact result for Target B5, followed independently by the representable
6-chromatic search in A3.
