# Single-\((d+2)\)-cycle probe

Date: 2026-07-23

Status: **blocked; no theorem about the \((d+2)\)-cycle case**

The audited hub-fan theorem routes every permutation with one nontrivial
cycle of length at most \(d+1\). This probe tested two natural extensions to
the first uncovered length, \(d+2\).

## Paired-branch route

The attempted reduction first sought consecutive terminals \(u,v\) that
remain connected after deleting the other \(d\) terminals. A solver reported
an existence argument from the minimum-cut classification of \(Q_d\), but
that argument was not written out or hostile-audited before the probe was
stopped, so it is **not accepted into this record**. The stronger statement
for an arbitrary consecutive pair is false: in \(Q_2\), opposite \(u,v\)
become disconnected when their two common neighbors are deleted.

This suggests a supporting tree with \(d\) branches from one root, where one
branch contains a prescribed avoiding path \(P:u\leadsto v\) and the other
\(d-1\) branches separately contain the remaining terminals.

Even granting such a pair and an avoiding path \(P\), the exact next
unsupported step is the existence of that paired-branch tree. The ordinary
fan lemma does not preserve a prescribed path \(P\), and contracting \(P\) is
invalid because contraction need not preserve the \(d\)-connectivity needed
for the fan argument. No replacement lemma was proved.

## One-bridge split is false as a universal method

In \(Q_3\), consider the prescribed five-terminal cyclic order

\[
(000,011,100,001,110).
\]

For every coordinate, the corresponding cyclic bit word has four
transitions. A construction that splits on one coordinate and permits only
one undirected bridge between the halves can supply only the two opposite
directed bridge arcs, hence at most two cyclic transitions. Therefore no
coordinate realizes this order by that restricted one-bridge construction.

This refutes only the proposed construction. It is not a counterexample to
the single-\((d+2)\)-cycle statement or to Szymanski's Conjecture.

## Disposition

The single-\((d+2)\)-cycle case remains open in this record. A useful next
step would prove the paired-branch tree lemma with all avoidance hypotheses,
or give a cube counterexample to that lemma. Merely contracting the prescribed
path or invoking the ordinary fan lemma is not valid.
