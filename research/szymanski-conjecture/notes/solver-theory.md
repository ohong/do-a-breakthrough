# Solver-theory report

Date: 2026-07-23

## Scope and outcome

This report concerns only the canonical conjecture from `contract.md`:
for every \(d\geq 1\) and every permutation \(\sigma\) of
\(V_d=\{0,1\}^d\), route every request \(x\to \sigma(x)\) by pairwise
arc-disjoint directed paths in the bidirected cube.

No proof or counterexample to that conjecture is claimed here. No novelty
claim has been checked. The strongest artifacts obtained in this run are:

1. a proved sufficient induction criterion;
2. a proved \(Q_3\) counterexample to a broad one-crossing version of that
   criterion, including an explicit routing showing that the conjecture itself
   is not being refuted;
3. a proved \(Q_3\) counterexample to the stronger Beneš-style cycle-flip
   \(2\)-SAT induction lemma;
4. an exact closed-trail formulation of permutation-cycle routing and several
   constructive subclasses, including every single cycle of length at most
   \(d+1\);
5. a self-contained proof that every permutation demand satisfies every
   directed cut condition, with a classification of all tight cuts.

Vertices of \(Q_3\) are sometimes written as the integers \(0,\ldots,7\), with
the usual three-bit binary representations. Coordinate \(i\) means the bit of
value \(2^i\). For a vertex \(x\), write \(x^i=x\oplus e_i\).

## Approach-family registry

| ID | Family | Mechanism | First falsifiable target | Quick test | Concrete artifact obtained | Theorem-strength blocker |
|---|---|---|---|---|---|---|
| A | Flexible induction | Cut on a chosen coordinate; use adaptive portals or a Beneš-style alternating lane assignment; invoke the \((d-1)\)-dimensional statement on induced permutations | Some coordinate has either a one-cross partial-permutation portal assignment or a satisfiable cycle-flip \(2\)-SAT lane assignment | Derive the exact local constraints, then test a derangement with no adjacent request | Portal induction and counting lemmas, plus one \(Q_3\) permutation with hand-checkable obstructions to both restricted embeddings | A universal multi-crossing decomposition without a strictly simpler routable request class would merely restate the original routing problem |
| B | Cycle/Cayley decomposition | Replace each permutation cycle by an ordered directed closed trail; use cube translations, coordinate blocks, fans, and supporting paths | Every single permutation cycle has an ordered closed trail, followed by an arc-disjoint packing theorem for distinct cycles | Prove the hub-fan construction through length \(d+1\); test whether routable factors compose in \(Q_1\) | Exact trail equivalence, fan routing, translation routing, direct-product lemma, and path-order criterion | Packing arbitrary ordered trails is equivalent to the original conjecture unless an independently checkable structural restriction is found |
| C | Cut/potential and Eulerian flow | Prove all demand cuts, classify equality, then seek cube-specific integral multiflow or splitting-off | The cut condition is sufficient for permutation demands in a bidirected cube | Inspect all nontrivial equality cases and the global down-arc saturation used by the known \(2\)-to-\(1\) obstruction | Boundary theorem, automatic cut condition, tight-cut classification, and saturation rigidity | Cut sufficiency is false for general multiflows; a cube-specific proof for exactly these demands would be essentially the conjecture |

## A. Flexible induction

### A1. Portal induction criterion

**Claim A1, `proved`.** Fix a coordinate \(i\), splitting \(Q_d\) into
halves \(H_0,H_1\). Suppose every request crossing the cut is assigned a
directed cut arc

\[
p\longrightarrow p^i
\]

in its source-to-target direction, with no directed cut arc assigned twice.
Split such a request \(x\to y\) into

\[
x\longrightarrow p,\qquad p\longrightarrow p^i,\qquad
p^i\longrightarrow y.
\]

Keep an internal request as \(x\to y\). Delete all length-zero subrequests.
If, in each half, the remaining subrequests have pairwise distinct sources and
pairwise distinct targets, then the truth of Szymanski's conjecture in
dimension \(d-1\) implies that \(\sigma\) is routable in \(Q_d\).

**Proof.** A request set with distinct sources and distinct targets is a
partial permutation. Match its unused sources bijectively to its unused
targets to extend it to a permutation of the half. Apply the
\((d-1)\)-dimensional conjecture and discard the paths belonging to added
pairs. Do this independently in both halves. The resulting half-cube paths
are mutually arc-disjoint within each half. They use no coordinate-\(i\)
arc, while the assigned cut arcs are distinct by hypothesis. Concatenating
the two half-cube pieces with the cut arc therefore routes every original
request, with no directed arc repeated. \(\square\)

This is a genuine induction step, but its portal hypothesis still has to be
established. The next two claims show that the natural one-crossing version is
false.

### A2. Counting rigidity for one-crossing portal schemes

Call a crossing request **source-crossed** (\(F\)) when its portal is its
source, so its first half-cube segment is empty. Call it
**target-crossed** (\(L\)) when its portal is the neighbor of its target, so
its second half-cube segment is empty.

**Claim A2, `proved`.** Let \(\sigma\) be a derangement, and fix a coordinate
cut such that no crossing request has adjacent endpoints. If a one-crossing
portal assignment makes the nonempty half-cube subrequests partial
permutations, then every crossing request is either \(F\) or \(L\). In
particular, allowing arbitrary portals gives no more freedom than choosing
one endpoint of every crossing request.

**Proof.** Each half has \(N=2^{d-1}\) vertices. Let \(m\) requests leave
one half. Because \(\sigma\) is a permutation, exactly \(m\) requests enter
it. Its \(N-m\) internal requests are all nonempty because \(\sigma\) is a
derangement.

Let \(a\) be the number of outgoing requests whose first half-cube segment is
empty, and let \(b\) be the number of incoming requests whose second
half-cube segment is empty. The number of nonempty subrequests in this half is

\[
(N-m)+(m-a)+(m-b)=N+m-a-b.
\]

A partial permutation on \(N\) vertices has at most \(N\) requests, so
\(a+b\geq m\). Apply the same argument in the other half. There are \(2m\)
crossing requests in total, while the two inequalities require at least
\(2m\) empty endpoint segments. A crossing request with nonadjacent
endpoints cannot have both half-cube segments empty, so it contributes at
most one. Equality follows throughout, and every crossing request has
exactly one empty endpoint segment. \(\square\)

### A3. A routable \(Q_3\) permutation that defeats every such cut

Define

\[
\begin{array}{c|rrrrrrrr}
x&0&1&2&3&4&5&6&7\\ \hline
\sigma(x)&3&4&7&0&2&6&5&1.
\end{array}
\]

Its cycle form is

\[
(0\ 3)(1\ 4\ 2\ 7)(5\ 6).
\]

Every request has Hamming distance \(2\). Hence \(\sigma\) is a derangement,
and no request crossing any coordinate cut has adjacent endpoints. By Claim
A2, an arbitrary one-crossing portal scheme satisfying Claim A1 would reduce
to \(F/L\) choices.

For an \(F\) choice on \(x\to y\), the nonempty subrequest is
\(x^i\to y\). For an \(L\) choice, it is \(x\to y^i\). The following
conflicts prove that no coordinate works.

**Coordinate \(i=0\).**

1. The internal request \(7\to1\) rules out \(3\to0\) being \(L\), since
   that would add \(3\to1\) with the same target. Thus request \(3\) is
   \(F\).
2. The internal request \(4\to2\) rules out \(5\to6\) being \(F\), since
   that would add \(4\to6\) with the same source. Thus request \(5\) is
   \(L\).
3. If request \(2\to7\) were \(L\), it would add \(2\to6\), while request
   \(3\) being \(F\) adds \(2\to0\). Thus request \(2\) is \(F\).
4. Request \(2\) being \(F\) adds \(3\to7\), while request \(5\) being
   \(L\) adds \(5\to7\). Their targets collide.

**Coordinate \(i=1\).**

1. The internal request \(1\to4\) rules out \(3\to0\) being \(F\), since
   that would add \(1\to0\). Thus request \(3\) is \(L\).
2. The internal request \(2\to7\) rules out \(6\to5\) being \(L\), since
   that would add \(6\to7\). Thus request \(6\) is \(F\).
3. Request \(3\) being \(L\) adds \(3\to2\), so \(4\to2\) cannot be \(F\),
   which would add \(6\to2\). Thus request \(4\) is \(L\).
4. Request \(4\) being \(L\) adds \(4\to0\), while request \(6\) being
   \(F\) adds \(4\to5\). Their sources collide.

**Coordinate \(i=2\).**

1. If \(7\to1\) is \(F\), it adds \(3\to1\), whose source collides with
   the internal request \(3\to0\).
2. If \(7\to1\) is \(L\), it adds \(7\to5\), whose target collides with
   the internal request \(6\to5\).

Both choices are impossible.

Therefore:

**Claim A3, `refuted`.** It is false that every permutation admits some
coordinate cut and a one-crossing portal assignment whose induced nonempty
requests are partial permutations.

This does **not** refute Szymanski's conjecture. The same permutation has the
following explicit routing:

\[
\begin{array}{c|l}
0\to3&0,1,3\\
1\to4&1,0,4\\
2\to7&2,3,7\\
3\to0&3,2,0\\
4\to2&4,6,2\\
5\to6&5,7,6\\
6\to5&6,7,5\\
7\to1&7,3,1.
\end{array}
\]

The sixteen directed arcs displayed here are pairwise distinct. Opposite
orientations of the same undirected edge occur, which is permitted by the
contract.

Explicitly, the arc set is

\[
\begin{split}
\{&(0,1),(1,3),(1,0),(0,4),(2,3),(3,7),(3,2),(2,0),\\
  &(4,6),(6,2),(5,7),(7,6),(6,7),(7,5),(7,3),(3,1)\}.
\end{split}
\]

It has cardinality \(16\), and the path table shows directly that each path
starts at \(x\) and ends at the displayed \(\sigma(x)\).

### A4. Beneš-style alternating lanes also fail on the same permutation

There is a stronger and very natural induction attempt. Pair inputs and
outputs across coordinate \(i\), and delete that bit to label each pair by a
physical index \(z\in Q_{d-1}\). Make a bipartite multigraph whose left
vertices are input pairs, whose right vertices are output pairs, and whose
edge for source \(s\) joins the pair of \(s\) to the pair of \(\sigma(s)\).
Every graph vertex has degree two.

Alternately color the edges of each cycle by lanes \(0,1\). Each lane then
has one commodity at every input pair and every output pair, so it induces a
permutation of \(Q_{d-1}\). At input index \(z\), let \(A_z=1\) when the
lane assignment swaps the two source sides. At output index \(z\), let
\(B_z=1\) when the lane assignment swaps the two target sides. An input swap
uses both directed coordinate-\(i\) arcs at physical index \(z\), and so
does an output swap. Therefore the cut arcs are conflict-free exactly when

\[
\neg(A_z\wedge B_z)\qquad\text{for every }z.
\]

Each connected cycle has two alternating colorings. Flipping one cycle
complements all of its incident lane colors, so these conditions form a
\(2\)-SAT instance on one flip variable per cycle. If it is satisfiable, the
two lane permutations can be routed inductively and concatenated with their
input/output cut arcs.

**Claim A4, `refuted`.** The cycle-flip \(2\)-SAT instance need not be
satisfiable for any coordinate, even for a routable derangement in \(Q_3\).

**Certificate.** Use the permutation from Claim A3 and color the commodity
edges indexed by sources \(0,\ldots,7\) with

\[
c=(0,1,1,0,1,0,0,1).
\]

For each coordinate, the table lists the quotient edge \(q_i(s)q_i(\sigma(s))\)
for \(s=0,\ldots,7\), the source-edge indices on side \(0\), and the
preimage-edge indices of the side-\(0\) targets.

\[
\begin{array}{c|l|l|l}
i&\text{quotient edges}&\text{side-0 sources}&
  \text{preimages of side-0 targets}\\ \hline
0&01,02,13,10,21,23,32,30&0,2,4,6&3,4,1,5\\
1&01,12,03,10,20,32,23,31&0,1,4,5&3,7,1,6\\
2&03,10,23,30,02,12,21,31&0,1,2,3&3,7,4,0
\end{array}
\]

In every row, the quotient multigraph is connected and the displayed
coloring is alternating at every input and output vertex. Thus it is a
single cycle and has only this coloring and its complement. Reading \(c\)
on either of the last two columns gives

\[
(A_0,A_1,A_2,A_3)=(B_0,B_1,B_2,B_3)=(0,1,1,0).
\]

This coloring conflicts at physical indices \(1,2\). Flipping the unique
cycle makes both vectors \((1,0,0,1)\), which conflicts at indices \(0,3\).
Hence the \(2\)-SAT instance is unsatisfiable for all three coordinates.

The fixed-point convention is not responsible: this permutation is a
derangement. Allowing partial lane assignments by omitting empty commodities
can repair some smaller examples, but Claim A3 shows that the one-crossing
partial-permutation version also fails on this same instance. The explicit
paths in Claim A3 again show that only the restricted embedding has failed.

### A5. First unresolved induction step

**A-U1, `unsupported`.** Some adaptive cut with multiple crossings should
still yield strictly simpler lower-dimensional requests.

Nothing above proves this. The first falsifiable repair target is to classify
the minimum source/target defect forced by a cut decomposition and test the
following strictly weaker auxiliary lemma:

> Every partial permutation of \(Q_n\) with one additional duplicated source
> or one additional duplicated target is routable.

This is deliberately narrower than arbitrary \(2\)-to-\(1\) routing, which is
known to fail. A tempting strengthening with one prescribed arc forbidden is
already false in \(Q_1\): the requests \(0\to0,0\to1\) force the arc
\(0\to1\). Even if the stated auxiliary lemma is true, a separate
decomposition lemma must bound the number and interaction of defects.
Requiring arbitrary multi-crossing pieces themselves to be routable would be
a theorem-strength restatement, not progress.

## B. Cycle and Cayley structure

### B1. Exact ordered-closed-trail formulation

A directed trail may repeat vertices but not directed arcs.

**Claim B1, `proved`.** A permutation \(\sigma\) is routable if and only if,
for every nontrivial cycle

\[
C=(x_1\,x_2\,\ldots\,x_k)
\]

of \(\sigma\), there is a directed closed trail \(W_C\) with marked
occurrences of \(x_1,x_2,\ldots,x_k\) in this cyclic order, and the trails
for distinct cycles are pairwise arc-disjoint.

**Proof.** Given a routing, concatenate the path \(x_j\to x_{j+1}\) around
each permutation cycle. Arc-disjointness makes the concatenation a closed
trail, and trails for distinct cycles share no arc.

Conversely, split each \(W_C\) at the marked occurrences. Each resulting
piece is a directed terminal-to-terminal trail. Delete directed closed
subwalks whenever a vertex repeats. This leaves a directed path with the same
endpoints and only removes arcs, so no new conflict is introduced. Fixed
points use empty paths. \(\square\)

This formulation is exact, but by itself is only a reduction. The work lies in
constructing and packing the ordered trails.

### B2. Constructive ordered-cycle criteria

**Claim B2, `proved` (path-order criterion).** Suppose the vertices
\(x_1,\ldots,x_k\) occur in that order on a simple undirected cube path
\(R\). Then the single cycle \((x_1\,\ldots\,x_k)\), with all other vertices
fixed, is routable.

**Proof.** For \(j<k\), route \(x_j\to x_{j+1}\) along the corresponding
forward subpath of \(R\). Let \(R'\) be the \(x_1\)-to-\(x_k\) subpath of
\(R\). These forward subpaths partition \(R'\). Route \(x_k\to x_1\) along
\(R'\) in reverse. The final route uses the opposite directed arc of every
arc used forward, so all directed arcs are distinct. \(\square\)

**Claim B3, `proved` (every single \(3\)-cycle).** For any three distinct cube
vertices \(a,b,c\), the permutation \((a\,b\,c)\), with all other vertices
fixed, is routable.

**Proof.** Let \(m\) be the coordinatewise majority of \(a,b,c\). Define

\[
A=\{i:a_i\ne m_i\},\quad
B=\{i:b_i\ne m_i\},\quad
C=\{i:c_i\ne m_i\}.
\]

These coordinate sets are pairwise disjoint: in a binary coordinate, at most
one of \(a,b,c\) differs from the majority. Choose a shortest branch from
\(m\) to each terminal, flipping only its associated coordinate set.
Different branches meet only at \(m\).

Route \(a\to b\) down the \(a\)-branch and up the \(b\)-branch; route
\(b\to c\) down the \(b\)-branch and up the \(c\)-branch; and route
\(c\to a\) down the \(c\)-branch and up the \(a\)-branch. Every branch edge
is used exactly once in each direction. These are distinct directed arcs, so
the three paths are arc-disjoint. Empty branches, when one terminal equals
\(m\), cause no problem. \(\square\)

The same path-and-reverse argument proves a single \(2\)-cycle immediately.
These are proper subclasses, not a solution.

**Claim B4, `proved` (hub-fan routing).** Let a permutation of the vertices
of a bidirected graph have exactly one nontrivial cycle
\(C=(x_1\,\ldots\,x_k)\), with every vertex outside \(C\) fixed. If some
cycle vertex \(r=x_k\) has undirected paths \(R_j\) to \(x_j\),
\(1\leq j<k\), such that any two paths intersect only at \(r\), then the
permutation is routable.

**Proof.** For \(j<k-1\), route \(x_j\to x_{j+1}\) by following \(R_j\)
back to \(r\) and then \(R_{j+1}\) forward. Route
\(x_{k-1}\to r\) backward along \(R_{k-1}\), and route
\(r\to x_1\) forward along \(R_1\). Every branch edge is used exactly once
in each direction, hence every directed arc is used at most once. The
intersection hypothesis makes each concatenation a path. \(\square\)

**Claim B5, `proved`.** For every \(d\geq1\) and
\(2\leq k\leq d+1\), every permutation of \(V_d\) having exactly one
nontrivial cycle of length \(k\) and fixing every other vertex is routable in
\(\overleftrightarrow{Q_d}\).

**Proof.** The cube \(Q_d\) is \(d\)-vertex-connected. A short induction
proves this. The base \(Q_1\) is connected. For \(d\geq2\), after deletion
of at most \(d-1\) vertices, split \(Q_d\) into two \(Q_{d-1}\) halves. If
both halves lose at most \(d-2\) vertices, they
remain connected inductively. The matching between the halves has
\(2^{d-1}>d-1\) edges, while one deleted vertex destroys at most one of
them, so a matching edge survives and joins the two connected remainders.
If one half contains all \(d-1\) deletions, the other is intact and every
surviving vertex of the damaged half has its matching neighbor in the intact
half. Thus deleting fewer than \(d\) vertices never disconnects \(Q_d\).

For completeness, apply the fan lemma with hub \(r=x_k\) and endpoint set
\(X=\{x_1,\ldots,x_{k-1}\}\). Here is its needed proof. Adjoin a new vertex
\(t\) adjacent to every vertex of \(X\). No set of fewer than
\(|X|=k-1\) other vertices separates \(r\) from \(t\): after deleting such
a set, \(Q_d\) remains connected because \(k-1\leq d\), and at least one
vertex of \(X\) remains to provide its edge to \(t\). Vertex Menger's
theorem therefore gives \(k-1\) internally vertex-disjoint \(r\)-to-\(t\)
paths. Truncate each at its first vertex of \(X\), discarding the remaining
suffix and the final edge to \(t\). Their endpoints are distinct, and the
resulting paths form the required fan from \(r\) to all of \(X\). Claim B4
now supplies the routing. \(\square\)

This argument stops at \(k=d+1\) for a concrete reason: a common hub has only
\(d\) incident cube edges, so it cannot support \(k-1>d\) internally
vertex-disjoint branches. It also does not combine several nontrivial cycles.
The fan lemma constructs each fan separately and gives no edge-disjointness
between different fans; if two supporting fans share an undirected edge,
each cycle's construction uses both orientations of that edge, causing an
arc conflict.

### B3. Cayley translations and independent coordinate blocks

For \(a\in\{0,1\}^d\), let \(T_a(x)=x\oplus a\).

**Claim B6, `proved`.** Every translation \(T_a\) has an arc-disjoint
shortest-path routing.

**Proof.** List the coordinates in the support of \(a\) as
\(i_1,\ldots,i_r\). From every \(x\), flip them in that fixed order. At step
\(j\), the current vertex is

\[
z=x\oplus e_{i_1}\oplus\cdots\oplus e_{i_{j-1}}.
\]

As \(x\) ranges over all cube vertices, so does \(z\). Consequently the
step-\(j\) arcs are exactly all directed arcs in dimension \(i_j\), each
once. Different steps use different dimensions. Hence no directed arc is
repeated. \(\square\)

**Claim B7, `proved` (direct product).** Let the coordinates be partitioned
into two blocks \(A,B\). If \(\alpha\) is a routable permutation of \(Q_A\)
and \(\beta\) is a routable permutation of \(Q_B\), then

\[
\sigma(u,v)=(\alpha(u),\beta(v))
\]

is routable in \(Q_{A\cup B}\).

**Proof.** For every fixed \(v\), copy the routing of \(\alpha\) in the
\(A\)-subcube at \(v\). Then, for every fixed \(\alpha(u)\), copy the routing
of \(\beta\) in the \(B\)-subcube at \(\alpha(u)\), and concatenate the two
paths. Copies within a stage lie in disjoint subcubes. The two stages use
disjoint coordinate sets. Thus no directed arc is shared. \(\square\)

As one concrete consequence, swapping two coordinate positions is routable:
in each corresponding \(2\)-face, the vertices with local labels \(00,11\)
are fixed, while

\[
01\to00\to10,\qquad 10\to11\to01
\]

uses four distinct directed arcs. Claim B7 therefore routes any vertex
permutation induced by a product of disjoint coordinate transpositions.

### B4. Why factorization alone fails

**Claim B8, `refuted`.** “Routable permutation factors can always be routed
one after another without creating arc conflicts.”

**Counterexample.** In \(Q_1\), let \(T\) flip the unique bit. Its only
routing uses \(0\to1\) and \(1\to0\). Although \(T\circ T\) is the identity,
concatenating the two factor routings sends

\[
0\to1\to0,\qquad 1\to0\to1,
\]

so each directed arc is used twice. The final identity is of course routed by
empty paths. Thus a Cayley or transposition factorization needs a global arc
allocation or a cancellation theorem; group generation by itself proves
nothing about arc congestion.

### B5. First unresolved cycle step

**B-U1, `unsupported`.** Every single permutation cycle has an ordered closed
trail in the bidirected cube.

Claims B2 through B5 establish useful base classes through cycle length
\(d+1\), but no argument here handles an arbitrary longer cyclic order. Even
a proof of B-U1 would still leave the
independent problem of packing the trails of several cycles. Demanding that
packing for arbitrary cycle partitions is exactly Claim B1 and hence
theorem-strength.

A bounded next target is the single-\((d+2)\)-cycle case, the first length
not covered by the hub-fan argument. It needs an explicit two-hub supporting
tree or a counterexample to such a tree criterion.

## C. Cut, potential, and saturation structure

### C1. Cube boundary theorem

For \(S\subseteq V_d\), let \(\partial S\) be its undirected edge boundary.
Its size is also the number of directed arcs leaving \(S\).

**Claim C1, `proved`.** For every \(S\subseteq V_d\),

\[
|\partial S|\geq \min(|S|,\,2^d-|S|).
\]

If \(S\) is nonempty and \(|S|\leq2^{d-1}\), equality holds if and only if
\(S\) is one side of a coordinate cut.

**Proof.** Induct on \(d\). Identify the two \((d-1)\)-halves and write
\(S=(A,B)\), with \(a=|A|\), \(b=|B|\), and \(M=2^{d-1}\). Assume
\(a+b\leq M\), since boundary is unchanged by complementation. Then

\[
|\partial_{Q_d}S|
=|\partial A|+|\partial B|+|A\mathbin{\triangle}B|.
\]

If \(a,b\leq M/2\), induction gives a lower bound
\(a+b+|A\triangle B|\geq a+b\). If, say, \(a>M/2\), then
\(b<M/2\), and induction plus
\(|A\triangle B|\geq a-b\) gives

\[
|\partial S|\geq (M-a)+b+(a-b)=M\geq a+b.
\]

This proves the inequality.

For equality in the first case, \(A=B\), and both nonempty half-boundaries
must be tight. Induction makes \(A=B\) a coordinate half of \(Q_{d-1}\),
so \(S\) is a coordinate half of \(Q_d\). In the second case, equality forces
\(a+b=M\). The smaller set \(B\) would itself have to attain equality below
half-size; induction forces \(B=\varnothing\), hence \(A=V_{d-1}\). This is
the coordinate cut used in the initial split. The base \(d=1\) is immediate.
\(\square\)

### C2. Every permutation satisfies every directed cut

For a permutation \(\sigma\), define

\[
r_\sigma(S)=|\{x\in S:\sigma(x)\notin S\}|.
\]

**Claim C2, `proved`.** For every \(S\subseteq V_d\),

\[
r_\sigma(S)\leq |\delta^+(S)|.
\]

Every nontrivial tight cut is a coordinate half \(S\), and tightness occurs
there exactly when \(\sigma(S)=V_d\setminus S\).

**Proof.** Distinct sources in \(S\) give
\(r_\sigma(S)\leq |S|\), and their distinct targets outside \(S\) give
\(r_\sigma(S)\leq |V_d\setminus S|\). Claim C1 now proves the cut
inequality. If equality holds, all inequalities are equalities. Claim C1
then makes the smaller side a coordinate half, so both sides have equal
size, and \(r_\sigma(S)=|S|\) says that every target of \(S\) lies in its
complement. Bijection makes the image equal to the complement. The converse
is immediate. \(\square\)

In a tight coordinate cut, any valid routing must use every directed cut arc
once in each direction, and every path crosses that coordinate exactly once.
There are already as many compulsory crossings as available arcs, so any
recrossing would exceed capacity.

### C3. Global down-arc saturation cannot copy the \(2\)-to-\(1\) obstruction

For coordinate \(i\), let

\[
D_i=|\{x:x_i=1,\ \sigma(x)_i=0\}|,\qquad
U_i=|\{x:x_i=0,\ \sigma(x)_i=1\}|.
\]

**Claim C3, `proved`.** For every permutation, \(D_i=U_i\leq2^{d-1}\).
Equality \(D_i=2^{d-1}\) holds exactly when
\(\sigma(x)_i=1-x_i\) for every \(x\). If
\(\sum_iD_i=d2^{d-1}\), then \(\sigma(x)=x\oplus(1,\ldots,1)\), which is
routable by Claim B6.

**Proof.** Sources and targets contain the same number of zeros and ones in
coordinate \(i\), so the number changing \(1\to0\) equals the number changing
\(0\to1\). If all \(2^{d-1}\) sources with bit \(1\) target bit \(0\), they
exhaust the bit-\(0\) targets, and every bit-\(0\) source must target bit
\(1\). This proves the equality characterization. Equality in the sum forces
equality in every coordinate and hence bitwise complementation. \(\square\)

Thus a proof of infeasibility based only on saturating all downward arcs can
never refute the permutation conjecture: the only fully saturated demand is
an explicit routable translation. More local, interacting bottlenecks remain
possible.

### C4. First unresolved flow step

**C-U1, `unsupported`.** The directed cut condition is sufficient for
permutation demands in a bidirected hypercube.

Claim C2 proves necessity only. General integral multicommodity flow has no
such cut-sufficiency theorem. Importing one without hypotheses tailored to
this cube and this Eulerian demand would be invalid. A valid next step would
need a cube-specific splitting-off operation that:

1. preserves every terminal pair, not merely aggregate connectivity;
2. preserves directed-arc capacity one;
3. terminates in an explicitly routable instance; and
4. does not assume the desired path packing in its admissibility condition.

No such operation is proved here.

## Unsupported-inference and blocker ledger

1. **A-U1, missing lemma:** a multi-crossing cut decomposition produces a
   strictly simpler routable request class. The one-crossing partial-
   permutation form is refuted by Claim A3.
2. **A-U2, false lemma:** a Beneš-style alternating lane coloring always has
   satisfiable cycle flips. Refuted by Claim A4 in \(Q_3\).
3. **B-U1, missing lemma:** every single cyclic order has an ordered closed
   trail. Proved here for the path-order class and all cycle lengths at most
   \(d+1\).
4. **B-U2, theorem-strength:** independently constructed trails for distinct
   permutation cycles can always be packed. By Claim B1, the unrestricted
   version is equivalent to the original conjecture.
5. **B-U3, false inference:** routable factors compose. Refuted in \(Q_1\) by
   Claim B8.
6. **C-U1, theorem-strength:** cut sufficiency for these integral
   multicommodity demands. Claim C2 supplies only necessary inequalities.
7. **C-U2, unsupported:** tight coordinate cuts can be peeled off as
   translations. Tightness gives crossing rigidity, but composing or removing
   a translation may reuse the very arcs that are saturated.

## First unresolved step to inspect next

The cleanest theory target is the **single-\((d+2)\)-cycle ordered-trail
lemma**. The hub-fan proof is sharp at the level of one \(d\)-valent hub, so
the next attempt must use a two-hub tree or a different Eulerian support.
This remains a proper subclass of the conjecture and has a concrete
construction or counterexample certificate.

In parallel, the induction route should not retry cross-first routing. Its
next useful artifact is a classification of the smallest source/target
defect left by arbitrary one-cut decompositions, followed by a direct attack
on the one-defect auxiliary request above. Neither target, even if proved,
would alone satisfy the solution contract.
