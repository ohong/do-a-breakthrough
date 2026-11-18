# The total-displacement-six near-antipodal family

Date: 2026-07-23

Status: **proved relative to the published \(Q_p\), \(p\leq3\), strong
Szymanski theorem; independently checked computationally in the finite cases
described below.** No novelty claim has been investigated.

## Result

Let \(A_d(x)=\bar x\) be the antipodal permutation of \(Q_d\), let
\(\tau\) be a permutation of \(Q_d\), and put

\[
\sigma=A_d\circ\tau,\qquad
\Delta(\tau)=\sum_{x\in Q_d}h(x,\tau(x)).
\]

**Theorem (`proved`, with the cited low-dimensional theorem as an external
dependency).** If \(\Delta(\tau)\leq6\), then \(\sigma\) has a family of
pairwise directed-arc-disjoint **shortest** paths.

In particular, every \(\Delta(\tau)=6\) instance asked about in this research
wave is shortest-path routable. It is not a candidate obstruction to the
ordinary Szymanski conjecture.

The external dependency, in the notation used here, is:

> For every \(p\in\{1,2,3\}\) and every permutation \(\alpha\) of
> \(V(Q_p)\), there are pairwise directed-arc-disjoint paths
> \(P_x:x\to\alpha(x)\) with \(|P_x|=h(x,\alpha(x))\) for every \(x\).

Baudon, Fertin, and Havel explicitly attribute exactly this result to
Szymanski: he proved the conjecture for dimensions at most three "with the
stronger property that all the requests are satisfied by shortest paths."
Their preceding definition makes a permutation a \(1\)-to-\(1\) routing
request containing all cube vertices, and their formulation requires pairwise
arc-disjoint directed paths. See pp. 44-45, especially text-extraction lines
51-70; their reference [8] is T. Szymanski, *On the permutation capability of
a circuit-switched hypercube*, ICPP 1989, pp. I-103-I-110:

<https://dept-info.labri.fr/~baudon/Articles/PermutationsHn-versionDAM.pdf>

## Proof

### 1. Only three coordinates can be active

For coordinate \(i\), define

\[
u_i=\left|\{x:x_i=0,\ \tau(x)_i=1\}\right|,\qquad
v_i=\left|\{x:x_i=1,\ \tau(x)_i=0\}\right|.
\]

Because \(\tau\) is a bijection, its target list contains the same number of
zeros and ones in coordinate \(i\) as its source list. Hence \(u_i=v_i\).
The number of source-target pairs changed in coordinate \(i\) is therefore

\[
\delta_i=u_i+v_i=2u_i.
\]

Every active coordinate has \(\delta_i\geq2\), while

\[
\sum_i\delta_i=\Delta(\tau)\leq6.
\]

Thus the active-coordinate set

\[
J=\{i:\exists x,\ x_i\neq\tau(x)_i\}
\]

has size \(p=|J|\leq3\).

If \(p=0\), then \(\tau\) is the identity and \(\sigma=A_d\), whose standard
coordinate-order routing is shortest and arc-disjoint. Hence assume below
that \(1\leq p\leq3\).

### 2. The permutation decomposes into inactive-coordinate fibers

Reorder coordinates so that \(J\) comes first and write

\[
Q_d=Q_p\times Q_q,\qquad q=d-p.
\]

Since \(\tau\) changes no coordinate outside \(J\), it preserves every
\(Q_p\)-fiber. Therefore there is a permutation \(\tau_z\) of \(Q_p\) for
each \(z\in Q_q\) such that

\[
\tau(x,z)=(\tau_z(x),z).
\]

Consequently

\[
\sigma(x,z)=
\left(A_p(\tau_z(x)),A_q(z)\right).
\tag{1}
\]

### 3. Shortest skew-product routing

We use the following closure lemma.

**Lemma (`proved`).** Let \(\beta\) be a shortest-path routable permutation
of \(Q_q\), and for every \(z\in Q_q\) let \(\alpha_z\) be a shortest-path
routable permutation of \(Q_p\). Then

\[
\pi(x,z)=(\alpha_z(x),\beta(z))
\]

is shortest-path routable in \(Q_{p+q}\).

**Proof.** First route

\[
(x,z)\longrightarrow(\alpha_z(x),z)
\]

inside each \(Q_p\)-fiber. The fibers are arc-disjoint. For a fixed
\(x'\in Q_p\), exactly one commodity from each \(z\)-fiber now occupies
\((x',z)\), since every \(\alpha_z\) is a bijection. Route these commodities
as

\[
(x',z)\longrightarrow(x',\beta(z))
\]

inside the \(Q_q\)-fiber indexed by \(x'\).

Different second-phase fibers are arc-disjoint. The first phase uses only the
first \(p\) coordinate directions, while the second uses only the last \(q\),
so the phases share no directed arc. The concatenated path length is

\[
h(x,\alpha_z(x))+h(z,\beta(z))
=h\bigl((x,z),(\alpha_z(x),\beta(z))\bigr),
\]

so every path is shortest. \(\square\)

Apply the lemma to (1) with

\[
\alpha_z=A_p\circ\tau_z,\qquad \beta=A_q.
\]

Each \(\alpha_z\) is an arbitrary permutation of \(Q_p\), and \(p\leq3\), so
the cited strong \(Q_p\) theorem supplies its shortest routing. The antipodal
map \(A_q\) is shortest-path routable by flipping the \(q\) coordinates in
one fixed order for every source; this uses every directed cube arc in those
coordinates exactly once (with the empty routing when \(q=0\)). The lemma now
proves the theorem. Explicitly, the two phase lengths add to

\[
h_p\!\left(x,A_p(\tau_z(x))\right)+q
=h_d\!\left((x,z),
  \left(A_p(\tau_z(x)),A_q(z)\right)\right),
\]

because \(z\) and \(A_q(z)\) differ in all \(q\) inactive coordinates. Thus
the construction has no hidden detour. \(\square\)

The construction is uniform. It does not require a case-by-case splice for
the cycle types below.

## Exact coarse classification at displacement six

Every nontrivial cycle \(C=(x_1,\ldots,x_k)\) of \(\tau\) has an even positive
cost

\[
c(C)=\sum_{j=1}^k h(x_j,x_{j+1}),\qquad x_{k+1}=x_1.
\]

Indeed, every coordinate is toggled an even number of times around the closed
cycle. Therefore the nontrivial cycle costs partition \(6\) as

\[
2+2+2,\qquad 2+4,\qquad\text{or}\qquad6.
\]

This gives the following complete classification by cycle length and cyclic
side lengths:

| Cost partition | Nontrivial cycle types |
|---|---|
| \(2+2+2\) | three transpositions of adjacent vertices |
| \(2+4\) | one adjacent transposition, plus either a distance-two transposition, a \(3\)-cycle with side lengths \(1,1,2\), or an oriented square |
| \(6\), \(2\)-cycle | a distance-three transposition |
| \(6\), \(3\)-cycle | side lengths \(1,2,3\) or \(2,2,2\) |
| \(6\), \(4\)-cycle | side-length multiset \(1,1,1,3\) or \(1,1,2,2\); the latter has adjacent and alternating cyclic orders |
| \(6\), \(5\)-cycle | cyclic side lengths \(1,1,1,1,2\) |
| \(6\), \(6\)-cycle | six cube edges |

The table is exhaustive. A nontrivial \(k\)-cycle has at least \(k\) total
side length. For costs \(2,4,6\), listing the positive integer side lengths
and imposing the Hamming triangle inequality leaves exactly the entries
shown. The even-cost observation rules out every other partition.

This is a metric/cycle classification, not a finite classification of every
ambient \(Q_d\) orbit. Different cycles can occupy different fibers of the
inactive coordinates, and their relative fiber distances remain parameters
as \(d\) grows. The proof above deliberately avoids pretending those placements
form one finite orbit list.

## \(Q_3\) cube-automorphism refinement

For the local \(Q_3\) case, exhaustive enumeration gives 876 permutations
with \(\Delta=6\), split into 27 conjugacy orbits under translations and
coordinate permutations. The exact coarse-signature counts are:

| Cycle metric signature | Permutations | Cube-automorphism orbits |
|---|---:|---:|
| three adjacent transpositions | 44 | 3 |
| adjacent plus distance-two transposition | 72 | 2 |
| adjacent plus \(1,1,2\) three-cycle | 240 | 5 |
| adjacent plus square | 48 | 1 |
| distance-three transposition | 4 | 1 |
| \(1,2,3\) three-cycle, both directed orientations | 48 | 2 |
| \(2,2,2\) three-cycle | 16 | 1 |
| \(1,1,1,3\) four-cycle | 48 | 1 |
| \(1,1,2,2\) four-cycle, nonalternating | 96 | 2 |
| \(1,2,1,2\) four-cycle | 84 | 4 |
| \(1,1,1,1,2\) five-cycle | 144 | 3 |
| six-edge six-cycle | 32 | 2 |
| **Total** | **876** | **27** |

The result JSON retains a canonical representative, directed cycle notation,
orbit size, and shortest-routing witness for every orbit.

## Computation and independent audit

These checks support the proof but are not being substituted for it.

- Exhaustive \(Q_3\): all 876 permutations with \(\Delta=6\) were transformed
  to \(\sigma=A_3\circ\tau\); the exact shortest-path flow model returned
  `sat` for all 876.
- Orbit lifts: all 27 local \(Q_3\) orbit representatives were placed in one
  active fiber of \(Q_4\) and \(Q_5\); all 54 shortest-path instances were
  `sat`.
- Multi-fiber probes: four structured \(Q_5\) instances covering
  \(2+2+2\) and all three \(2+4\) subtypes were `sat`.
- A separate standard-library checker, which does not import the routing
  solver, reconstructed the exact 876-element population and its 27 orbits
  and validated 961 stored shortest-routing certificates comprising 22,594
  directed-arc occurrences. All checks passed.

Reproduction:

```sh
cd research/szymanski-conjecture/code
python3 slack_six.py \
  --output ../results/2026-07-23-slack-six/exhaustive-and-lifts.json \
  --timeout-seconds 10
python3 audit_slack_six.py \
  ../results/2026-07-23-slack-six/exhaustive-and-lifts.json \
  --output ../results/2026-07-23-slack-six/independent-audit.json
```

Artifacts:

- `code/slack_six.py`
- `code/audit_slack_six.py`
- `results/2026-07-23-slack-six/exhaustive-and-lifts.json`
- `results/2026-07-23-slack-six/independent-audit.json`

## Hostile-audit notes

1. The proof uses the set of coordinates changed by \(\tau\), not merely the
   coordinates appearing in one cycle. The balance argument is global and
   still gives at most three.
2. A permutation preserving inactive coordinates really does restrict to a
   permutation on each fiber: injectivity of \(\tau\) supplies injectivity of
   each finite restriction.
3. Phase two of the skew product is legitimate because every
   \(\alpha_z\) is bijective. Without that fact, several commodities could
   arrive at the same \((x',z)\) lane.
4. Shortestness is additive because the two phases use disjoint coordinate
   sets. This would fail for an arbitrary two-stage decomposition.
5. The published low-dimensional strong theorem is the only nontrivial
   external dependency. The original 1989 full text was not retrieved in this
   run, but the 2001 paper states the result explicitly.
6. Correctness and novelty are separate. This bounded wave did not search the
   literature for the active-coordinate reduction, so no claim that the
   theorem is new should be made without an expert literature review.

The next unresolved slack value is \(\Delta=8\). The same active-coordinate
argument only reduces that case to the strong \(Q_4\) statement, which is
false in general, so the proof stops exactly there.
