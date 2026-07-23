---
name: do-a-breakthrough
description: Conduct rigorous, long-horizon AI-assisted research on open or unsolved mathematics problems. Use when a user wants to investigate, prove, disprove, find a counterexample to, or make meaningful progress on an open conjecture, especially when coordinating a stronger solver model through repeated nudges, competing approaches, counterexample search, proof repair, and adversarial verification.
---

# Do a Breakthrough

Run a persistent mathematical research program. Treat a claimed breakthrough as a
hypothesis until it survives independent checking.

Read [references/research-playbook.md](references/research-playbook.md) before
starting. Use its contract, prompts, nudge ladder, audit checklist, and handoff
template.

## Set expectations

- Tell the user that no prompt or model guarantees a breakthrough.
- Explain that frontier models can fabricate citations, overlook edge cases, and
  produce persuasive but invalid proofs.
- Make the process usable without advanced training: define unfamiliar notation,
  translate each major claim into plain language, and state what the user should
  inspect next.
- Require expert review before public claims, submission, or attribution of a new
  result. Prefer formal verification when practical, but do not confuse a broken
  or assumption-heavy formalization with proof.

## Choose and verify the problem

1. Start from the exact primary-source statement. Record definitions, quantifiers,
   parameter ranges, conventions, date, source, and known partial results.
2. Check current literature and authoritative problem lists. Determine whether the
   problem remains open, has equivalent formulations, or has silently different
   variants. Never rely on the user's or a model's memory alone.
3. Prefer bounded, checkable problems with concrete objects, finite or structural
   witnesses, accessible definitions, and clear verification paths.
4. Deprioritize problems whose resolution would immediately settle several famous
   conjectures, require large missing theories, or cannot be stated precisely from
   available sources. Explain why.
5. Never assume a proof, disproof, or novel result exists. Permit rediscovery,
   partial progress, or an honest blocked result.

## Write the solution contract

Do not search until the contract is explicit. Include:

- the statement verbatim and a normalized formal version;
- what a complete affirmative solution must establish;
- what a complete negative solution or counterexample must exhibit and verify;
- all edge cases, conventions, and allowed dependencies;
- weaker results that do **not** count, such as finite evidence, asymptotics where
  exactness is required, a special case, a conditional theorem, or a reduction to
  another open statement;
- a verification plan for every claim and any computational certificate;
- a novelty check that is separate from correctness.

Ask a solver to compare the contract against the source statement before research.
Repair any changed quantifier, domain, or definition.

## Establish the research record

Keep a durable ledger containing:

- the contract and sources;
- an approach-family registry;
- every useful lemma, witness, failed route, and counterexample;
- assumptions and dependencies;
- solver prompts and outputs;
- verification status and unresolved gaps;
- a current best artifact that a fresh reviewer can inspect.

Label claims `conjectured`, `tested`, `proved`, `refuted`, or `blocked`. Do not
upgrade status because a model sounds confident.

## Coordinate the models

Assign two logical roles:

- **Coordinator/nudger:** maintain the record, diagnose failures, choose the next
  nudge, protect the contract, and demand artifacts. This can be a smaller or
  cheaper model.
- **Solver:** use the strongest available reasoning model for deep search, proof
  construction, and repair.

Give the solver the contract, relevant ledger excerpts, and one precise objective.
Do not repeatedly resend an unbounded transcript. The coordinator must challenge
and redirect the solver, not merely summarize it.

When only one model is available, alternate roles in separate passes: first solve,
then reset posture and audit as a hostile verifier, then resume from a compact
ledger. State that this is weaker than independent review.

## Run the continual research loop

Repeat until a stop condition applies:

1. **Attempt:** launch several genuinely different approach families. Keep at
   least three viable families when the problem permits, such as constructive,
   extremal, algebraic, probabilistic, computational, or minimal-counterexample
   routes.
2. **Failure:** force each route to name its first unsupported step. Reject vague
   progress reports and optimism without a proof fragment, witness, computation,
   or falsifiable lemma.
3. **Diagnosis:** classify the failure as false lemma, missing lemma, quantifier
   error, boundary case, illicit assumption, computational gap, circularity,
   theorem-strength reduction, or resource limit.
4. **New approach:** repair only local gaps. If the gap is central, switch
   mechanisms or approach families. Keep incompatible routes independent until
   they produce artifacts worth synthesizing.
5. **Proof draft:** assemble a self-contained argument or explicit counterexample.
   List every dependency and verification obligation.
6. **Adversarial audit:** ask a fresh context or model to disprove each lemma,
   search edge cases, reconstruct computations, detect circularity, and compare
   every quantifier with the contract.
7. **Repair:** patch the exact gap, weaken the claim honestly, or retire the route.
   Update the ledger and begin another wave.

Use the playbook's nudge ladder after stalls. Escalate from a concrete next
deliverable, to structural diagnosis, to an incompatible restart, to
unconditional completion pressure, and finally to hostile audit and proof repair.
Never use encouragement as a substitute for a diagnosed next action.

## Enforce research discipline

- Mark a route `blocked` when its main missing lemma is comparable in strength to
  the original problem. Reopen it only with a materially new mechanism.
- Reject circular arguments, restatements, and chains ending in an unproved
  equivalent claim.
- Treat computation as evidence unless exhaustive coverage and the checking code
  or certificate are independently verified, or the computation is converted
  into a proof.
- Search for counterexamples to every new lemma before building on it. Test the
  smallest cases, boundary values, degenerate objects, and symmetry assumptions.
- Verify an explicit counterexample by independently checking every defining
  property and the claimed violation. Prefer two implementations using different
  formulations.
- Verify a proof line by line in a fresh context. Check cited theorems against
  primary sources and confirm their hypotheses exactly.
- Separate correctness from novelty. A correct result may already be known.
- Preserve negative results and failed approaches. They prevent repeated dead ends
  and make the final handoff useful.

## Stop honestly

Do not stop merely because one search wave failed or the solver asks to give up.
Continue while there is budget and a concrete new experiment, mechanism, or audit.

Stop when one of these holds:

- a candidate solution satisfies the contract and survives independent audit;
- the agreed time, token, or compute budget is exhausted;
- all live routes reduce to catalogued blocked lemmas and no materially new route
  remains;
- required sources, computation, tools, or expertise are unavailable.

On success, produce a proof or counterexample package, verification artifacts,
exact prompts, a gap log, and an expert-review checklist. On failure, produce a
blocked-research handoff using the playbook template. Never label an unaudited
candidate a solution or announce novelty without a literature check.
