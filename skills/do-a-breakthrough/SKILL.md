---
name: do-a-breakthrough
description: Conduct rigorous, long-horizon AI-assisted research on open problems in mathematics or theoretical computer science. Use when a user wants to select, prove, disprove, find a counterexample to, or make meaningful progress on an open conjecture through exact contracts, finite witness search, invariant mining, computation, proof repair, and independent verification.
---

# Do a Breakthrough

Run an artifact-first research program. Optimize for a correct, checkable result,
not for a dramatic answer. A claimed breakthrough remains a candidate until its
exact statement, dependencies, proof, computation, and scope survive independent
checking.

Read [references/research-playbook.md](references/research-playbook.md) completely
before starting. Use its problem-selection scorecard, counterexample protocol,
gates, theorem-conflict procedure, nudge ladder, audit stack, future-model
protocol, and handoff format.

## Set expectations and scope

- Tell the user that no model, prompt, or amount of compute guarantees a
  breakthrough.
- Explain that strong models can fabricate citations, silently change variants,
  overgeneralize finite evidence, and produce persuasive invalid proofs.
- Require expert review before public claims, submission, or attribution of
  novelty. Formal verification helps only after the encoded statement and
  dependencies are audited.
- State the available time, token, and compute budget when the user supplies one.
  Otherwise work in bounded waves and record what each wave consumed.
- Make the process inspectable without specialist training: define notation,
  explain the mechanism in plain language, and identify what remains unproved.

## Create a durable research workspace

Before deep work, establish a problem-local record. Prefer:

```text
research/<problem-slug>/
  README.md
  contract.md
  variant-matrix.md
  sources.md
  ledger.md
  prompts.md
  quarantine/
  notes/
  audits/
  code/
  results/<run-id>/
  handoff.md
```

- Record model/version, reasoning mode, prompts, dates, runtime, seeds, tools,
  human interventions, and environment versions.
- Treat chat messages as transient. A result does not exist until its exact
  statement and evidence are written to the record.
- Check whether the research directory is ignored, temporary, or untracked. Warn
  the user and export a portable bundle before handoff if the record would not
  survive a fresh clone or future model session.
- Give concurrent workers disjoint file ownership. Never let two runs overwrite
  the same result file.

## Lock the problem before solving it

Literature and source work comes first. Do not begin conjecture search until the
solution contract is explicit.

1. If the user gives an area rather than a problem, build a slate from explicit
   open-problem sections, current primary papers, and authoritative problem lists.
   Do not select from model memory or perceived fame.
2. Find the exact statement and its date, definitions, quantifiers, parameter
   ranges, conventions, and variants.
3. Build a variant matrix. Separate strong from weak forms, directed from
   undirected conventions, exact from asymptotic claims, and full from partial
   requests.
4. Check current literature, authoritative problem lists, synonyms, equivalent
   formulations, citation trails, known small cases, and known counterexamples.
5. Record source quality honestly:
   - `primary-verified`: original statement or proof inspected;
   - `corroborated`: exact result reported by an authoritative secondary source;
   - `source-pending`: access or provenance remains incomplete.
6. Do not let unavailable primary text halt mathematically valid work. Continue
   with the best available source, but keep provenance status separate from
   mathematical correctness.

Apply both gates:

- **Impact floor:** a resolution should correct, complete, or materially sharpen
  credible published work. Ease alone does not make a problem worth solving.
- **Tractability ceiling:** the first decisive experiment or lemma must fit the
  available budget and yield a compact artifact a fresh reviewer can check.

Prefer a narrow seam between known positive and negative cases, such as multiple
sources next to a single-source theorem, one fault next to a many-fault
counterexample, or one missing boundary case in a classification. Score finalists
for source confidence, worth, semantic precision, finite-certificate potential,
independent checkability, calibration anchors, and novelty-search cost. State why
the winner dominates the runner-up.

Deprioritize problems that cannot be stated precisely, have no checkable artifact,
are arbitrary generated conjectures with no impact, or hide several comparably
hard conjectures behind one sentence.

## Write the solution contract

The contract must contain:

- the original statement and a normalized formal statement;
- the formal negation with quantifiers reversed correctly;
- exact affirmative and negative completion criteria;
- every convention, state variable, and boundary case;
- variant exclusions for nearby models that look equivalent but are not;
- allowed external theorems with exact hypotheses;
- results that do not count, including special cases, finite samples, timeouts,
  conditional theorems, asymptotics when exactness is required, and reductions to
  theorem-strength missing lemmas;
- verification obligations for proof, computation, formalization, and novelty.

Audit the contract against the sources before research. Repair every altered
quantifier, domain, direction, capacity convention, or fixed-point rule.

For a dynamical, delayed, randomized, asynchronous, or distributed process, define
a **Markov-complete state**. Ask: could two executions agree on the recorded state
but evolve differently next? If yes, include the missing queues, in-transit
messages, residual timers, multiplicities, orientations, scheduler state, or
random choices. Repetition of a projected state is not a periodicity certificate.

## Use a multi-axis claim ledger

Do not compress all uncertainty into one label. Every material claim must record:

- exact statement and scope;
- dependencies and where each is used;
- mathematical status: `conjectured`, `tested`, `proved`, `refuted`, or
  `blocked`;
- verification status: `unaudited`, `hostile-audited`,
  `independently-computed`, `formalized`, or `expert-reviewed`;
- source status: `primary-verified`, `corroborated`, or `source-pending`;
- novelty status: `unchecked`, `targeted-search`, `no-prior-art-found`, or
  `externally-confirmed`;
- counterexamples attempted, evidence, and first unresolved step.

Keep raw solver claims in `quarantine/`. Promote a claim to the canonical ledger
only after a separate audit of the frozen statement and artifact. A coordinator
must not paraphrase an unreviewed solver message into a theorem.

## Calibrate before open-ended search

Build a small test corpus from the literature before trusting the pipeline:

1. reproduce known positive cases;
2. reproduce at least one known negative or failure case when available;
3. test empty, minimal, equality, parity, orientation, and degenerate cases;
4. prove the search encoding sound and complete for the intended statement;
5. verify stored witnesses with a checker that does not import the search
   implementation.

If a known case does not reproduce, stop and resolve the convention, source, or
encoding mismatch. Do not search novel territory with an uncalibrated pipeline.

## Run a counterexample-first campaign when the negation is finite

When one finite object, trace, or exact computation refutes the statement,
counterexample search is a primary strategy, not a fallback after failed proof
attempts.

1. Freeze the mathematical specification before coding: legal-instance validator,
   complete-state encoding, transition or calculation rule, and exact violation
   predicate.
2. Search the smallest legal instances first. Vary distinguished vertices, source
   sets, orientations, weights, and boundary parameters. Use symmetry reduction
   only if its completeness is justified.
3. Save the complete witness and replayable trace, not merely a search hit or cycle
   length. Minimize it after discovery.
4. Convert the hit into a self-contained finite certificate that checks every
   hypothesis and demonstrates the exact failed conclusion.
5. Audit it by hand, reimplement from the written specification, assert the exact
   trace, and use metamorphic checks such as relabeling or reversal.
6. Keep code as supporting evidence. The proof should explain why the explicit
   certificate is decisive without asking the reader to trust the search.

For a deterministic finite-state process, the same nonempty Markov-complete state
occurring at two distinct times implies a periodic nonterminating execution.
State the determinism step explicitly.

## Treat conflict with a published theorem as a diagnostic

When a candidate contradicts a published theorem:

1. freeze the candidate and recheck the theorem statement, hypotheses, timing, and
   model against the primary source;
2. reproduce a published example or theorem boundary to calibrate semantics;
3. construct the smallest theorem-specific instance and an independent trace;
4. inspect the proof for the first assertion falsified by that instance, including
   claimed invariants, equivalence relations, transitivity, reductions, and hidden
   closure assumptions;
5. keep the direct counterexample logically separate from the proof audit;
6. if the conflict remains, ask the authors or a specialist targeted questions.

Do not discard a valid-looking witness merely because a theorem says it cannot
exist. Do not announce an error merely because one simulator disagrees.

## Coordinate roles and artifacts

Use distinct logical roles when resources permit:

- **Coordinator:** owns the contract, accepted ledger, budgets, and synthesis.
- **Explorer/solver:** pursues one precise mechanism and writes proof fragments or
  witnesses.
- **Falsifier:** attacks lemmas and searches small or degenerate counterexamples.
- **Computational verifier:** audits encodings, certificates, search completeness,
  and denominators.
- **Source auditor:** checks theorem statements, hypotheses, variants, and
  provenance.
- **Integrator:** updates summaries only from accepted, audited claims.

Give each role one bounded objective, acceptance criteria, file ownership, and a
required artifact. Require checkpoint writes after each meaningful lemma or run,
not only at the end. Freeze candidate artifacts before audit.

When only one model is available, use separate cold passes: solve, discard the
persuasive posture, reconstruct the claim from the contract, then audit it as if
written by an adversary. This is weaker than independent review and must be
labeled accordingly.

## Run breadth waves, then depth waves

Do not keep many routes alive indefinitely.

1. **Breadth:** launch three to five genuinely incompatible families when the
   problem permits: constructive, extremal, algebraic, probabilistic,
   minimal-counterexample, dual, or computational. For a strongly
   counterexample-shaped problem, one exhaustive search plus independent semantic
   and proof-audit formulations may be better than three superficial proof routes.
2. **Falsify early:** for every route, name the first falsifiable lemma and test
   it on the smallest and most hostile instances.
3. **Diagnose:** classify failure as false lemma, missing lemma, quantifier error,
   boundary case, ambiguity, illicit assumption, circularity, theorem-strength
   reduction, computational gap, source gap, or resource limit.
4. **Score:** rank surviving routes by distance to a complete result,
   falsifiability, auditability, novelty of mechanism, and expected artifact
   value.
5. **Depth:** pursue at most the best one or two mechanisms until they yield a
   proof fragment, witness, counterexample, or exact blocker.
6. **Mine structure:** ask what invariant explains the experiments. Convert data
   into a parameter, decomposition, closure lemma, or obstruction whenever
   possible.
7. **Audit and freeze:** hostile-check the result, repair it exactly, and update
   the ledger before beginning another wave.

Useful general tactics include:

- parameterizing distance from a known extremal object by slack or defect;
- counting how a small defect localizes to few coordinates, blocks, supports, or
  fibers;
- symmetry reduction and canonical orbit representatives;
- closure under products, fibers, lifts, or decomposition;
- minimal-counterexample structure and equality-case rigidity;
- LP or metric duals that yield compact negative certificates;
- extracting human lemmas from recurring solver witnesses;
- explicitly distinguishing a counterexample to a method from a counterexample
  to the conjecture.

## Enforce computational and formal discipline

- Write every run to a unique immutable directory. Use atomic writes and a
  manifest with input hashes, command, seed, timeout, versions, and status.
- Preserve original outcomes. A later witness may supersede an `unknown`, but it
  must not rewrite the historical run.
- Report `sat`, `unsat`, `unknown`, timeout, crash, and heuristic failure
  separately. A timeout is not negative evidence.
- State the denominator for every count: exact population, dimension, mode,
  symmetry quotient, structured sample, or random sample.
- Separate search from checking. An independent verifier should reconstruct the
  object and defining conditions from the specification, not call the original
  solver.
- For stateful processes, include every hidden or in-transit component in the
  stored state. Assert the expected witness trace, not only the searcher's generic
  cycle or violation flag.
- For SAT, retain and independently check the witness. For UNSAT, require a
  checkable proof/certificate or an independently justified exhaustive search and
  preferably a materially different formulation.
- Prefer exact arithmetic. Label floating-point, heuristic, and bounded-search
  evidence explicitly.
- For formal proof, lock the theorem statement first; audit axioms, admitted
  facts, generated bindings, and the correspondence between the formal theorem
  and the contract. Compilation alone is not mathematical validation.

## Audit dependencies and novelty separately

For every external theorem, keep a dependency card containing its exact statement,
hypotheses, source tier, and the line where it enters the proof. If the original
source is inaccessible, use an authoritative corroboration and mark
`source-pending`; do not downgrade a sound local argument to “mere computation.”

Run novelty searches both before and after the mathematical work. Search the exact
statement, equivalent formulations, mechanism, construction, and proper subclass.
“No result found” means only that the recorded search found none. Novelty requires
expert confirmation.

## Prepare external verification

When a candidate survives internal audit, prepare an expert-review packet:

- a short self-contained note with the exact statement and model;
- the smallest witness, diagram, state table, or algebraic certificate;
- a proof that the certificate implies the claimed conclusion;
- reproducible checking code and calibration results when computation was used;
- a separate section for any published-proof diagnosis;
- a candid AI-assistance disclosure;
- precise questions about semantics, correctness, prior art, and corrections.

Use cautious language such as “candidate counterexample” and “appears to” until
external review. Track author or expert responses as new evidence without silently
upgrading correctness or novelty.

## Prepare for stronger future models

At the end of every serious run, create a compact, model-agnostic research bundle:

```text
contract.md
variant-matrix.md
accepted-ledger.md
quarantined-claims.md
failed-routes.md
frontier-obligations.md
test-corpus/
certificates/
environment.md
manifest.sha256
```

When a substantially stronger model arrives:

1. give one instance only the contract and sources for a **blind restart**;
2. give another pass the accepted ledger and ask it first to falsify the strongest
   accepted lemma;
3. require reproduction of one known positive case, one known negative case, and
   one stored certificate before new claims are trusted;
4. assign one exact frontier obligation, not the entire transcript;
5. compare the blind and informed mechanisms before synthesis;
6. record model/version, reasoning mode, prompts, and every inherited assumption.

Do not let a new model inherit today’s blocked routes as truth. The ledger is
evidence to audit, not doctrine.

## Stop and close out honestly

Continue while budget remains and a materially new mechanism, exact experiment,
or audit exists. Stop when:

- a candidate satisfies the full contract and survives independent audit;
- the agreed budget is exhausted;
- all live routes reduce to catalogued theorem-strength blockers;
- required sources, tools, compute, or expertise are unavailable.

Before final reporting, run a closeout audit:

- reconcile every summary sentence and number with the canonical ledger;
- remove stale `pending` labels and quarantine unaudited claims;
- distinguish original run results from later corrections;
- verify that “method refuted,” “proper subclass proved,” and “full conjecture
  solved” are never conflated;
- export the record if its directory is ignored or ephemeral.

On success, produce a proof or counterexample package, exact dependencies,
certificates, prompts, gap log, and expert-review checklist. On failure, produce
an honest blocked handoff. Never use completion pressure to fill a gap with prose.
