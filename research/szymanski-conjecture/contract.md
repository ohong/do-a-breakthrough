# Exact solution contract

Status: **source-audited and repaired**

## Primary-source wording

Ted H. Szymanski's 1989 paper states in its abstract that “the conjecture that
the circuit switched hypercube is rearrangeable for arbitrary N is
postulated.”

Separately, Baudon-Fertin-Havel define the \(d\)-cube to have \(2^d\)
vertices, so their notation identifies the network size as \(N=2^d\).

The modern surviving formulation is the one recorded by West's REGS problem
page and by Baudon, Fertin, and Havel (2001): rearrangeability by arbitrary
directed paths, without a shortest-path requirement.

## Normalized formal statement

For every integer \(d\ge 1\), let

\[
V_d=\{0,1\}^d,\qquad
A_d=\{(x,x\oplus e_i):x\in V_d,\ 1\le i\le d\},
\]

where \(e_i\) flips coordinate \(i\). Thus
\(\overleftrightarrow{Q_d}=(V_d,A_d)\) is the bidirected \(d\)-cube.

For every bijection \(\sigma:V_d\to V_d\), there must exist a family
\((P_x)_{x\in V_d}\) such that:

1. \(P_x\) is a directed path from \(x\) to \(\sigma(x)\);
2. if \(x\ne y\), then \(P_x\) and \(P_y\) share no directed arc.

Equivalently, every permutation routing request on the bidirected hypercube is
rearrangeable with directed-arc congestion one.

## Affirmative completion criteria

A complete affirmative solution must:

1. prove the normalized statement for every integer \(d\ge1\) and every
   permutation \(\sigma\);
2. construct the paths or prove their existence without assuming a
   theorem-strength routing lemma equivalent to the conjecture;
3. cover fixed points and all cycle structures of \(\sigma\), without assuming
   a shortest-path restriction (chosen routes may be shortest or non-shortest);
4. show explicitly that directed-arc capacity is at most one; and
5. verify every external theorem and all of its hypotheses from a primary
   source.

## Negative completion criteria

A complete negative solution must:

1. give an explicit dimension \(d\ge1\) and an explicit permutation
   \(\sigma\) of all \(2^d\) vertices;
2. verify that every vertex occurs exactly once as a source and once as a
   target;
3. prove that no family of directed \(x\)-to-\(\sigma(x)\) paths can be
   pairwise arc-disjoint; and
4. if infeasibility is computational, supply reproducible code plus a
   checkable exhaustive certificate, and independently verify both the search
   space and the certificate from a second formulation or implementation.

The cited results prove the statement through \(d=4\), so any genuinely new
counterexample must in fact have \(d\ge5\). This is the known search frontier,
not part of the formal negation.

## Conventions and edge cases

- The source range is \(d\ge1\). As an auxiliary observation outside that
  sourced range, the \(d=0\) case is immediate under the empty-path
  convention.
- The audited sources do not specify the fixed-point convention. This contract
  adopts the standard convention that \(\sigma(x)=x\) uses the length-zero
  path and consumes no arc. If the original paper imposes a different
  convention, the contract must be revised.
- “Edge-disjoint” in the bidirected graph means **arc-disjoint**. The arcs
  \((u,v)\) and \((v,u)\) are distinct and may both be used.
- The sources impose arc-disjointness and state no vertex-disjointness
  condition. Under the standard meaning of arc-disjoint paths, shared vertices
  are therefore permitted.
- The ordinary conjecture explicitly has no shortest-path condition. It also
  states no monotonicity or common-coordinate-order restriction, so this
  contract adds neither.

## Results that do not satisfy the contract

- a counterexample requiring paths to be shortest;
- a non-routable \(2\)-to-\(1\) request that is not a permutation;
- finite, random, heuristic, or bounded-length testing without exhaustive
  coverage;
- a proof only for \(d=5\), a special cycle type, or another proper subclass;
- congestion two, two wavelengths, fractional flow, or asymptotic congestion;
- checking only cut conditions;
- a conditional theorem or a reduction to an unproved claim of comparable
  strength.

## Allowed dependencies

Standard finite graph theory, exact combinatorics, integral single-commodity
flow, and elementary group actions may be used once their exact statements and
hypotheses are recorded. Any multicommodity integrality, path-pairability, or
hypercube routing theorem must be checked against its primary source and may not
silently assume the desired conclusion.

## Verification plan

1. Independently compare every quantifier, domain, and convention above with
   Szymanski (1989), Baudon-Fertin-Havel (2001), and the REGS statement.
2. For a proof, map each conclusion in the formal statement to a numbered proof
   step, then ask a fresh hostile reviewer to falsify every lemma and boundary
   case.
3. For a counterexample, check the permutation mechanically, encode
   unrestricted simple directed paths, certify infeasibility exactly, and
   reconstruct the check independently without copying the first
   implementation.
4. Before restricting a search to simple paths, prove the cycle-deletion lemma:
   for distinct endpoints, deleting a repeated-vertex segment from a directed
   routing walk preserves its endpoints and cannot introduce an arc conflict.
   Handle fixed points separately under the adopted empty-path convention.
5. Treat bounded computation as evidence only unless completeness is proved.
6. Search later literature separately for the statement, construction, and
   proof mechanism before making any novelty claim.
