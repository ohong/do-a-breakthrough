# Structural route: cuts, total-arc slack, metric duality, and parity

Status: **blocked, with proved partial lemmas and one refuted induction
mechanism**.

This note concerns the bidirected cube
\(\overleftrightarrow{Q_d}=(V_d,A_d)\), where
\(V_d=\{0,1\}^d\) and

\[
A_d=\{(x,x\oplus e_i):x\in V_d,\ 1\leq i\leq d\}.
\]

Write \(N=2^d\), \(M=|A_d|=dN\), \(h(x,y)\) for Hamming
distance, and \(\bar x=x\oplus(1,\ldots,1)\). Fixed points of a
permutation use empty paths. All paths below may share vertices but not
directed arcs.

## Summary of outcomes

1. **Proved:** every ordinary directed cut condition is automatic for a
   permutation request. For a fixed vertex set \(S\), the exact largest
   possible demand from \(S\) to \(S^c\), over all permutations, is
   \(\min(|S|,|S^c|)\), while the cube has at least that many arcs in
   each direction across the cut.
2. **Proved:** if
   \[
   \Delta(\sigma)=d2^d-\sum_xh(x,\sigma(x))
   \]
   is the total-arc slack, then every routing satisfies the exact
   conservation law
   \[
   \text{unused arcs}+\text{total detour excess}=\Delta(\sigma).
   \]
   The unused arcs form a balanced directed graph.
3. **Proved:** all permutations with
   \(\Delta\in\{0,2,4\}\) are classified, and every one has an explicit
   arc-disjoint **shortest-path** routing. Hence a low-slack
   counterexample cannot occur before \(\Delta=6\).
4. **Proved:** the weighted directed-metric inequalities are exactly the
   dual conditions for a **fractional** multiflow. A rational violation
   has a compact vertex-potential certificate and would be a full
   obstruction to integral routing. No such cube-permutation
   certificate was obtained.
5. **Blocked:** proving all weighted metric inequalities for every cube
   permutation is the same as proving universal fractional
   routability. Even that would not prove integral arc-disjoint routing;
   the needed rounding statement is theorem-strength.
6. **Proved but nonseparating:** aggregate arc usage and its complement
   obey Eulerian and mod-2 cycle-space constraints. These reject some
   proposed arc sets, but no condition depending only on \(\sigma\)
   stronger than the metric dual was extracted.
7. **Refuted as a method:** the natural Beneš-style split produces an
   exact 2-SAT condition, but it is not universally satisfiable. It
   already fails for a permutation of \(Q_2\) that is nevertheless
   routed by two obvious shortest paths.

No claim in this note satisfies the full solution contract.

## 1. Exact directed cut bounds

For \(S\subseteq V_d\), define

\[
k_\sigma(S)=|\{x\in S:\sigma(x)\notin S\}|
\]

and let \(b(S)\) be the number of undirected cube edges with one end in
\(S\) and the other in \(S^c\). There are exactly \(b(S)\) directed arcs
from \(S\) to \(S^c\), and exactly \(b(S)\) in the reverse direction.

### Claim C1 (proved): exact permutation demand across a fixed cut

For every permutation \(\sigma\),

\[
k_\sigma(S)=k_\sigma(S^c)\leq \min(|S|,|S^c|).
\]

Moreover, for each fixed \(S\),

\[
\max_{\sigma\in\operatorname{Sym}(V_d)} k_\sigma(S)
   =\min(|S|,|S^c|).
\]

#### Proof

Let \(i\) be the number of sources in \(S\) whose targets also lie in
\(S\). Then \(k_\sigma(S)=|S|-i\). Since exactly \(|S|\) targets lie in
\(S\), exactly \(|S|-i\) sources in \(S^c\) must target \(S\). This is
\(k_\sigma(S^c)\). The common value is at most both side sizes.

Assume first that \(|S|\leq |S^c|\). Choose \(|S|\) distinct vertices
of \(S^c\), pair them bijectively with \(S\), transpose each paired
pair, and fix the remaining vertices. Every source in \(S\) then
leaves \(S\), so \(k_\sigma(S)=|S|\). The case
\(|S|>|S^c|\) follows by interchanging \(S\) and \(S^c\). ∎

### Claim C2 (proved): expansion one, including equality

For every \(S\subseteq V_d\),

\[
b(S)\geq \min(|S|,|S^c|).
\]

If \(S\) is nonempty and proper, equality holds if and only if \(S\)
or \(S^c\) is a coordinate halfcube

\[
\{x\in V_d:x_i=\varepsilon\}
\]

for some coordinate \(i\) and bit \(\varepsilon\).

#### Proof

The inequality and its equality case are proved together by induction
on \(d\). The assertion is immediate for \(d=1\). By replacing \(S\)
with \(S^c\), assume \(0<|S|\leq 2^{d-1}\).

Split \(Q_d\) on its last coordinate and identify each half with
\(Q_{d-1}\). Let \(S_0,S_1\subseteq V_{d-1}\) be the two sections,
with sizes \(a\geq b\). The boundary decomposes exactly as

\[
b_d(S)=b_{d-1}(S_0)+b_{d-1}(S_1)+|S_0\mathbin{\triangle}S_1|.
\tag{1}
\]

If \(a\leq 2^{d-2}\), induction and
\(|S_0\triangle S_1|\geq a-b\) give

\[
b_d(S)\geq a+b+(a-b)=2a\geq a+b=|S|.
\]

Equality throughout requires \(a=b\), \(S_0=S_1\), and equality for
both sections. Since a nonempty equality section in \(Q_{d-1}\) has
size \(2^{d-2}\) by induction, \(S_0=S_1\) is a coordinate halfcube
in \(Q_{d-1}\). Thus \(S\) is a coordinate halfcube in \(Q_d\).

If \(a>2^{d-2}\), apply induction to \(S_0^c\) and to \(S_1\):

\[
b_d(S)\geq (2^{d-1}-a)+b+(a-b)=2^{d-1}\geq a+b.
\]

For equality with \(a+b\), one must have \(a+b=2^{d-1}\). If
\(b>0\), equality for \(S_1\) would force \(b=2^{d-2}\), contradicting
\(a>2^{d-2}\). Hence \(b=0\), \(a=2^{d-1}\), and \(S\) is exactly one
of the two halfcubes in the chosen split. Coordinate halfcubes plainly
attain equality, completing the induction. ∎

### Corollary C3 (proved): all ordinary directed cuts pass

Every permutation request satisfies

\[
k_\sigma(S)\leq b(S)=|\delta^+(S)|
\]

for every \(S\). A nontrivial cut is saturated only when \(S\) is a
coordinate halfcube and \(\sigma\) maps all of \(S\) to \(S^c\) (and,
necessarily, all of \(S^c\) to \(S\)).

Thus cube isoperimetry settles **all ordinary vertex-set cut
conditions**, but nothing about multicommodity integrality. The first
unsupported affirmative step would be:

> Every cube permutation satisfying these cuts has an integral
> arc-disjoint path packing.

Because every cube permutation satisfies the cuts, that statement is
just the conjecture in cut-sufficiency language. This route is
**theorem-strength blocked**.

## 2. Total-arc slack and the Eulerian complement

Define

\[
D(\sigma)=\sum_{x\in V_d}h(x,\sigma(x)),\qquad
\Delta(\sigma)=M-D(\sigma),
\]

and define the permutation

\[
\tau(x)=\overline{\sigma(x)}.
\]

### Claim S1 (proved): slack identities

For every permutation \(\sigma\),

\[
\Delta(\sigma)=\sum_xh(x,\tau(x)).
\tag{2}
\]

If \((P_x)\) is an arc-disjoint routing, define

\[
E=\sum_x\bigl(|P_x|-h(x,\sigma(x))\bigr)
\]

and let \(U\) be the number of directed cube arcs unused by every path.
Then

\[
U+E=\Delta(\sigma).
\tag{3}
\]

Both \(E\) and \(\Delta(\sigma)\) are even.

#### Proof

For every \(x,y\in V_d\),

\[
h(x,y)+h(x,\bar y)=d.
\]

Summing with \(y=\sigma(x)\) proves (2).

Arc-disjointness gives
\(\sum_x|P_x|=M-U\). Since
\(\sum_x|P_x|=D(\sigma)+E\), rearrangement proves (3).

Every cube arc changes Hamming-weight parity. Consequently every
\(x\)-to-\(\sigma(x)\) path has length congruent to
\(h(x,\sigma(x))\) modulo \(2\), so every summand in \(E\) is even.
For each coordinate, the number of \(0\)-to-\(1\) moves under a
permutation equals the number of \(1\)-to-\(0\) moves. Hence
\(D(\sigma)\), and therefore \(\Delta(\sigma)=d2^d-D(\sigma)\), is
even for \(d\geq1\). ∎

### Claim S2 (proved): unused arcs are Eulerian

In every routing, the directed graph of used arcs is balanced at every
vertex:

\[
\deg^+_{\rm used}(v)=\deg^-_{\rm used}(v).
\tag{4}
\]

The unused directed arcs are balanced as well and decompose into
directed cycles. In particular:

- \(U\) is even;
- if \(U=2\), the two unused arcs are the opposite orientations of
  one cube edge;
- if \(U=4\), the unused arcs decompose into two directed digons or one
  directed \(4\)-cycle.

#### Proof

The incidence vector of a directed path has divergence \(+1\) at its
source, \(-1\) at its target, and \(0\) elsewhere. Summing all path
incidences gives divergence zero, because every vertex occurs once as
a source and once as a target. This remains true for fixed points with
empty paths. Hence (4) holds.

The full bidirected cube has indegree and outdegree \(d\) at every
vertex, so subtracting the used arcs shows that the unused arcs are
balanced. Every finite balanced digraph decomposes into directed
cycles. A directed cycle in the bidirected cube has even length:
length \(2\) is a digon, while every longer cycle projects to a cycle
in the bipartite undirected cube. The conclusions for \(U=2,4\)
follow. ∎

There is also a mod-\(2\) version. For each undirected cube edge \(e\),
mark \(e\) when exactly one of its two orientations is used. At every
vertex an even number of marked edges is incident, because
\(\deg^+_{\rm used}+\deg^-_{\rm used}=2\deg^+_{\rm used}\) modulo
\(2\). Thus the marked edges form an even subgraph, i.e. an element of
the undirected cycle space. This is a real restriction on a proposed
arc set, but so far it supplies no obstruction depending only on
\(\sigma\).

### Claim S3 (proved): equality and very-low-slack classification

The equality \(D(\sigma)=M\), equivalently \(\Delta=0\), holds if and
only if

\[
\sigma(x)=\bar x\quad\text{for every }x.
\]

For \(\Delta=2\), \(\tau\) is exactly a transposition of two adjacent
vertices.

For \(\Delta=4\), \(\tau\) has exactly one of the following forms:

1. a transposition of two vertices at Hamming distance \(2\);
2. two disjoint transpositions, each of an adjacent pair;
3. a \(3\)-cycle whose three vertices form a length-\(2\) cube path;
4. a cyclic orientation of a square face of the cube.

These alternatives are exhaustive and disjoint by cycle type.

#### Proof

Equation (2) says that \(\Delta\) is the total Hamming displacement of
the permutation \(\tau\).

Total displacement zero forces every point to be fixed, so
\(\tau=\mathrm{id}\) and \(\sigma(x)=\bar x\).

If the total displacement is \(2\), every moved point contributes at
least \(1\). A nonidentity permutation moves at least two points, so
there are exactly two, they are transposed, and their distance is
\(1\).

Suppose the total displacement is \(4\), and let \(m\) be the support
size of \(\tau\). Then \(2\leq m\leq4\).

- If \(m=2\), the unique transposition contributes twice the distance
  of its two points, so that distance is \(2\).
- If \(m=3\), the support is a \(3\)-cycle. The three successive
  distances are positive integers with even sum \(4\), so they are
  \(1,1,2\); the three vertices form a length-\(2\) path.
- If \(m=4\) and the cycle type is \(2+2\), each of the four moved
  points must contribute \(1\), so both transpositions are cube edges.
- If \(m=4\) and the cycle type is \(4\), all four successive
  distances are \(1\). Four distinct vertices connected cyclically by
  cube edges form a square face.

No other support size or cycle type is possible. ∎

### Claim S4 (proved): every permutation with \(\Delta\leq4\) is
shortest-path routable

For every \(\sigma\) with
\(\Delta(\sigma)\in\{0,2,4\}\), there is a family of pairwise
arc-disjoint paths \(P_x:x\to\sigma(x)\) such that

\[
|P_x|=h(x,\sigma(x))\quad\text{for every }x.
\]

#### Standard antipodal decomposition

Fix an ordering \(\pi=(i_1,\ldots,i_d)\) of the coordinates. For each
source \(x\), let \(R_x^\pi\) flip the coordinates in that order. The
endpoint is \(\bar x\). At the step that flips \(i_j\), the tail is

\[
x\oplus e_{i_1}\oplus\cdots\oplus e_{i_{j-1}}.
\]

As \(x\) ranges over \(V_d\), these tails range bijectively over
\(V_d\). Thus the paths \(R_x^\pi\) use every directed arc exactly
once.

#### A splice operation

Suppose \(\tau\) transposes \(a,b\), and the coordinates on which
\(a,b\) differ form a consecutive block in \(\pi\). Replace
\(R_a^\pi,R_b^\pi\) as follows. Each new path follows its own prefix
before the block, omits the whole block, and follows the other path's
suffix after the block. At the splice point the two relevant vertices
agree, because \(a\) and \(b\) differ exactly on the omitted block.
The two new paths end at \(\bar b,\bar a\), respectively, flip every
coordinate outside the block exactly once, and use only disjoint arcs
from the original antipodal decomposition.

For one transposition this proves the \(\Delta=2\) case (a
one-coordinate block) and case S3.1 (a two-coordinate block, made
consecutive). For two disjoint adjacent transpositions, apply the
one-coordinate splice independently to the two disjoint pairs. A
single coordinate is a consecutive block in every order.

It remains to handle the \(3\)- and \(4\)-cycles.

#### The \(3\)-cycle

Label the cycle \(a\mapsto b\mapsto c\mapsto a\), where

\[
b=a\oplus e_p,\qquad c=b\oplus e_q,\qquad p\neq q.
\]

Order all other coordinates first, then \(p,q\). Let \(R_x^0\) be the
prefix that flips all coordinates other than \(p,q\), and write \(x^*\)
for its endpoint. Use

\[
\begin{aligned}
P_a&=R_a^0+(a^*,a^*\oplus e_q),\\
P_b&=R_b^0+(b^*,b^*\oplus e_p),\\
P_c&=R_c^0.
\end{aligned}
\]

These endpoints are, respectively, \(\bar b,\bar c,\bar a\). The two
added arcs are precisely the two successive \(p,q\) arcs originally
belonging to \(R_b^\pi\), while the \(p,q\) arcs of
\(R_a^\pi,R_c^\pi\) are discarded. Hence no arc is repeated. Every
displayed path flips exactly the coordinates on which its endpoints
differ.

#### The \(4\)-cycle

Label the oriented square

\[
a\mapsto b\mapsto c\mapsto r\mapsto a
\]

with

\[
b=a\oplus e_p,\quad
c=b\oplus e_q,\quad
r=c\oplus e_p=a\oplus e_q.
\]

Again order all other coordinates first, then \(p,q\), and use

\[
\begin{aligned}
P_a&=R_a^0+(a^*,a^*\oplus e_q),&
P_b&=R_b^0+(b^*,b^*\oplus e_p),\\
P_c&=R_c^0+(c^*,c^*\oplus e_q),&
P_r&=R_r^0+(r^*,r^*\oplus e_p).
\end{aligned}
\]

The two arcs used by \(P_a,P_b\) are the \(p,q\) block originally
belonging to \(R_b^\pi\); the two used by \(P_c,P_r\) are the block
originally belonging to \(R_r^\pi\). The endpoints are
\(\bar b,\bar c,\bar r,\bar a\). Arc-disjointness and shortestness
follow exactly as in the \(3\)-cycle case.

All sources fixed by \(\tau\) retain their full antipodal paths.
Together with Claim S3, these constructions prove the claim. ∎

### Consequence for a counterexample search

Let

\[
E_{\min}(\sigma)=
\min_{\text{arc-disjoint routings}}\;
\sum_x(|P_x|-h(x,\sigma(x))),
\]

with \(E_{\min}=+\infty\) if no routing exists. Equation (3) implies
that any routing must have \(E_{\min}\leq\Delta\). Merely proving that
no shortest routing exists establishes only \(E_{\min}\geq2\), not
\(E_{\min}>\Delta\).

Claim S4 shows more: every permutation with \(\Delta\leq4\) actually
has \(E_{\min}=0\). Therefore a counterexample based on a
shortest-path obstruction plus insufficient total-arc slack must have
\(\Delta\geq6\) and must prove the genuinely stronger statement

\[
E_{\min}(\sigma)>\Delta(\sigma).
\]

The earliest unsupported step in this route is any inference from
“shortest routing is impossible” to such a lower bound on total
detour. Without a new invariant, proving that bound is simply proving
unrestricted infeasibility for the candidate. This route is
**blocked after the complete \(\Delta\leq4\) classification**.

## 3. Weighted directed metrics and fractional multiflow

Let \(\ell:A_d\to\mathbb{R}_{\geq0}\) be arbitrary directed arc
lengths. Let

\[
d_\ell(u,v)=\min_{P:u\leadsto v}\sum_{a\in P}\ell(a)
\]

be directed shortest-path distance.

### Claim M1 (proved): metric inequality

Every integral arc-disjoint routing satisfies

\[
\sum_{x\in V_d}d_\ell(x,\sigma(x))
\leq \sum_{a\in A_d}\ell(a)
\quad\text{for every }\ell\geq0.
\tag{5}
\]

#### Proof

For each routed path,
\(d_\ell(x,\sigma(x))\leq\sum_{a\in P_x}\ell(a)\). Summing and using
each directed arc at most once proves (5). ∎

This is stronger in principle than checking only ordinary cuts.
For example, assigning length \(1\) to every arc leaving a set \(S\)
shows at least the ordinary inequality
\(k_\sigma(S)\leq|\delta^+(S)|\), because every commodity leaving
\(S\) has weighted distance at least \(1\).

The distinction is genuine on general networks. Consider the
bidirected \(K_{2,3}\), with bipartition
\(\{s,t\}\cup\{a,b,c\}\), unit arc capacities, and demands in both
directions on the four undirected pairs

\[
st,\quad ab,\quad bc,\quad ca.
\]

Every directed cut passes. Indeed, if a cut contains \(h\) of
\(\{s,t\}\) and \(l\) of \(\{a,b,c\}\), its outgoing supply capacity
and outgoing demand are

\[
3h+2l-2hl,\qquad
\mathbf 1_{\{h=1\}}+l(3-l),
\]

respectively; checking \(h=0,1,2\) and \(l=0,1,2,3\) gives demand at
most capacity. But with unit arc lengths, the total arc length is
\(12\), while the eight directed demands each have distance \(2\),
for total \(16\). Thus the metric inequality detects fractional
infeasibility that all cuts miss. This example is **not** a cube and
**not** a permutation request; it proves only that the dual family is
not cut bookkeeping in disguise.

### Claim M2 (proved): exact fractional interpretation

For a fixed cube permutation \(\sigma\), all inequalities (5) hold if
and only if there is a fractional path routing in which every
commodity sends one unit and every directed arc has total load at most
one.

#### Proof

For each commodity \(x\), let \(\mathcal P_x\) be the finite set of
simple \(x\)-to-\(\sigma(x)\) paths. A fractional routing chooses
numbers \(f_{x,P}\geq0\) satisfying

\[
\sum_{P\in\mathcal P_x}f_{x,P}=1,\qquad
\sum_{x}\sum_{\substack{P\in\mathcal P_x\\a\in P}}f_{x,P}\leq1.
\tag{6}
\]

Necessity follows from the proof of Claim M1, after weighting and
summing the fractional path loads.

For sufficiency, consider the compact convex set of all arc-load
vectors obtained by independently choosing, for each commodity, a
probability distribution on \(\mathcal P_x\). If this set does not
meet the coordinatewise capacity box \([0,1]^{A_d}\), finite
linear-programming separation gives a nonnegative vector
\(\ell\) for which the minimum weighted load of the path-choice set
exceeds \(\sum_a\ell(a)\). The minimum separates by commodity and is
exactly

\[
\sum_x\min_{P\in\mathcal P_x}\sum_{a\in P}\ell(a)
=\sum_xd_\ell(x,\sigma(x)).
\]

This violates (5). Conversely, a violation separates the two sets.
Thus (5) is equivalent to (6). ∎

For completeness, the separating vector may be taken nonnegative:
replace any separator by its coordinatewise positive part. Loads are
nonnegative, so this cannot decrease its value on a load vector, while
its maximum on the capacity box is exactly the sum of its coordinates.

The qualifier **fractional** is essential. A proof of (5) for every
cube permutation would still leave an integrality problem. Assuming

> every feasible fractional cube-permutation multiflow of congestion
> one can be rounded to arc-disjoint paths of congestion one

would, together with universal fractional feasibility, prove the
conjecture. No such rounding lemma is established here, and it may
not be assumed.

### Claim M3 (proved): exact certificate and separation LP

A weighted-metric violation for a fixed permutation can be searched
for and certified by a polynomial-size rational linear program, with
no path enumeration.

Normalize \(\sum_a\ell(a)=1\). For each commodity \(x\), introduce
vertex potentials \(p_x(v)\) and impose

\[
\ell(a)\geq0,\qquad p_x(x)=0,\qquad
p_x(v)-p_x(u)\leq\ell(u,v)
\quad\text{for every arc }(u,v).
\tag{7}
\]

Maximize

\[
\sum_x p_x(\sigma(x)).
\tag{8}
\]

For fixed \(\ell\), the maximum possible
\(p_x(\sigma(x))\) is exactly
\(d_\ell(x,\sigma(x))\): summing (7) along a path gives the upper
bound, and \(p_x(v)=d_\ell(x,v)\) attains it. Therefore an optimum
strictly greater than \(1\) is exactly a violation of (5).

After scaling rational values to integers, a checkable negative
certificate consists of:

1. the permutation table \(\sigma\);
2. nonnegative integer arc lengths \(\ell(a)\);
3. integer potentials \(p_x(v)\) satisfying (7);
4. the strict arithmetic inequality
   \[
   \sum_x\bigl(p_x(\sigma(x))-p_x(x)\bigr)
   >\sum_a\ell(a).
   \]

Each potential inequality is local to one directed arc. Such a
certificate proves **fractional** infeasibility and therefore also
integral infeasibility. Conversely, an exact LP optimum at most \(1\)
proves fractional feasibility for that one permutation, not an
integral routing.

### Claim M4 (proved): coordinate-homogeneous directed lengths pass

Suppose the length of an arc in coordinate \(i\) is \(\alpha_i\) in
the \(0\)-to-\(1\) direction and \(\beta_i\) in the \(1\)-to-\(0\)
direction, independent of the other coordinates. Then (5) holds for
every permutation.

#### Proof

For coordinate \(i\), let \(r_i\) be the number of sources with bit
\(0\) whose target has bit \(1\). Since \(\sigma\) preserves the
number of zero and one bits in the target column, the number moving
from \(1\) to \(0\) is also \(r_i\). Nonnegative coordinate-homogeneous
lengths make a path that flips each differing coordinate once
shortest, so

\[
\sum_xd_\ell(x,\sigma(x))
=\sum_i r_i(\alpha_i+\beta_i).
\]

Since \(r_i\leq N/2\), this is at most

\[
\sum_i\frac N2(\alpha_i+\beta_i)
=\sum_{a\in A_d}\ell(a).
\]

This includes the unweighted slack inequality as a special case. ∎

The earliest unsupported step in the metric route is extending Claim
M4 from coordinate-homogeneous lengths to arbitrary
location-dependent directed lengths. By Claim M2, that extension is
exactly universal fractional routability. It is weaker than the
original conjecture, but it is not proved here. The finite LP in Claim
M3 is the surviving counterexample mechanism.

## 4. Beneš-style split and its exact 2-SAT obstruction

This section tests a natural induction that uses the same coordinate
once near each endpoint, as a cube analogue of a Beneš network.

Fix a split coordinate and write each physical vertex as \((s,z)\),
where \(s\in\{0,1\}\) is its side and \(z\in V_{d-1}\). Make a
bipartite multigraph \(H_\sigma\):

- a left vertex \(I_z\) for each input pair
  \(\{(0,z),(1,z)\}\);
- a right vertex \(O_z\) for each output pair
  \(\{(0,z),(1,z)\}\);
- one edge for every commodity
  \((s,z)\mapsto(t,w)\), joining \(I_z\) to \(O_w\), and retaining
  its source-side label \(s\) and target-side label \(t\).

Every vertex of \(H_\sigma\) has degree \(2\), so every component is an
even cycle, with a pair of parallel edges allowed as a length-\(2\)
cycle.

### Claim B1 (proved): safe split choices are exactly a 2-SAT instance

Alternately color the edges of every component \(0,1\). Color \(c\)
means that the commodity is assigned to middle subcube \(c\). This
gives one commodity of each color at every input and output pair, so
each middle subcube receives a permutation request.

At a physical pair \(z\), define:

- \(I_z^{\rm swap}=1\) if the source on side \(0\) is colored \(1\)
  (equivalently, the source on side \(1\) is colored \(0\)); then both
  orientations of the physical split edge are used at the first
  stage;
- \(O_z^{\rm swap}=1\) if the commodity targeting side \(0\) is
  colored \(1\) (equivalently, the commodity targeting side \(1\) is
  colored \(0\)); then both orientations are used at the last stage.

The first and last stages avoid directed-arc reuse exactly when

\[
\neg(I_z^{\rm swap}\wedge O_z^{\rm swap})
\quad\text{for every }z.
\tag{9}
\]

Fix one alternating base coloring \(b_e\) on each cycle \(C\), and let
\(X_C\) record whether that cycle's colors are flipped. If \(e_z^I\)
is the edge sourced on side \(0\) at \(I_z\), and \(e_z^O\) is the edge
targeting side \(0\) at \(O_z\), then

\[
I_z^{\rm swap}=b_{e_z^I}\oplus X_{C(e_z^I)},\qquad
O_z^{\rm swap}=b_{e_z^O}\oplus X_{C(e_z^O)}.
\]

Consequently (9) is one 2-CNF clause in the two indicated cycle-flip
variables (or a unary clause when they are the same variable).
Satisfiability is therefore necessary and sufficient for making this
restricted first/middle/last split safe at its physical cross arcs.
Recursive routing inside the middle subcubes remains a separate
obligation.

### Claim B2 (refuted): the 2-SAT condition is not universally
satisfiable

The smallest failure is \(d=2\). Number vertices by their two-bit
strings and take

\[
\sigma(00)=00,\quad
\sigma(01)=10,\quad
\sigma(10)=01,\quad
\sigma(11)=11.
\tag{10}
\]

Split on the second bit. The input pairs are
\(\{00,01\}\), \(\{10,11\}\), and the output pairs are the same. The
four commodity edges form one \(4\)-cycle:

\[
I_0\!-\!(00\to00)\!-\!O_0\!-\!(10\to01)\!-\!I_1
\!-\!(11\to11)\!-\!O_1\!-\!(01\to10)\!-\!I_0.
\]

In one alternating coloring, pair \(0\) is unswapped at both stages
and pair \(1\) is swapped at both stages. Flipping the only cycle
reverses the roles: pair \(0\) is swapped at both stages and pair \(1\)
is unswapped. Thus one clause is violated in either coloring. The
permutation (10) is invariant under exchanging its two coordinates,
so the other possible split fails identically.

This is only a counterexample to the restricted architecture.
Unrestricted routing is immediate:

\[
01\to00\to10,\qquad
10\to11\to01,
\]

with empty paths at \(00,11\). These two paths are shortest and share
no directed arc. In fact (10) has \(\Delta=4\) and is covered by Claim
S4.

For \(d=1\), both permutations satisfy the split condition, so
\(d=2\) is minimal. The proposed universal Beneš/2-SAT induction is
therefore **refuted**, not merely unproved.

## 5. Small and degenerate checks

All proved claims above have dimension-free proofs. The following
finite checks were also performed to catch convention, parity, and
classification errors.

For every permutation and every vertex subset in \(d=1,2,3\), direct
enumeration computed \(k_\sigma(S)\), \(b(S)\), \(\Delta(\sigma)\), and
the cycle type of \(\tau=\bar{\phantom{x}}\circ\sigma\). The results
were:

| \(d\) | permutations | subsets | cut violations | \(\#\Delta=0\) | \(\#\Delta=2\) | \(\#\Delta=4\) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 0 | 1 | 1 | 0 |
| 2 | 24 | 16 | 0 | 1 | 4 | 14 |
| 3 | 40,320 | 256 | 0 | 1 | 12 | 114 |

The explicit constructions in Claim S4 were separately instantiated
for every permutation in those three low-slack columns. This checked
2 cases in \(d=1\), 19 in \(d=2\), and 127 in \(d=3\). For every
constructed family, a second pass verified each source, endpoint,
shortest length, and directed-arc key; it found no repeated directed
arc.

The low-slack counts also follow independently from Claim S3. If
\(E_d=d2^{d-1}\) is the number of cube edges, then:

- \(\Delta=2\): \(E_d\) adjacent transpositions;
- \(\Delta=4\), distance-\(2\) transposition:
  \(2^{d-1}\binom d2\);
- \(\Delta=4\), two disjoint edge transpositions:
  \(\binom{E_d}{2}-2^d\binom d2\);
- \(\Delta=4\), oriented \(3\)-cycle on a length-\(2\) path:
  \(2^{d+1}\binom d2\);
- \(\Delta=4\), oriented square:
  \(2^{d-1}\binom d2\).

Their total is
\(\binom{E_d}{2}+2^{d+1}\binom d2\), giving \(14\) and \(114\) for
\(d=2,3\).

An independent enumeration of the Beneš 2-SAT condition found no
failure for \(d=1\), two failures for either fixed split in \(d=2\),
and 11,700 failures among the 40,320 permutations for a fixed split in
\(d=3\). These counts are evidence about the restricted architecture
only; Claim B2 already gives a hand-checkable minimal refutation.

Boundary and convention checks:

- \(d=1\): the antipodal permutation uses the two opposite directed
  arcs and has \(\Delta=0\); the identity uses two empty paths and has
  \(\Delta=2\).
- \(d=2\): (10) explicitly checks fixed points, empty paths,
  \(\Delta=4\), and the distinction between opposite directed arcs and
  a repeated directed arc.
- \(d=3\): exhaustive enumeration found no odd slack, no cut
  violation, and no exception to either low-slack classification.
- Identity in any dimension has \(D=0\), maximal slack \(d2^d\), and
  is routed by empty paths.
- The antipodal permutation in any dimension has zero slack and is
  routed by the standard antipodal decomposition using every directed
  arc once.
- Outside the sourced contract, \(d=0\) has one fixed vertex, no arcs,
  and all displayed identities read \(0=0\).

## 6. Earliest unsupported steps and route disposition

1. **Cuts:** ordinary cuts are universally satisfied. Assuming their
   integral sufficiency is exactly assuming the conjecture. **Blocked.**
2. **Slack:** shortest-path infeasibility yields only two units of
   required detour. A counterexample needs a proof that every routing
   requires more detour than \(\Delta\). No such lower bound is known
   here, and all \(\Delta\leq4\) cases are shortest-routable.
   **Blocked below slack \(6\); certificate target made precise.**
3. **Metric dual:** arbitrary directed metric separation is an exact,
   checkable counterexample mechanism. Universal validity is equivalent
   to universal fractional routability, which is unproved. Fractional
   validity would still need theorem-strength integral rounding.
   **Blocked as a proof route; live as an exact LP counterexample
   route.**
4. **Eulerian/parity:** the unused arcs must be a directed cycle union,
   and singly used underlying edges lie in the cycle space. No
   \(\sigma\)-only separation stronger than the metric LP was derived.
   **Necessary filter only.**
5. **Beneš split:** the exact cycle-flip 2-SAT condition fails already
   in \(Q_2\). **Restricted mechanism refuted.**

The strongest surviving artifact is therefore the combination of:

- exact automatic cut bounds;
- the conservation law \(U+E=\Delta\);
- the complete shortest-routing theorem for \(\Delta\leq4\); and
- the potential-based LP certificate for a genuinely stronger
  weighted-metric obstruction.
