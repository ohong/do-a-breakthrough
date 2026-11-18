# Minimal-counterexample reductions for the \(n=2\) frontier

Status labels in this note have the meanings fixed by the research playbook.
Throughout, a *valid instance* is a finite weighted bipartite multigraph for
which every vertex has a packing of its incident edges into two unit bins. A
*counterexample* is a valid instance with no proper weighted 3-edge-colouring.

## Choice of a minimal object

Fix a counterexample with the minimum number of positive-weight edges. Subject
to that, minimize the number of non-isolated vertices. Isolated vertices are
discarded. This is called an **edge-minimal counterexample** below.

The existence of this object is conditional on the existence of any
counterexample. None of the lemmas below asserts that a counterexample exists.

## Surviving reductions

### M1. One connected component suffices

**Status: proved.**

An edge-minimal counterexample is connected.

**Proof.** The local two-bin condition restricts independently to each
component. If every component had a weighted 3-edge-colouring, the component
colourings, using the same three colour names, would combine to colour the
whole graph. Hence some component is itself a counterexample. Minimality and
the absence of isolated vertices leave only that component. \(\square\)

### M2. Every proper edge deletion is colourable

**Status: proved.**

For every edge \(e\), the instance \(G-e\) has a weighted 3-edge-colouring.

**Proof.** Edge deletion preserves every supplied local two-bin packing. The
result has fewer positive-weight edges, so edge minimality applies. \(\square\)

### M3. Edge-deletion saturation

**Status: proved.**

Let \(e=uv\) have weight \(x>0\), and let \(c\) be any weighted
3-edge-colouring of \(G-e\). Write

\[
 L_z(i)=\sum_{\substack{f\ni z,\ f\ne e\\c(f)=i}}w(f)
 \qquad(z\in\{u,v\},\ i\in\{0,1,2\}).
\]

Then for every colour \(i\),

\[
 L_u(i)>1-x\quad\text{or}\quad L_v(i)>1-x.
\tag{M3.1}
\]

Consequently, at one endpoint \(z\in\{u,v\}\),

\[
 \sum_{f\ni z}w(f)>2-x.
\tag{M3.2}
\]

**Proof.** If (M3.1) failed for colour \(i\), assigning \(e\) colour \(i\)
would extend \(c\), contradicting that \(G\) is a counterexample. The three
colours are covered by the two endpoint blocking sets, so one endpoint blocks
at least two colours. The two corresponding loads have sum
strictly greater than \(2(1-x)\); adding \(x\) gives (M3.2). \(\square\)

**Search consequence.** Every edge of weight \(x\) must touch a vertex whose
total incident weight lies in the narrow interval

\[
 (2-x,2].
\]

In particular, very light edges must touch nearly weight-tight vertices. This
is an exact pruning rule, independent of topology.

### M4. A light edge cannot be blocked three times at one endpoint

**Status: proved.**

In the notation of M3, if \(x\le 1/2\), neither endpoint can have
\(L_z(i)>1-x\) for all three colours.

**Proof.** Three blocked colours would give

\[
 \sum_{f\ni z,\ f\ne e}w(f)>3(1-x).
\]

Local two-bin feasibility gives total incident weight at most \(2\), hence the
left side is at most \(2-x\). But \(3(1-x)\ge2-x\) exactly when
\(x\le1/2\), a contradiction to the strict inequality. \(\square\)

Thus every colouring of \(G-e\), for a light \(e\), has a genuinely
two-endpoint obstruction: no endpoint alone blocks all three colours.

### M5. The maximum degree is at least four

**Status: proved.**

Every counterexample has an original-graph vertex of degree at least \(4\),
counting parallel edges separately.

**Proof.** If \(\Delta(G)\le3\), König's line-colouring theorem gives a proper
ordinary 3-edge-colouring of the bipartite multigraph. Each vertex then has at
most one incident edge of each colour, and every edge weight is at most \(1\).
The same colouring is therefore a proper weighted colouring. \(\square\)

### M6. The heavy-edge subgraph has maximum degree two

**Status: proved.**

Call an edge *heavy* if \(w(e)>1/2\). At most two heavy edges are incident with
any vertex. Hence the heavy-edge subgraph is a disjoint union of paths and even
cycles (including two-edge cycles formed by parallel edges).

**Proof.** Two heavy edges cannot share one unit bin. A local packing into two
bins therefore contains at most two of them. The structural conclusion follows
from maximum degree two and bipartiteness. \(\square\)

### M7. Both heavy and light edges are necessary

**Status: proved, with one cited dependency.**

A counterexample must contain an edge of weight \(>1/2\) and an edge of weight
\(\le1/2\).

- If all edges are heavy, M6 gives \(\Delta(G)\le2\). König's theorem then
  gives an ordinary 2-edge-colouring, which is a weighted colouring.
- If all weights are at most \(1/2\), the Melen--Turner special case quoted by
  Feige--Singh proves the stronger total-weight version with \(2n-1=3\)
  colours. Local two-bin feasibility implies total incident weight at most
  \(2\), so that theorem applies.

The second bullet must be checked against the exact Melen--Turner statement in
any publication-quality proof; here it is used only as reported in the
source-checked Feige--Singh paper.

### M8. A non-pendant bridge is impossible

**Status: proved.**

Every bridge in an edge-minimal counterexample is pendant, i.e. one component
of \(G-e\) is an isolated vertex.

**Proof.** Let bridge \(e=uv\) separate two components that both contain an
edge. Form \(G_u\) from the \(u\)-side together with \(e\), replacing \(v\)'s
side by a new leaf endpoint; define \(G_v\) symmetrically. The original local
bin certificates restrict to both graphs. Each graph has fewer edges than
\(G\), so each has a weighted 3-edge-colouring. Permute the three colour names
in one colouring so that the two copies of \(e\) have the same colour. Gluing
the colourings along \(e\) gives a colouring of \(G\), a contradiction.
\(\square\)

This proof does **not** eliminate pendant bridges.

### M9. Safe parallel-edge merging criterion

**Status: proved.**

Let parallel edges \(e,f\) have \(w(e)+w(f)\le1\). Replace them by one edge
\(g\) of weight \(w(e)+w(f)\). If the merged instance still has a local
two-bin packing at both common endpoints, then an edge-minimal counterexample
cannot contain \(e,f\).

**Proof.** Any weighted 3-edge-colouring of the merged instance lifts by giving
\(e\) and \(f\) the colour of \(g\); all colour loads are unchanged. Thus
uncolourability of the original implies uncolourability of the merged valid
instance, contradicting edge minimality. \(\square\)

**Exact preprocessing test.** Try all four choices of a bin for \(g\) at its
two endpoints, with the other incident edges assigned as in any feasible
two-bin packing. Merge only when feasibility is certified at both endpoints.

### M10. Real counterexamples can be made rational and locally slack

**Status: proved.**

If any real-weight counterexample exists, one exists with strictly positive
rational weights, all displayed local bin sums strictly below \(1\), and at
least one vertex of total incident weight strictly above \(1\).

**Proof.** Fix local two-bin partitions. For each of the finitely many global
3-colour assignments \(c\), let

\[
 M_c=\max_{v,i}\sum_{\substack{e\ni v\\c(e)=i}}w(e)>1.
\]

The finite minimum \(\delta=\min_c(M_c-1)\) is positive. Scale every weight by
a common \(s<1\) sufficiently close to \(1\) that
\(s(1+\delta)>1\), and also so that a vertex that originally required two
bins still has total weight above \(1\). Every fixed local bin now has strict
slack, while every colouring still overloads some vertex-colour pair.

All relevant inequalities are now strict. A sufficiently small independent
perturbation of the finitely many weights preserves positivity, the chosen
local packings, exact \(n=2\), and all colouring obstructions. Rational points
are dense, so choose the perturbation rational. \(\square\)

This justifies rational-grid searches in principle. It does **not** give an
a-priori denominator bound.

## Failed or unsafe reductions

### F1. “Every pendant edge extends after colouring its deletion”

**Status: refuted as a proposed proof mechanism; the structural claim that
minimal counterexamples have minimum degree two remains conjectured.**

The averaging argument works automatically only for a pendant edge of weight
\(\le1/2\). For a heavy pendant edge \(e\) of weight \(0.6\), a valid star can
have remaining incident weights

\[
 0.41,\ 0.41,\ 0.18,\ 0.18,
\]

packed locally as \((0.6+0.18+0.18)\) and \((0.41+0.41)\). A colouring of the
deleted star with colour loads \(0.41,0.41,0.36\) blocks \(e\) in every
colour, even though a different colouring may extend. Hence an arbitrary
colouring supplied by M2 is insufficient.

**Central missing lemma.** Either prove that some colouring of the deleted
instance leaves capacity \(1-w(e)\) at the neighbour of every pendant edge,
or build a gadget that forces all three neighbour loads above that threshold.
This is the first central blocker in upgrading M8 to bridgelessness.

### F2. “Parallel edges of total weight at most one always merge”

**Status: refuted.**

At one endpoint, weights \(0.3,0.3,0.7,0.7\) can be packed as
\((0.3+0.7),(0.3+0.7)\). Merging the two \(0.3\) items produces
\(0.6,0.7,0.7\), which needs three bins. Parallelism at the other endpoint
does not repair this local failure. M9 therefore requires an explicit
post-merge packing certificate.

### F3. “Every vertex is weight-tight” or “every local bin is tight”

**Status: refuted as a normalization.**

M10 shows that, if a counterexample exists, it can be chosen with every
displayed local bin strictly below capacity. Minimality in edge count does not
force equality of weight inequalities. Weight-tight variants may still be
useful as boundary points of an optimization, but they are not without-loss
normal forms.

## Concrete checks requested from the computational route

1. Enforce connectedness and \(\Delta\ge4\).
2. Require at least one heavy and one light edge.
3. Enforce heavy degree at most two.
4. For every proposed witness edge \(e\), independently verify the M3
   deletion-saturation condition by enumerating colourings of \(G-e\).
5. Reject any non-pendant bridge before weight solving.
6. Run the safe merge test M9 on every parallel pair.
7. Prefer rational weights with strict local slack, but do not impose a small
   denominator as a theorem.

