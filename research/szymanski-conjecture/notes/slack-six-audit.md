# Hostile audit: the total-displacement-six theorem

Date: 2026-07-23

Audited claim: for every \(d\geq 1\), permutation \(\tau\) of \(Q_d\), and
\(\sigma=A_d\circ\tau\), if

\[
\Delta(\tau)=\sum_{x\in Q_d}h(x,\tau(x))\leq 6,
\]

then \(\sigma\) has a pairwise directed-arc-disjoint shortest-path routing.

## Verdict

**PASS, with one source-provenance caveat.** The reduction and closure proof
are valid. I found no missing case, capacity collision, path-simplicity issue,
or shortestness gap. The only non-elementary dependency needed is exactly the
strong \(Q_p\) result for \(p\leq 3\). Baudon, Fertin, and Havel (2001) state
that result explicitly, but attribute it to Szymanski (1989). The original
1989 full text was not retrieved in this research run. Thus:

- mathematical status: **proved using the published low-dimensional result**;
- source status: **corroborated by a peer-reviewed published paper, but not
  checked against the original proof**;
- contract status under the unusually strict primary-source clause in
  `contract.md`: **downgrade to source-pending, not theorem-pending**, until
  the 1989 paper itself is inspected.

This caveat does not make the theorem merely computational or conjectural. It
limits only the strength of the provenance claim.

## Step-by-step attack

### 1. Coordinate movement parity: pass

Fix a coordinate \(i\). Let \(u_i\) count \(0\to1\) movements and \(v_i\)
count \(1\to0\) movements under \(\tau\). Among all sources of \(Q_d\), exactly
\(2^{d-1}\) have bit \(1\); because \(\tau\) is a bijection, the same is true
among all targets. Counting target ones in two ways gives

\[
2^{d-1}-v_i+u_i=2^{d-1},
\]

so \(u_i=v_i\). Hence

\[
\delta_i=\left|\{x:x_i\ne\tau(x)_i\}\right|=u_i+v_i=2u_i.
\]

If coordinate \(i\) is active, \(u_i>0\), so \(\delta_i\geq2\). Also,
interchanging the two finite sums gives

\[
\sum_i\delta_i
=\sum_x\left|\{i:x_i\ne\tau(x)_i\}\right|
=\sum_xh(x,\tau(x))
=\Delta(\tau).
\]

Therefore \(\Delta\leq6\) implies at most three globally active coordinates.
This uses global bijectivity, not cycle-by-cycle reasoning, and survives
fixed points and permutations whose nontrivial cycles lie in different
fibers.

### 2. Active-coordinate set: pass

Let \(J\) be the union, over every source \(x\), of the coordinates on which
\(x\) and \(\tau(x)\) differ. The proof uses this global union. From Step 1,
\(|J|\leq3\). There is no hidden assumption that one common cycle or one
source witnesses every active coordinate.

### 3. Fiber decomposition: pass

After a coordinate permutation, write \(Q_d=Q_p\times Q_q\), where the first
\(p=|J|\) coordinates are active. By the definition of \(J\), every inactive
coordinate is fixed pointwise by \(\tau\). Thus

\[
\tau(x,z)=(f_z(x),z)
\]

for some map \(f_z:Q_p\to Q_p\). If \(f_z(x)=f_z(y)\), global injectivity of
\(\tau\) gives \(x=y\). A finite injective self-map of \(Q_p\) is bijective,
so \(f_z=\tau_z\) is a permutation. This proves, rather than assumes, that no
commodity can migrate between inactive-coordinate fibers.

Complementation factors across the product, so

\[
(A_d\circ\tau)(x,z)
=\bigl(A_p(\tau_z(x)),A_q(z)\bigr).
\]

The composition order is correct. No commutativity of \(A_p\) and \(\tau_z\)
is used.

### 4. Skew-product closure: pass

For

\[
\pi(x,z)=(\alpha_z(x),\beta(z)),
\]

route first inside each \(z\)-fiber from \(x\) to \(\alpha_z(x)\).

- Within one fiber, arc-disjointness is the hypothesis on \(\alpha_z\).
- Distinct \(z\)-fibers have disjoint vertex sets, hence disjoint arcs.

At the phase boundary, fix a lane label \(x'\). For each \(z\), exactly one
commodity arrives at \((x',z)\), namely the commodity whose first coordinate
is \(\alpha_z^{-1}(x')\). This is where bijectivity of every \(\alpha_z\) is
essential. Copy a routing of \(\beta\) into each fixed-\(x'\) \(Q_q\)-fiber.

- Within a lane, arc-disjointness is the hypothesis on \(\beta\).
- Different \(x'\)-lanes have disjoint vertex sets, hence disjoint arcs.
- Phase one flips only an active coordinate; phase two flips only an inactive
  coordinate. Since a cube arc has one unique coordinate, the two phases
  cannot share a directed arc.

The commodity indexed by \((x,z)\) finishes at
\((\alpha_z(x),\beta(z))\), its stated target. The target map is a permutation:
given \((x',z')\), its unique preimage is

\[
z=\beta^{-1}(z'),\qquad x=\alpha_z^{-1}(x').
\]

Thus the construction neither loses nor duplicates a commodity.

### 5. Path simplicity and shortestness: pass

Let the selected local paths be shortest. The concatenated walk has length

\[
h(x,\alpha_z(x))+h(z,\beta(z))
=h\bigl((x,z),(\alpha_z(x),\beta(z))\bigr),
\]

because the coordinate blocks are disjoint. This equals the graph distance
between its endpoints in \(Q_{p+q}\). Therefore the concatenated walk is
itself shortest. In particular it cannot repeat a vertex or contain a
cycle, so it is a path rather than merely a walk.

One can also see the only possible intersection between the two phase
segments directly. A first-phase vertex has inactive coordinate \(z\), while
a second-phase vertex has active coordinate \(\alpha_z(x)\). A shortest first
segment reaches that active coordinate only at its end, and a shortest second
segment has inactive coordinate \(z\) only at its start. Their unique common
vertex is the phase boundary. Empty first or second phases cause no problem.

### 6. Antipodal factor: pass

For \(A_q\), choose one coordinate order and flip those \(q\) coordinates for
every source. Each path has length \(q\), hence is shortest and simple.

For the stage that flips coordinate \(j\), the map from a source \(z\) to the
tail reached after the preceding fixed coordinate flips is an XOR
translation, hence a bijection of \(Q_q\). Consequently, as \(z\) ranges over
all sources, this stage uses every directed arc in coordinate \(j\) exactly
once. Different stages use different coordinate directions. The paths are
therefore pairwise directed-arc-disjoint. For \(q=0\), all paths are empty.

### 7. Low-dimensional dependency: pass with provenance caveat

Baudon, Fertin, and Havel define a permutation request and directed
arc-disjoint routing, then state:

> Szymanski proved it for \(n\leq3\), with the stronger property that all
> requests are satisfied by shortest paths.

This appears on pp. 44-45 (PDF text lines 64-71):

<https://dept-info.labri.fr/~baudon/Articles/PermutationsHn-versionDAM.pdf>

That statement has precisely the required strength for

\[
\alpha_z=A_p\circ\tau_z,
\]

because the composition of two bijections is an arbitrary permutation of
\(Q_p\), and \(p\leq3\). It is about the directed symmetric hypercube and
pairwise arc-disjoint paths, so there is no undirected-edge-disjointness or
vertex-disjointness mismatch.

The cited statement is a later paper's report of Szymanski's theorem, not the
original proof. Under ordinary mathematical practice this is a valid,
specific published dependency. Under `contract.md`'s requirement that every
external theorem be checked from a primary source, the source audit remains
incomplete until the 1989 paper is read.

### 8. Boundary cases: pass

- \(p=0\): \(\tau=\mathrm{id}\), so \(\sigma=A_d\), handled by the antipodal
  construction without invoking the low-dimensional theorem.
- \(q=0\): the second phase is empty; the result is exactly the strong
  \(Q_p\) theorem with \(p=d\leq3\).
- Fixed points of \(\tau\): allowed and remain within their inactive fiber.
- Fixed points of \(\alpha_z\) or \(\beta\): use length-zero paths and consume
  no arc, consistently with the adopted convention in `contract.md`.
- \(d=1,2,3\): included. No proof step assumes \(d\geq5\).
- \(\Delta=0,2,4\): included because the argument uses \(\Delta\leq6\), not
  equality.

## Computation: regression evidence only

I inspected `code/slack_six.py`, `code/audit_slack_six.py`, and the stored
result summaries. The independent standard-library checker:

- reconstructs all \(8!=40320\) permutations of \(Q_3\) and selects exactly
  the 876 with \(\Delta=6\);
- independently recomputes the 27 translation/coordinate-permutation orbits;
- checks the target permutation, endpoints, cube adjacency, simple paths,
  shortest lengths, and directed-arc uniqueness for every stored
  certificate;
- reports 961 certificates and 22,594 directed-arc occurrences checked.

The stored summary reports all checks passed. This is coherent finite
regression evidence. It is not needed to prove the all-dimension theorem and
does not repair the source-provenance caveat. In particular, the finite audit
does not independently prove the strong theorem for every permutation of
\(Q_3\); the proof legitimately obtains that fact from the cited published
result.

## Attempts to falsify the mechanism

The proof would fail under any of the following weakenings, none of which
occurs here:

1. If \(\tau\) were only a request relation rather than a permutation,
   \(u_i=v_i\) could fail.
2. If any \(\alpha_z\) were not bijective, multiple commodities could enter
   the same second-phase lane.
3. If the two phases shared coordinate directions, phase-to-phase arc
   collisions and a nonadditive length bound would become possible.
4. If only arbitrary-path routing (rather than shortest routing) were known
   for \(Q_p\), the construction would still prove ordinary routability but
   not the theorem's shortest-path conclusion.
5. Replacing \(\Delta\leq6\) by \(\Delta\leq8\) permits four active
   coordinates. The required strong \(Q_4\) statement is false, so this proof
   does not extend by the same dependency.

None exposes a defect in the stated \(\Delta\leq6\) theorem.

## Final classification

| Item | Result |
|---|---|
| Even coordinate movement count | Pass |
| At most three globally active coordinates | Pass |
| Fiber decomposition of \(\tau\) | Pass |
| Formula for \(A_d\circ\tau\) | Pass |
| Skew-product target accounting | Pass |
| Directed-arc disjointness | Pass |
| Path simplicity | Pass |
| Shortestness | Pass |
| Antipodal routing | Pass |
| Strong \(Q_p\), \(p\leq3\), theorem strength | Pass |
| Strong \(Q_p\) original-source inspection | Pending |
| Finite regression evidence | Pass, non-probative |

Recommended status wording: **“proved using the low-dimensional strong theorem
reported by Baudon, Fertin, and Havel; original-source verification pending.”**
