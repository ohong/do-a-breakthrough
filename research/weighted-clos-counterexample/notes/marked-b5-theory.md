# Closing the \(3/5,2/5\) marked B5 route

## Result

### The marked-family five-colour theorem

**Status: proved.**

Let \(G\) be a finite bipartite multigraph whose edges are marked heavy or
light, with weights

\[
 w(e)=
 \begin{cases}
 3/5,&e\in H,\\
 2/5,&e\in L.
 \end{cases}
\]

If

\[
 \Delta(H)\le3
 \qquad\text{and}\qquad
 \Delta(L)\le6,
\tag{1}
\]

then \(G\) has a proper weighted edge-colouring with five colours.

In particular, every locally three-bin-packable \(3/5,2/5\) instance has
such a colouring. Local feasibility gives (1): at most three heavy edges fit
in three bins, and at most six light edges fit in three bins.

**Proof.**

By König's line-colouring theorem for bipartite multigraphs:

1. properly edge-colour \(L\) with six ordinary colours
   \(\lambda_1,\ldots,\lambda_6\);
2. merge \(\lambda_5\) and \(\lambda_6\) into one global colour 5, and map
   \(\lambda_1,\ldots,\lambda_4\) to global colours \(1,\ldots,4\);
3. independently, properly edge-colour \(H\) with three ordinary colours and
   map them to global colours \(1,2,3\).

At every original vertex, the possible loads are bounded as follows:

| global colour | incident heavy edges | incident light edges | maximum load |
|---:|---:|---:|---:|
| 1, 2, or 3 | at most 1 | at most 1 | \(3/5+2/5=1\) |
| 4 | 0 | at most 1 | \(2/5\) |
| 5 | 0 | at most 2 | \(4/5\) |

All loads are at most one. Equality in colours 1--3 is feasible by the
problem convention. Parallel edges cause no exception because each ordinary
colour class supplied by König is a matching in the multigraph. \(\square\)

This is a special-family theorem, not a proof of the arbitrary-weight
\(n=3\) conjecture and not a novelty claim. It closes Target B5: no marked
counterexample with exactly these two weights exists.

## Mechanism I: proper six-edge-colouring and merging

The successful merge is deliberately applied only to two **light** matching
colours. Merging arbitrary colours of a proper six-edge-colouring of the
whole graph is not justified.

### Fixed-colouring global merge lemma

> Every proper six-edge-colouring of a locally feasible marked graph has a
> pair of colour classes that can be merged.

**Status: refuted.**

For every unordered pair \(\{i,j\}\subseteq\{1,\ldots,6\}\), take a
two-edge star whose two edges are heavy, and colour them \(i\) and \(j\).
The disjoint union of these 15 stars is bipartite and locally feasible: each
centre has two \(3/5\)-edges, placed in separate bins. The displayed
six-edge-colouring is proper.

Every pair of colour classes meets as two adjacent heavy edges at its
corresponding star centre. Merging that pair creates load \(6/5\). Thus this
particular proper colouring has no mergeable colour pair.

The graph is not an obstruction; it is plainly three-colourable after
recolouring its independent star components. The example refutes the fixed
colouring argument, not the theorem. Separating \(H\) and \(L\) is the repair.

### Why the successful merge has no hidden exchange step

The two light classes \(\lambda_5,\lambda_6\) are matchings. Their union has
degree at most two, including at vertices incident with parallel light
edges. Both edges together weigh \(4/5\). Heavy edges are assigned only
colours 1--3, so colour 5 never acquires a hidden heavy-light or heavy-heavy
pair.

No alternating-path recolouring is required.

## Mechanism II: capacity and \(b\)-matching formulation

For a colour \(c\), let \(b_{v,c}\) be the number of light edges of colour
\(c\) allowed at \(v\). The construction proves the following decomposition
lemma.

### Fixed-capacity light decomposition

**Status: proved.**

Every bipartite multigraph \(L\) with \(\Delta(L)\le6\) has a five-colouring
such that at every vertex

\[
 \bigl(d_1(v),d_2(v),d_3(v),d_4(v),d_5(v)\bigr)
 \le (1,1,1,1,2)
\tag{2}
\]

coordinatewise.

**Proof.** Properly edge-colour \(L\) with six colours and merge the last two.
\(\square\)

After properly colouring \(H\) with colours 1--3, (2) is a simultaneous
feasible \(b\)-matching assignment for all light edges:

\[
 b_{v,c}=
 \begin{cases}
 1,&c=1,2,3,4,\\
 2,&c=5.
 \end{cases}
\]

The first three capacities allow one light edge to share a colour with one
heavy edge; the fourth is unused by heavy edges; the fifth holds two lights.
The capacity vector is the same at every vertex, so there is no endpoint
list-alignment problem.

### Local capacity totals alone imply a feasible colour assignment

**Status: refuted in general.**

Take one edge \(uv\). Give \(u\) positive capacity only in colour 1 and \(v\)
positive capacity only in colour 2. Both endpoints have enough total
capacity for their incident degree, but the edge has no common permitted
colour.

This trivial example identifies the real issue in a generic \(b\)-matching
formulation: capacities must align across both endpoints. Lemma (2) succeeds
because it is produced by a global proper edge-colouring, not by checking
the vertex inequalities separately.

## Mechanism III: lists, alternating paths, and minimal counterexamples

One might first assign the light edges any weighted-valid five-colouring,
then give each heavy edge the colours with at most one light edge at both
endpoints. The needed lists need not be large.

### Arbitrary balanced light colouring leaves three common colours

**Status: refuted.**

Let \(uv\) be one heavy edge. At \(u\), add four light pendant edges and
colour them \(1,1,2,2\). At \(v\), add four light pendant edges and colour
them \(3,3,4,4\). The local marked degrees are

\[
 h(u)=h(v)=1,\qquad \ell(u)=\ell(v)=4,
\]

so the instance is locally three-bin feasible. The displayed light
colouring is weighted-valid.

A heavy edge cannot use a colour already containing two light edges at its
endpoint. Its safe sets are therefore

\[
 \{3,4,5\}\text{ at }u,\qquad \{1,2,5\}\text{ at }v,
\]

whose intersection is only \(\{5\}\), not three colours. With several
adjacent heavy edges, ordinary list-edge-colouring cannot be invoked from
such a false list-size bound.

Again, the canonical light decomposition (2) is the repair. Colours 1--4
contain at most one light edge at every vertex. Every heavy edge therefore
has the same four safe colours \(1,2,3,4\), and the proof needs only three of
them.

### Minimal-counterexample conclusion

**Status: proved.**

There is no edge-minimal counterexample inside the \(3/5,2/5\) family.
Indeed, for any alleged counterexample, apply König separately to \(L\) and
\(H\) and use the construction in the theorem. This colours the whole graph
directly, contradicting uncolourability before any deletion, alternating
path, or exchange lemma is needed.

The initially anticipated exchange lemma,

> repair an arbitrary coupled six-colouring by alternating paths until two
> globally mergeable colours appear,

is therefore both false in its fixed-colouring form and unnecessary after
the heavy/light separation.

## Hostile verification checklist

- **Bipartite multigraph:** König's theorem applies with parallel edges.
- **Degree hypotheses:** local three-bin feasibility implies
  \(\Delta(H)\le3\) and \(\Delta(L)\le6\) independently.
- **Global colour names:** heavy colours 1--3 intentionally coincide with
  light matching colours 1--3; their maximum joint load is exactly one.
- **Merged class:** only light colours 5 and 6 are merged.
- **Capacity equality:** \(3/5+2/5=1\) is allowed.
- **Empty subgraphs or unused colours:** pad with empty matching classes.
- **Exact \(n\):** the construction works whether the instance needs one,
  two, or three local bins; exactness is irrelevant to the affirmative
  result.
- **Scope:** no inference is made for weights other than \(2/5\) and \(3/5\).

The B5 search should be retired rather than expanded to larger topologies.
