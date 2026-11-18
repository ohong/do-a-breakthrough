# Research ledger

Last updated: 2026-07-23

## Claim status

| Claim | Status | Evidence |
|---|---|---|
| Feige--Singh Conjecture 1.1 has the statement copied in `contract.md` | proved | ESA 2008 primary PDF, Conjecture 1.1 |
| The same multirate Clos statement was still called a popular conjecture in 2024 | proved | PODC 2024, §6 |
| No resolution was found through 2026-07-23 | tested | exact-title and equivalent-form web searches |
| The \(n=2\) case satisfies the conjectured three-colour bound | proved | Ngo--Vu 2003, \(m(2,r)=3\) |
| A finite \(n=3\) counterexample exists | conjectured | no witness found |
| Every pair-conflict graph at local parameter \(n\) is \((n+1)\)-colourable | proved | `notes/pair5-theory.md` |
| Every locally feasible \(\{3/5,2/5\}\) instance is five-colourable at \(n=3\) | proved | `notes/marked-b5-theory.md` |
| Any candidate emitted by search is correct | blocked | no candidate; verification machinery audited |
| Any correct candidate is novel | blocked | requires final construction-specific search and expert review |

## Approach-family registry

| ID | Family | Core mechanism | Next falsifiable claim | Artifact | Status | Blocker |
|---|---|---|---|---|---|---|
| A | Exact synthesis | CEGAR over rational weights and local three-bin packings for fixed bipartite multigraphs | Some topology admits locally 3-packable weights but no global 5-colouring | `code/search_n3.py`, `notes/n3-search.md` | tested | no topology/size bound |
| B | Discrete denominator search | Enumerate small rational weights with bounded denominators and test every global colouring | A richer finite alphabet contains an \(n=3\) obstruction | `code/search_discrete.py` | retired pilot | current implementation is only \(n=2\) |
| C | Pair-conflict construction | Force chromatic number six using pairwise overloads | A representable 6-chromatic conflict graph exists | `notes/pair5-theory.md` | refuted | all such graphs are \((n+1)\)-colourable |
| D | Fixed \(3/5,2/5\) construction | Encode heavy matchings and light degree-two colour classes | A marked bipartite graph has no five-colouring | `notes/marked-b5-theory.md` | refuted | factorization gives five colours universally |
| E | Minimal-counterexample theory | Use deletion saturation, density orientation, and bridge reductions | A bounded normal form supports complete search | `notes/higher-order-theory.md` | proved / blocked | no finite degree or weight-alphabet bound |
| F | Hostile verification | Differentially audit exact master, checker, block clauses, and backtracker | Every emitted candidate is independently rejected or certified | `notes/n3-verification-audit.md` | tested | no candidate; Z3 UNSAT lacks proof artifacts |

## Initial bounds and observations

- \(n=1\) is immediate: every vertex's incident edges fit together in one unit
  bin, so giving every edge the sole colour is proper.
- Ngo--Vu prove \(n=2\), so a counterexample cannot occur there.
- At \(n=3\), their published bound is six colours; Chung--Ross predicts five.
- Ngo--Vu also prove \(m(n,2)\le\lceil 3n/2\rceil\). Hence an \(n=3\)
  counterexample needs at least three nonisolated vertices on each side.
- If all weights are at most \(1/2\), Feige--Singh report that the stronger
  total-weight conjecture is known. A witness must mix weights above and below
  \(1/2\).
- If all weights are strictly above \(1/2\), the conjecture follows from
  König's bipartite edge-colouring theorem. Again, a witness must be mixed.
- A non-bipartite obstruction at \(n=2\) is known: the Petersen graph with all
  weights \(2/3\). It is a mechanism clue, not a valid witness.

## Gap log

1. **Open-status gap:** bibliographic search cannot exclude unpublished work.
2. **Frontier gap:** no authoritative source was found settling the isolated
   five-colour \(n=3\) case.
3. **Search-completeness gap:** the \(n=3\) exact search covers a complete
   simple \(3\times3\) topology frontier plus bounded multigraph samples, but
   there is no theorem placing a minimum counterexample in that frontier.
4. **Certificate gap:** a solver's `unsat` response alone will not be accepted
   as a counterexample certificate.
5. **Mechanism gap:** pairwise conflicts and the \(\{3/5,2/5\}\) alphabet are
   now eliminated. Any counterexample must use overloaded triples or larger
   sets with a richer weight alphabet.

## Retained prompts and outputs

The coordinator/solver prompts and compact results belong in `prompts.md`.
