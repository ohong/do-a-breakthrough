# Hostile audit: structural route

Date: 2026-07-23

Audited against `contract.md`: `notes/solver-structural.md`, with special
attention to C2, S3/S4, M2/M3, and B2.

## Verdict

**The audited claims survive.** I found no false theorem, missing endpoint,
reused directed arc, or illicit jump from fractional to integral routing.
The note correctly labels the surviving work as partial and does not satisfy
the full conjecture contract.

This verdict is not a novelty judgment and does not elevate finite checks into
proof. C2, S3/S4, and M2/M3 stand on their written dimension-free arguments;
the independent program below is only a regression check on their small cases.

## C2: cut expansion and equality

**Verdict: valid.**

The induction has the needed equality bookkeeping.

- After complementing, write \(0<|S|=a+b\le 2^{d-1}\) with \(a\ge b\).
  If \(a\le2^{d-2}\), equality in
  \[
  b_d(S)\ge a+b+(a-b)=2a\ge a+b
  \]
  forces \(a=b\), equality in
  \(|S_0\triangle S_1|\ge a-b\), hence \(S_0=S_1\), and equality in
  both sectional induction bounds. A nonempty equality section has size
  \(2^{d-2}\) and is a coordinate halfcube in \(Q_{d-1}\), so its double
  is a coordinate halfcube in \(Q_d\).
- If \(a>2^{d-2}\), the lower bound is \(2^{d-1}\). Equality with
  \(|S|=a+b\) first forces \(a+b=2^{d-1}\). Equality for a nonempty
  \(S_1\) would make its size \(2^{d-2}\), contradicting
  \(b<2^{d-2}\). Thus \(b=0\), \(a=2^{d-1}\), which is exactly the
  halfcube in the split coordinate.

I independently enumerated every nonempty proper subset through \(Q_4\).
There were no expansion violations, and the equality sets numbered
\(2d\) in each dimension, exactly the coordinate halfcubes:

| \(d\) | subsets checked | nontrivial equality sets |
|---:|---:|---:|
| 1 | 2 | 2 |
| 2 | 14 | 4 |
| 3 | 254 | 6 |
| 4 | 65,534 | 8 |

## S3/S4: classification and constructions

**Verdict: valid.**

The classification follows from the support size and cycle type of
\(\tau\), whose total displacement is \(\Delta\). The only point that is
implicit in the prose is harmless: in the three-cycle case, the cycle must be
cyclically relabeled so that its two unit-distance moves appear first. The
\(1,1,2\) distance multiset guarantees that rotation.

The splice argument was checked at its vulnerable points:

- If \(a\) and \(b\) differ on a consecutive coordinate block, the endpoint
  of \(a\)'s prefix before the block equals the start of \(b\)'s suffix after
  the block, and conversely.
- The new paths omit exactly the differing block. Therefore they end at
  \(\bar b,\bar a\), respectively, and their lengths equal their Hamming
  distances.
- For two disjoint adjacent transpositions, all reassigned arcs are subsets
  of four distinct paths in the standard antipodal arc decomposition.
  Performing both splices cannot create a cross-pair collision.
- In the three-cycle construction, the two added arcs are exactly the
  \(p,q\) block of the original route from \(b\). In the four-cycle
  construction, the four added arcs are exactly the corresponding blocks of
  the original routes from \(b\) and \(r\). Prefixes retain their original
  owners, and no discarded block is still used by another modified path.
- Each modified path flips each coordinate on which its endpoints differ
  exactly once. This proves shortestness as well as simplicity.

The independent checker `code/audit_structural.py` does not import the main
routing implementation. It generates every permutation \(\tau\) with total
displacement \(0,2,\) or \(4\) from support sizes at most four, reconstructs
the claimed route, and checks source, target, adjacency, simplicity,
shortestness, and global directed-arc uniqueness. Results:

| \(d\) | \(\Delta=0\) | \(\Delta=2\) | \(\Delta=4\) | total verified |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 2 |
| 2 | 1 | 4 | 14 | 19 |
| 3 | 1 | 12 | 114 | 127 |
| 4 | 1 | 32 | 688 | 721 |

These counts match the closed forms in the structural note. No construction
failed.

## M2: fractional equivalence

**Verdict: valid, and explicitly fractional only.**

The path-load set is a compact convex polytope because each commodity has a
finite set of simple paths and independently chooses a probability
distribution over them. Its intersection with the capacity box is precisely
a fractional unit multiflow.

If the sets are disjoint, strict finite-dimensional separation can be
oriented as
\[
\min_{k\in K}c\mathbin{\cdot}k
   > \max_{b\in[0,1]^A}c\mathbin{\cdot}b.
\]
Replacing \(c\) by \(c_+\) preserves the strict inequality: loads are
nonnegative, so the left side cannot decrease, and the right side was already
\(\sum_a(c_a)_+\). For this nonnegative length vector, minimizing over the
independent path distributions separates by commodity and gives the sum of
directed shortest-path distances. Thus the full family of metric inequalities
is equivalent to fractional feasibility.

Nothing in this argument supplies integrality, and the note correctly refuses
to infer arc-disjoint paths from it.

## M3: potential LP and certificate

**Verdict: valid.**

For fixed nonnegative \(\ell\), the constraints
\[
p_x(v)-p_x(u)\le\ell(u,v),\qquad p_x(x)=0
\]
bound \(p_x(\sigma(x))\) by the length of every source-target path. The
directed distance labels \(p_x(v)=d_\ell(x,v)\) attain the bound by the
triangle inequality. Hence maximizing the sum of target potentials jointly
with normalized lengths really does maximize the left side of the metric
inequality.

Normalizing \(\sum_a\ell(a)=1\) loses no strict violation: a length vector of
total zero has every directed distance zero, while every nonzero violating
vector can be scaled. Rational LP data gives a rational optimum and, after
clearing denominators, the listed local integer certificate. Summing the
potential inequalities along arbitrary paths proves that such a strict
certificate is independently checkable and obstructs fractional, hence also
integral, routing.

## B2: \(Q_2\) Beneš refutation

**Verdict: valid as a refutation of the restricted architecture only.**

For \(\sigma=(00)(01\ 10)(11)\), I independently enumerated all colorings for
each possible split coordinate. Exactly two colorings balance both input and
output pairs for either split, and neither satisfies the no-double-swap
condition at every physical pair. Coordinate exchange symmetry gives the same
result for the second split.

The unrestricted witness also checks:
\[
01\to00\to10,\qquad 10\to11\to01.
\]
All four steps are cube arcs, the two paths have the required endpoints and
shortest length two, and their directed arcs are distinct. Empty paths at
\(00\) and \(11\) consume no arcs. Therefore the example kills only the
first/middle/last split mechanism, not Szymanski's conjecture.

## Reproduction

Run:

```sh
python3 research/szymanski-conjecture/code/audit_structural.py
python3 -m py_compile research/szymanski-conjecture/code/audit_structural.py
```

Observed: all 869 low-slack route families through \(d=4\) verified, every
cut subset through \(d=4\) checked, and the \(Q_2\) split refutation plus its
unrestricted routing verified.

## Scope boundary

The audit leaves the structural route exactly where its author placed it:

- low slack through \(\Delta=4\) is settled affirmatively;
- a metric violation remains an exact counterexample mechanism;
- universal fractional feasibility is unproved;
- fractional-to-integral rounding is unproved; and
- no result here proves or disproves the full conjecture.
