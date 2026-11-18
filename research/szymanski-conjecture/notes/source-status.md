# Source and status record

Search date: 2026-07-23

## Primary source

- T. H. Szymanski, *On the Permutation Capability of a Circuit-Switched
  Hypercube*, Proceedings of the International Conference on Parallel
  Processing, vol. I (1989), pp. I-103–I-110.
- DBLP confirms the bibliographic record:
  https://dblp.org/rec/conf/icpp/Szymanski89
- An author-uploaded copy/abstract is indexed at:
  https://www.researchgate.net/publication/221085303_On_the_Permutation_Capability_of_a_Circuit-Switched_Hypercube

The original full-text download was not retrieved in this run: the available
endpoint returned access errors. The primary-source abstract states
rearrangeability for arbitrary \(N\); the exact modern graph formulation below
is corroborated by the later research paper and the authoritative open-problem
page. No DOI was found for the 1989 proceedings paper.

## Exact modern formulation and known boundary

- D. B. West, REGS in Combinatorics, *Szymanski's Conjecture - Routing
  Permutations in Hypercubes (1989)*:
  https://dwest.web.illinois.edu/regs/szymanski.html
- O. Baudon, G. Fertin, and I. Havel, *Routing permutations and 2-1 routing
  requests in the hypercube*, Discrete Applied Mathematics 113 (2001), 43–58,
  DOI 10.1016/S0166-218X(00)00386-3:
  https://dept-info.labri.fr/~baudon/Articles/PermutationsHn-versionDAM.pdf

Baudon-Fertin-Havel define a permutation as a \(1\)-to-\(1\) routing request
with exactly \(|V(Q_d)|\) pairs, state the arbitrary-path conjecture, prove it
for \(d=4\) by computer-assisted reduction, and explicitly leave \(d\ge5\)
open. Szymanski had proved \(d\le3\).

## Variant that is already false

- A. Lubiw, *Counterexample to a conjecture of Szymanski on hypercube
  routing*, Information Processing Letters 35(2) (1990), 57–61,
  DOI 10.1016/0020-0190(90)90106-8.

Lubiw refutes the additional requirement that every route be shortest.
Baudon-Fertin-Havel call that the **strong Szymanski conjecture**. It is not the
surviving target of this run.

## Current-status caution

An independent targeted search of publisher records, author PDFs, arXiv/ECCC,
and authoritative problem lists found no accepted proof or counterexample to
the arbitrary-path statement after the 2001 \(d=4\) result. The REGS page still
lists it as a conjecture. The ordinary conjecture therefore remains open for
\(d\ge5\) as of 2026-07-23, subject to the search limitation below.

An attempted OpenAlex citation-graph check could not be completed. Absence
from the sources searched is not a formal exhaustive bibliographic
certification and cannot establish novelty.

## Useful partial results

- Gu and Tamaki (1997) prove that two sets/time slots/wavelengths suffice for
  every permutation. This is congestion two, not the conjecture.
- Sprague and Tamaki (1994) handle involutions; West's REGS page summarizes
  the exceptional cases for the stronger symmetric-path construction.
- Briët, Chakraborty, García-Soriano, and Matsliah (2012) give much stronger
  negative results for **shortest-path** routing. These do not touch arbitrary
  paths.
- Baudon-Fertin-Havel show non-routable \(2\)-to-\(1\) requests in every
  dimension \(d\ge3\). Such a request is not a permutation.

## Naming check

No second open problem commonly carrying the singular name “Szymanski's
Conjecture” was found. A solved joint conjecture of Dudek, Szymański, and
Zwonek on stable graphs is unrelated. Ted H. Szymanski publishes his name
without the accent.

## Full-text recovery addendum

The ResearchGate record exposes an author-uploaded eight-page PDF at:

https://www.researchgate.net/profile/Ted-Szymanski/publication/221085303_On_the_Permutation_Capability_of_a_Circuit-Switched_Hypercube/links/0c960526855f1654ea000000/On-the-Permutation-Capability-of-a-Circuit-Switched-Hypercube.pdf

The PDF object was identified as `application/pdf`, but its pages could not be
inspected: subsequent lawful fetches returned HTTP 429, cache-miss, or 404
errors. A direct download also failed under restricted DNS, and the requested
network escalation was interrupted. No access control was bypassed.

The accessible primary-source abstract does state that, when every connection
is required to have minimum distance, the circuit-switched hypercube is
rearrangeable for \(N\le 8\). With \(N=2^p\), this is the \(p\le3\)
shortest-routing result. The explicit modern interpretation as pairwise
directed-arc-disjoint shortest paths remains verified through the published
Baudon–Fertin–Havel attribution, not by inspection of Szymanski's proof.
Accordingly, any contract item requiring primary-text verification, including
the slack-six theorem's source premise, remains source-pending.
