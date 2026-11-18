# Claim ledger

Search and verification date: 2026-07-23

| ID | Claim | Status | Evidence | Remaining risk |
|---|---|---|---|---|
| C1 | The primary paper explicitly poses the multi-source, bipartite, one-fixed-delay termination question | source-checked | Publisher full text, Section 5, Open Problem 2 | none |
| C2 | The five-node instance satisfies the problem's graph, source, and delay hypotheses | verified | direct graph check; two independent audits | hidden source-model convention |
| C3 | The full state in round 5 equals the full state in round 10 | verified | manual table; three separately implemented transitions | implementation correlation |
| C4 | The repeated nonempty state proves nontermination | proved from determinism | normalized model and transition rule | none if C2-C3 hold |
| C5 | The simulator uses the paper's timing/tick semantics | strongly verified | exact reproduction of the paper's Figure 6 repetition at rounds 5 and 13 | figures may omit an unstated convention |
| C6 | No prior correction or resolution was public by 2026-07-23 | provisional | exact-title, theorem, problem-text, citation, author, and errata searches; OpenAlex listed three citing works, all inspected | unpublished or poorly indexed work |
| C7 | A four-cycle with three sources refutes Theorem 4.3 | verified candidate | two independent state tables | expert review required because it contradicts a peer-reviewed theorem |
| C8 | Theorem 4.3's proof incorrectly asserts transitivity of `~` | verified candidate | explicit three-source calculation in expanded cycle | another part of the proof might repair the argument |
| C9 | Five vertices are minimal for a two-source counterexample | computational evidence only | independent enumeration of connected labelled bipartite graphs through five vertices for delay two | no general proof over all delays |

## Overall status

The direct counterexample is internally verified and appears to answer Open
Problem 2 negatively. Novelty and the interpretation of the peer-reviewed model
still require external expert review.
