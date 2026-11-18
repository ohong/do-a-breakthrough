# Conflict and threshold structure at the \(n=2\) frontier

This note separates pairwise conflicts from genuinely higher-order capacity
conflicts. It gives finite construction targets for the computational route.

## 1. The overload hypergraph

For a weighted instance \(G\), define a hypergraph \(\mathcal H_w\):

- its vertices are the original edges \(E(G)\);
- for each original vertex \(v\), include every inclusion-minimal set
  \(S\subseteq\delta_G(v)\) with \(\sum_{e\in S}w(e)>1\).

A weighted 3-edge-colouring of \(G\) is exactly a 3-colouring of
\(\mathcal H_w\) with no monochromatic hyperedge.

**Status: proved.** Every overloaded colour class contains an
inclusion-minimal overloaded subset, and every listed hyperedge is forbidden.

The local two-bin certificate is a 2-colouring of each *single-star*
subhypergraph \(\mathcal H_w[\delta(v)]\). The open difficulty is that these
local 2-colourings need not agree on an original edge's two endpoints.

## 2. Pairwise conflict graph

Define \(C_w\) on vertex set \(E(G)\) by

\[
 ef\in E(C_w)
 \quad\Longleftrightarrow\quad
 e,f\text{ share an endpoint and }w(e)+w(f)>1.
\]

Every weighted colouring is a proper vertex-colouring of \(C_w\).
The converse holds exactly when every set of pairwise compatible edges at
each original vertex has total weight at most \(1\).

### C1. Each local pair-conflict graph is a star plus isolates

**Status: proved.**

At a fixed original vertex \(v\), the graph
\(C_w[\delta(v)]\) is a threshold graph and is bipartite because the supplied
two-bin packing properly 2-colours it. A bipartite threshold graph is a star
plus isolated vertices.

**Direct proof of the last sentence.** Sort incident weights
\(a_1\ge a_2\ge\cdots\). Neighbourhoods are nested: if \(a_i\ge a_j\), every
neighbour of \(j\), other than \(i\) itself, is a neighbour of \(i\). More
directly, the weight-threshold definition forbids an induced \(P_4\):
if \(p-q-r-s\) were induced, then
\(x_p+x_q>1\) and \(x_r+x_s>1\), whereas
\(x_p+x_r\le1\) and \(x_q+x_s\le1\); summing the first pair and the second
pair gives a contradiction. The identical four-inequality argument forbids
an induced \(C_4\). A connected bipartite graph that is not a star contains
an induced \(P_4\) or \(C_4\): a shortest path of length at least three gives
the former, while diameter at most two forces a complete bipartite graph,
which gives the latter when both sides have size at least two. Therefore
every nontrivial connected component is a star. Two
nontrivial components would supply an induced \(2K_2\), also impossible:
for edges \(pq,rs\) and cross-nonedges \(pr,qs\), summing their four
threshold inequalities gives the same contradiction. Hence there is at most
one star component, with all remaining vertices isolated.

Equivalently, each original vertex designates at most one local conflict
centre; every pairwise conflict there joins that centre to one of its leaves.

### C2. The global pair-conflict graph is triangle-free

**Status: proved.**

Three vertices of a line graph are pairwise adjacent only when the three
original edges share one endpoint, or when the original graph contains a
triangle. The latter is impossible in a bipartite multigraph (parallel edges
do not create a third case). In the former case, three pairwise weight
conflicts cannot fit into two local bins. Therefore \(C_w\) has no triangle.

### C3. Two-star-forest representation

**Status: proved.**

Partition the original vertices into \(L\) and \(R\). The conflicts generated
at vertices of \(L\) form a star forest \(F_L\); those generated at vertices of
\(R\) form a star forest \(F_R\). Hence

\[
 C_w=F_L\cup F_R.
\tag{C3.1}
\]

Each conflict-graph vertex (an original edge) belongs to at most one component
of each star forest.

This is substantially stronger than merely being triangle-free or having
arboricity at most two.

## 3. Pairwise-only obstructions are impossible

### C4. A union of two star forests is 3-colourable

**Status: proved.**

Let \(H=F_1\cup F_2\), where \(F_1,F_2\) are star forests. The two forests
need not be edge-disjoint. Then \(\chi(H)\le3\).

**Proof.** Iteratively delete vertices of current degree at most two. Let
\(K\) be the induced subgraph left when this process stops. Each restricted
graph \(F_i[K]\) remains a star forest. In every nontrivial component of
\(F_i[K]\), designate one centre. The choice is forced for a star with at
least two leaves; for a \(K_2\) component choose either endpoint. Do not
designate a centre in an isolated-vertex component. Thus every edge of
\(F_i[K]\) has a designated centre as an endpoint, and every vertex not
designated in \(F_i[K]\) has \(F_i[K]\)-degree at most one.

If \(K\) is nonempty, it has minimum degree at least three. Hence every
vertex of \(K\) is a designated centre in at least one restricted forest:
otherwise

\[
 \deg_K(v)\le \deg_{F_1[K]}(v)+\deg_{F_2[K]}(v)\le2.
\]

Partition \(V(K)\) into

\[
\begin{aligned}
A&=\{\text{centres only in }F_1[K]\},\\
B&=\{\text{centres only in }F_2[K]\},\\
D&=\{\text{centres in both restricted forests}\}.
\end{aligned}
\]

Each set is independent in \(H[K]\). For \(A\), an \(F_1[K]\)-edge cannot
join two designated \(F_1[K]\)-centres, since exactly one centre was chosen
per nontrivial component. An \(F_2[K]\)-edge cannot join two vertices that
are both non-centres, since every such edge has its chosen centre as an
endpoint. The argument for \(B\) is symmetric. An edge joining two vertices
of \(D\) would belong to at least one \(F_i[K]\), but would then join two
chosen centres of that forest, again impossible. Thus \(A,B,D\) give a
3-colouring of \(K\).

Finally restore the deleted vertices in reverse order. Each has at most two
already coloured neighbours, so one of the three colours remains available.
This extends the colouring from \(K\) to \(H\). If \(K\) was empty, the same
reverse greedy argument colours all of \(H\). \(\square\)

The proof covers all degeneracies:

- restricting a larger star may create a \(K_2\), where choosing exactly one
  endpoint as centre preserves the argument;
- isolated vertices of a restricted forest are non-centres of degree zero;
- an edge present in both forests only lowers
  \(\deg_{F_1[K]}(v)+\deg_{F_2[K]}(v)\) relative to the union degree and does
  not affect any independence argument.

**Computational hostile check.** An independent ephemeral enumeration of all
labeled simple graphs through six vertices generated every star forest and
every distinct union of two of them, then tested exact 3-colourability. It
found no counterexample:

| vertices | star forests | distinct unions | non-3-colourable |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |
| 3 | 7 | 8 | 0 |
| 4 | 26 | 63 | 0 |
| 5 | 111 | 793 | 0 |
| 6 | 562 | 14,824 | 0 |

This computation is only a hostile sanity check; C4 rests on the proof.

### Consequence for the weighted problem

By C3 and C4, every pair-conflict graph \(C_w\) is 3-colourable. Therefore
no counterexample can be certified solely by pairwise overloads. In any
uncolourable weighted instance, every 3-colouring that avoids pair conflicts
must still create a monochromatic minimal overloaded set of size at least
three at some original vertex.

This does **not** prove the weighted conjecture. A proper 3-colouring of
\(C_w\) controls only pairs; three pairwise compatible edges can still have
total weight greater than one. The former Target P and its threshold-weight
system are retired.

As a consistency check, the earlier exhaustive test that the Grötzsch graph
\(M(C_5)\) has no edge decomposition into two star forests is now explained
by C4: that graph is 4-chromatic.

## 4. Higher-order conflicts are a separate route

Pairwise compatibility does not imply capacity compatibility. For example,
three edges of weight \(2/5\) are pairwise compatible but have total
\(6/5>1\). A counterexample may therefore have a 3-colourable pair-conflict
graph and still fail through monochromatic triples or larger sets.

The smallest useful local mixed pattern is

\[
 \{3/5,2/5,2/5,2/5\}.
\tag{T.1}
\]

It has the local packing

\[
 (3/5+2/5)\ \mid\ (2/5+2/5),
\]

but its capacity constraints say:

- a colour containing the \(3/5\) edge contains at most one \(2/5\) edge;
- no colour contains all three \(2/5\) edges.

### Refuted overly symmetric family

**Status: refuted.**

Take a 4-regular bipartite graph, choose a perfect matching of \(3/5\)-edges,
and give every other edge weight \(2/5\). The three light edges at every
vertex form a 3-regular bipartite graph and hence have a perfect matching
\(N\). Colour the heavy matching together with \(N\) using colour 0, and
2-edge-colour the remaining even-cycle light subgraph using colours 1 and 2.
All loads are at most one. Thus this natural regular construction cannot be a
counterexample.

An ephemeral exact backtracking check also coloured the cyclic versions on
4 through 8 vertices per side; the theorem above explains those outcomes.

### Target T: Hall-deficient mixed gadget

**Status: conjectured construction target.**

Use only weights \(3/5\) and \(2/5\). Let \(D\) be the endpoints incident
with exactly one heavy edge and three light edges. Let vertices outside \(D\)
have only light edges, with degree at most four. Require:

1. the heavy subgraph is a matching;
2. the light bipartite graph has no matching saturating \(D\);
3. every vertex has one of the locally valid multisets
   \[
   \{3/5,(2/5)^j\},\quad 0\le j\le3,
   \qquad\text{or}\qquad
   \{(2/5)^j\},\quad 0\le j\le4;
   \]
4. the complete weighted instance is not 3-colourable.

Condition 2 destroys the uniform two-colour mechanism used above. It does not
by itself prove condition 4, so this is a falsifiable topology generator, not
a claimed obstruction.

**Concrete inequality-free search order.**

- Choose \(|L|,|R|\in\{4,5,6\}\).
- Enumerate a matching \(M\) of heavy edges.
- Enumerate a connected light graph with the degree caps in item 3.
- Reject if a light matching saturates \(D\).
- Run exact weighted 3-colourability.
- Only after a topology survives, replace \(3/5,2/5\) by variables
  \(h_e,\ell_e\) and optimize rational slack.

### Target V: variable degree-four stars

**Status: conjectured construction target.**

For a fixed connected bipartite topology of minimum relevant degree four,
assign every degree-four star a designated heavy edge \(h_v\) and three light
edges \(a_v,b_v,c_v\). Solve

\[
\begin{aligned}
&1/2<h_v<1,\qquad 0<a_v,b_v,c_v\le1/2,\\
&h_v+a_v\le1,\\
&b_v+c_v\le1,\\
&a_v+b_v+c_v>1,
\end{aligned}
\tag{V.1}
\]

allowing permutation of which light edge is packed with \(h_v\) independently
at each endpoint. The last inequality forces a genuine triple conflict.
For every one of the \(3^{|E|}\) global colourings, add a disjunction selecting
one vertex-colour load \(>1\). Search first over topology, then solve this
finite strict rational system with a common slack variable.

Target V directly tests whether triple overloads can defeat all three colours
even when pairwise conflicts do not.

## 5. Surviving blocker and next falsifiable claims

Blocked lemma P0 is closed by C4. The first remaining construction blocker is
now genuinely higher-order:

> **Blocked target H0.** Can minimal overloaded triples, coupled through the
> two endpoints of each original edge, force a fourth colour even though the
> pair-conflict graph is 3-colourable?

Targets T and V make H0 finite and falsifiable without pretending that it is
already a lemma. The next two computational claims are:

1. **T-search claim:** every Hall-deficient \(3/5,2/5\) instance under the
   stated degree caps and with at most six vertices per side is
   3-colourable, or else output the first exact witness.
2. **V-search claim:** for successively larger degree-four bipartite
   topologies, the strict rational system (V.1) plus the complete
   colouring-obstruction disjunctions is infeasible, or else output exact
   rational weights and independently verify every colouring.

Neither finite nonexistence result would prove the full conjecture, but each
cleanly retires or advances a higher-order construction mechanism.
