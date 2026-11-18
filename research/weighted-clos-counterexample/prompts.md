# Coordinator and solver prompts

## Discovery prompt

Find current open problems in distributed systems or theoretical computer
science whose negation has a finite, explicit, independently checkable witness.
For each candidate, preserve the exact primary-source quantifiers, verify current
open status, and reject variants that require asymptotic algorithms or lower
bounds rather than one finite object.

## Solver kickoff

Act as the primary mathematical researcher. Work against `contract.md`, not a
remembered version of weighted edge colouring.

Begin with at least three incompatible approach families:

1. exact rational CEGAR synthesis on fixed small bipartite multigraphs at
   \(n=3\), asking whether five global colours suffice;
2. bounded-denominator exhaustive or symmetry-reduced search;
3. a structural construction through local conflict systems or a
   minimal-counterexample analysis.

For each family, state its first falsifiable lemma or construction target, run a
small counterexample test, and retain a reproducible artifact. A failed heuristic
or an `unknown` solver result is not evidence of non-colourability. Any candidate
must be reconstructed from the contract and independently verified.
