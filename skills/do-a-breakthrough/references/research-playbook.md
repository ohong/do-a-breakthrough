# Research playbook

Use this playbook to turn a long model conversation into a reproducible research
program in mathematics or theoretical computer science. Replace bracketed text
with problem-specific content. The canonical ledger, not the latest confident
message, determines what is accepted.

## 0. Non-negotiable invariant

Keep four questions separate:

1. **Is the mathematical statement correct?**
2. **Has the argument or certificate been independently verified?**
3. **Are its external dependencies and sources established?**
4. **Is the result novel?**

A claim can be mathematically sound but source-pending or already known. A
machine-checked witness can be valid but cover only a finite sample. Never collapse
these distinctions into “solved.”

## 1. Workspace bootstrap

Create a durable directory before research:

```text
research/<slug>/
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
  test-corpus/
  results/<YYYY-MM-DD>-<method>-<run-id>/
  handoff.md
```

Record this run header:

```text
Problem:
Run ID:
Date and timezone:
Coordinator model/version/reasoning mode:
Other models and roles:
Tools and versions:
Time/token/compute budget:
Workspace persistence:
Git status and unrelated changes:
```

If `research/` is ignored, temporary, or excluded from a packaged skill, say so.
Plan an export bundle before closeout.

Each computational run gets a unique directory containing:

```text
manifest.json
input.*
stdout.log
stderr.log
result.json
certificate.*
checksums.sha256
```

Never reuse a result filename across simultaneous or later runs.

## 2. Problem intake and selection

### Intake template

```text
Problem title:
Primary source and date:
Authoritative secondary sources:
Exact original statement:
Formal negation:
Definitions and conventions:
Statement shape (universal, existential, bound, termination, classification):
Known variants:
Known positive cases:
Known negative cases:
Narrow seam or boundary mechanism:
Equivalent formulations, if verified:
Current open-status evidence and search date:
Expected proof or counterexample artifact:
Independent verification path:
Reasons this is tractable enough:
Reasons to defer:
```

### Variant matrix

Use a table before attempting a proof:

| Variant | Exact difference | Known status | Source tier | In scope? |
|---|---|---|---|---|
| Ordinary | [...] | open | primary-verified | yes |
| Strong | adds [...] | false | corroborated | no |
| Partial | drops [...] | known | source-pending | no |

Explicitly compare:

- all versus some instances;
- exact versus asymptotic;
- directed versus undirected;
- edge-, arc-, or vertex-disjoint;
- shortest versus unrestricted;
- integral versus fractional;
- full permutation versus partial or repeated requests;
- finite dimension versus all dimensions.

### Selection score

Build a slate before committing. Five serious, source-checked candidates are more
useful than fifty remembered titles. Score each criterion from `0` to `3`, and
explain any score that determines the winner.

| Criterion | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Primary-source confidence | remembered or secondary only | traceable but ambiguous | exact source, status partly checked | exact statement plus current status search |
| Worth | arbitrary or generated | isolated curiosity | meaningful published question | resolves or corrects an important boundary in credible work |
| Certificate potential | no finite check | large or unclear artifact | bounded witness or proof fragment | tiny exact witness, trace, or local contradiction |
| Semantic precision | ambiguous model | unresolved conventions | precise after reconstruction | precise with a published calibration example |
| Searchability | no bounded experiment | large uncontrolled search | smallest cases enumerable | exhaustive minimal search practical |
| Independent verification | only original solver | one implementation | hand audit or second formulation | short certificate plus two independent checks |
| Novelty-search cost | diffuse folklore | large literature | focused citation graph | explicit recent open problem with identifiable authors |
| Boundary leverage | isolated statement | weak heuristic | adjacent partial result | narrow seam between known positive and negative cases |

Apply both gates:

- **Impact floor:** Would a correct resolution teach a specialist something or
  repair a credible theorem, classification, or algorithmic boundary?
- **Tractability ceiling:** Can the first decisive experiment or lemma be run and
  checked within the available budget?

Do not compensate for zero worth with easy verification, or for zero
verifiability with fame. State why the winner dominates the runner-up.

### Statement-shape routing

| Statement shape | Typical decisive certificate | Good first campaign |
|---|---|---|
| Universal finite/combinatorial claim | one legal object violating the conclusion | enumerate smallest objects, then minimize |
| Termination of a deterministic process | two equal nonempty complete states | finite-state cycle search |
| Claimed upper or lower bound | one exact configuration outside the bound | extremal construction search |
| Claimed invariant/equivalence relation | one transition or triple violating closure | property-based proof audit |
| Existential construction | one object meeting every constraint | constructive or constraint search |
| Asymptotic theorem | a construction family or scalable proof mechanism | usually defer unless such a mechanism is visible |

Prefer an unfilled cell next to understood cells. Examples include one source
versus multiple sources, one defect versus several defects, a missing endpoint,
or a proof relation whose closure was asserted but not tested. For each finalist,
name the mechanism that could make the open cell behave differently. If no
mechanism is visible, the problem is not yet selected.

## 3. Exact solution contract

```text
Investigate the following statement without assuming it is true, false, open, or
novel.

[Original statement]

Normalized formal statement:
[...]

Formal negation:
[...]

A complete affirmative result must:
1. [...]

A complete negative result must:
1. exhibit [...];
2. verify every hypothesis [...];
3. prove the exact negation [...];
4. supply a checkable certificate if computational.

The following do not count:
- finitely many cases without a completeness theorem;
- a special, asymptotic, weakened, or conditional result;
- a timeout, crash, or failed heuristic search;
- assuming the target under equivalent language;
- reducing to an unproved statement of comparable strength;
- citing a theorem without matching its hypotheses;
- a formal proof of a materially different statement.

Edge cases and conventions:
- [...]

State sufficiency test, if the problem is dynamical:
- [Could two executions share the recorded state but have different successors?]
- [Queues, messages in transit, residual timers, scheduler state, multiplicities,
  orientations, or random choices that must be included.]

Semantic calibration:
- [Published example, figure, or boundary theorem and the exact behavior to
  reproduce before novel search.]

Variant exclusions:
- [Nearby models, reductions, or substitutions that do not count.]

Allowed dependencies:
- [Exact theorem, source tier, hypotheses, intended use]

Verification obligations:
- mathematical [...]
- computational [...]
- source [...]
- novelty [...]

Before research, compare this contract with the sources and report every changed
quantifier, definition, domain, orientation, convention, and parameter endpoint.
```

Define affirmative and negative criteria even if one truth value looks more
likely.

## 4. Claim cards, quarantine, and promotion

Every material claim begins as a card in `quarantine/`:

```text
Claim ID:
Exact statement:
Scope:
Originating model/run:
Dependencies:
Proof or evidence:
Small cases tested:
Counterexamples attempted:
Mathematical status:
Verification status:
Source status:
Novelty status:
First unresolved step:
Artifact paths and hashes:
```

Allowed status values:

```text
Mathematical: conjectured | tested | proved | refuted | blocked
Verification: unaudited | hostile-audited | independently-computed |
              formalized | expert-reviewed
Source: primary-verified | corroborated | source-pending
Novelty: unchecked | targeted-search | no-prior-art-found |
         externally-confirmed
```

Promotion gate:

1. freeze the exact claim and evidence;
2. assign a verifier who did not construct it;
3. audit the statement, dependencies, edge cases, and scope;
4. record gaps and repairs;
5. reconstruct the repaired claim from scratch;
6. only then copy it into `ledger.md`.

The accepted ledger should link to raw cards but never silently inherit their
status. Claims mentioned only in chat remain unaccepted.

## 5. Calibration gate

Before searching novel instances, build `test-corpus/`:

```text
known-positive/
known-negative/
boundary/
convention/
malformed/
```

Required checks:

- reproduce the smallest known positive cases;
- reproduce a known negative or restricted-variant failure when available;
- test empty, singleton, equality, parity, orientation, and maximal cases;
- inject malformed objects and confirm rejection;
- prove the encoding is sound and complete for the contract;
- validate witnesses with a checker independent of the search code.

Calibration report:

```text
Known result:
Source:
Expected outcome:
Observed outcome:
Artifact:
Mismatch or caveat:
Gate status: pass | fail | source-pending
```

Do not proceed past a failed calibration gate.

## 5A. Counterexample-first protocol

Use this protocol when the formal negation can be witnessed by one finite object,
finite execution, exact computation, or local proof defect.

### Freeze the semantics before coding

Write four functions on paper:

```text
is_legal(instance) -> verifies every hypothesis
initial_state(instance) -> complete state, not a convenient projection
step(instance, state) -> unique successor or precisely defined transition set
violates(instance, trace_or_object) -> exact negated conclusion
```

For a dynamical process, apply the successor test:

```text
If two runs agree on my stored state, must their next states agree?
```

If not, add the missing information. Common omissions are in-transit messages,
residual delays, queues, multiplicities, orientations, adversary choices, and
random seeds. Do not replace a delayed channel with an ordinary subdivision
vertex, an asynchronous schedule with a synchronous one, or a multiset process
with a set process unless the source proves those models equivalent.

### Search the smallest legal instances

1. Enumerate size in increasing order.
2. Within a size, enumerate distinguished vertices, source sets, edge labels,
   weights, orientations, and boundary parameters.
3. Validate each instance independently of the generator.
4. Search the decisive predicate, not a proxy. For nontermination, compare
   complete states including hidden transit state.
5. Save the first witness and enough trace to replay it.
6. Continue briefly for relabelings or nearby witnesses that expose the mechanism,
   then minimize.

Symmetry reduction is optional. If used, justify that it cannot remove the only
legal placement of distinguished structure.

### Turn the search hit into a certificate

```text
Instance:
Every hypothesis checked:
Complete state or calculation table:
Two equal states or exact violated inequality:
Why this implies the formal negation:
Minimality claim, if any:
```

For a deterministic process:

```text
S_i = S_j, i < j, and S_i is nonempty
the complete-state update is deterministic
therefore S_{i+k} = S_{j+k} for all k >= 0
```

The search locates the certificate. The certificate, not the search log, is the
mathematical proof.

### Cross-check independently

- Audit the trace by hand.
- Reimplement from the written specification rather than translating the first
  program.
- Assert every expected state or calculation, not only a generic cycle detector
  or violation flag.
- Check object properties separately from the dynamics.
- Use relabeling, reversal, dual encoding, or another metamorphic check.
- Keep arithmetic exact and outputs deterministically ordered.

Two implementations that share the same mistaken state definition are not
independent. The calibration gate guards against that shared error.

### Transferable lesson from delayed flooding

A useful pattern is:

1. select an explicit open cell between a positive theorem and a nearby negative
   example;
2. model the full state, including information invisible at original vertices;
3. reproduce the source paper's published repeated state before searching;
4. find and minimize a finite periodic witness;
5. write the full state table so the proof is checkable without code;
6. if the witness collides with another theorem, audit that theorem separately.

The specific candidate may still await expert review. The workflow lesson does
not depend on its eventual acceptance.

## 5B. Published-theorem conflict protocol

When a candidate contradicts a published theorem, neither discard it nor announce
a correction.

1. Freeze the candidate, exact trace, code, and hashes.
2. Recheck the theorem statement, hypotheses, timing, model, and nearby definitions
   in the primary source.
3. Re-run the calibration corpus, especially a published example using the same
   convention.
4. Build the smallest theorem-specific instance and reproduce it by hand and with
   an independent formulation.
5. Find the first proof assertion falsified by the instance. Test claimed
   invariants, equivalence relations, transitivity steps, reductions, midpoint
   conditions, and hidden closure assumptions.
6. Keep two artifacts:
   - the direct counterexample certificate;
   - the proof audit explaining the suspected theorem defect.
7. Do not make the direct result depend on the proof diagnosis.
8. If any conflict remains, ask the authors or a specialist explicit questions
   about semantics, the trace, the proof step, and prior corrections.

Use cautious status language:

```text
candidate counterexample
internally reproduced
source-calibrated
apparent proof defect
not yet expert reviewed
```

## 6. Role packets

### Coordinator

```text
Own: contract, accepted ledger, budgets, integration, closeout.
Must not: promote an unaudited solver claim.
Next decision required:
```

### Explorer/solver

```text
Objective:
Why it matters:
Allowed assumptions:
First falsifiable claim:
Acceptance criteria:
Owned files:
Checkpoint cadence:
Stop condition:
Required artifact:
```

### Falsifier

```text
Assume [claim] is false.
Find the earliest invalid inference or smallest counterexample.
Test all boundary cases and ambiguous readings.
Return a numbered gap list and the minimal repair for each gap.
Do not edit the candidate artifact.
```

### Computational verifier

```text
Audit the specification-to-encoding correspondence.
Independently reconstruct certificates without importing search code.
Check population size, symmetry quotient, denominators, and run lineage.
Treat timeout/unknown as non-results.
```

### Source auditor

```text
Verify the exact external theorem and every hypothesis.
Distinguish original source, authoritative corroboration, and inaccessible text.
Search variant names and equivalent formulations.
Do not infer novelty from absence.
```

### Integrator

```text
Update summaries only from accepted ledger entries.
Reconcile counts with immutable results.
Remove stale statuses.
Never turn "method refuted" or "proper subclass proved" into a full result.
```

Give roles disjoint files. Freeze before audit. Require checkpoint writes so an
interrupted long run does not leave its only result in a final chat message.

## 7. Approach registry and wave protocol

Registry:

| ID | Family | Mechanism | First falsifiable claim | Quick test | Artifact | Status | Blocker |
|---|---|---|---|---|---|---|---|
| A | Constructive | [...] | A1 | [...] | notes/A.md | conjectured | |
| B | Counterexample | [...] | B1 | [...] | code/B.* | tested | |
| C | Dual/extremal | [...] | C1 | [...] | notes/C.md | conjectured | |

### Breadth wave

Start three to five incompatible routes. For each, force:

1. a mechanism;
2. the first falsifiable lemma;
3. the smallest hostile test;
4. a concrete artifact;
5. the condition under which the route becomes theorem-strength blocked.

### Route score

Score `0` to `2`:

```text
Distance to completion:
Falsifiability:
Auditability:
Novel mechanism:
Expected reusable artifact:
Total:
```

### Depth wave

Pursue only the best one or two routes. Stop a depth wave when it yields:

- a proof fragment with dependencies;
- an explicit witness;
- a counterexample to the current lemma;
- a reproducible exact experiment;
- or a precisely classified blocker.

After every wave, ask:

```text
What invariant explains the evidence?
Can a large object be localized to few coordinates, blocks, cycles, or fibers?
Is there a slack/defect parameter around a known extremal construction?
Can symmetry turn examples into finitely many canonical types?
Does an equality case force rigidity?
Can the computation be replaced by a closure or decomposition lemma?
Did we refute the statement, or only the chosen architecture?
```

## 8. Nudge ladder

Choose the lowest rung matching the stall. Every nudge demands an artifact.

### Rung 1: Continue to a checkpoint

```text
Continue only until you produce one proved lemma, explicit candidate, falsifying
example, or reproducible experiment. Write it to [owned path] before reporting.
State the first unresolved step exactly.
```

### Rung 2: Diagnose structure

```text
Pause local manipulation. Identify the invariant, obstruction, duality, or
decomposition controlling the failure. Classify the current gap and attack one
pivotal falsifiable claim.
```

### Rung 3: Mine the experiments

```text
Do not run more undirected random search. Group the existing witnesses by symmetry,
support, defect, equality pattern, or active coordinates. Propose the smallest
dimension-free lemma explaining them, then try to falsify it.
```

### Rung 4: Break the frame

```text
Retire the current mechanism. Start an incompatible route that does not assume the
blocked lemma or an equivalent statement. Reverse the likely truth value and test
the smallest degenerate cases first.
```

### Rung 5: Closure attempt

```text
Try to close every remaining gap. For each gap, either provide a proof/certificate
or mark it blocked with its exact strength. Do not bridge a gap with confidence,
analogy, or prose. If central, switch mechanisms immediately.
```

### Rung 6: Hostile verifier

```text
Assume the frozen candidate is wrong. Recopy its exact statement, then attack every
lemma, theorem hypothesis, boundary case, ambiguous term, count, and computational
claim. Return the earliest invalid inference and minimal repair.
```

### Rung 7: Reconstruct

```text
Repair the accepted gaps, then reconstruct the entire argument from the contract
without copying the old prose. Include dependency cards and a verification
obligation for every nontrivial step.
```

Completion pressure is allowed only as pressure to close or expose gaps. It is
never permission to assert that a gap is closed.

## 9. Computation protocol

### Search specification

```text
Object domain:
Exact property:
Encoding variables:
Complete-state sufficiency argument:
Soundness argument:
Completeness argument:
Symmetry reduction:
Population denominator:
Arithmetic mode:
Timeout policy:
Certificate format:
Independent checker:
Published calibration case:
Exact expected trace or certificate:
Metamorphic checks:
```

### Run manifest

```json
{
  "run_id": "...",
  "created_at": "...",
  "command": ["..."],
  "model_or_solver": "...",
  "versions": {},
  "seed": 0,
  "timeout_seconds": 0,
  "input_sha256": "...",
  "status": "sat|unsat|unknown|timeout|crash|inconclusive",
  "supersedes": null
}
```

Rules:

- Write to a new run directory, then atomically rename temporary outputs.
- Never overwrite a historical `unknown`; link a later witness with `supersedes`.
- Do not call heuristic exhaustion `unsat`.
- Store SAT witnesses and check every defining property.
- For UNSAT, retain a proof trace, certificate, exhaustive case manifest, or
  second independent formulation.
- Count populations independently from the search.
- Say “8 structured dimension-5 cases plus 76 lower-dimensional calibrations,”
  not “84 dimension-5 cases.”
- A verifier must not import the original solver module or trust redundant result
  metadata.

### Turning computation into mathematics

After a successful batch:

1. canonicalize witnesses under symmetries;
2. classify by cycle type, support, rank, slack, defect, or equality signature;
3. inspect which coordinates or constraints are actually active;
4. search for a closure theorem explaining lifted examples;
5. state and falsify the smallest dimension-free lemma;
6. keep the computation as regression evidence after the proof is found.

## 10. Proof and dependency audit

### Lemma audit

- Recopy the exact statement.
- Map every conclusion to a proof step.
- Try the weakest literal reading of ambiguous terms.
- Check endpoint, orientation, simplicity, disjointness, integrality, equality,
  empty, and minimal-size cases.
- Construct small counterexamples before trusting induction.
- Detect appeals to the target or an equivalent theorem-strength lemma.
- Distinguish a walk, trail, path, simple path, and shortest path.
- Distinguish a construction failing from the mathematical statement failing.

### Dependency card

```text
Theorem:
Exact statement:
Hypotheses:
Source:
Source status:
Where used:
Hypothesis-by-hypothesis match:
Fallback if source inaccessible:
```

If the original proof is inaccessible but a peer-reviewed source states the exact
result, mark the dependency `corroborated` or `source-pending`. Keep the local
mathematical argument’s status separate.

### Formalization audit

```text
Formal theorem statement:
Corresponding contract clause:
Definitions compared:
Axioms/imported theorems:
Admitted facts/sorries:
Generated code or bindings:
Kernel/compiler result:
Independent statement review:
```

A compiling proof of the wrong theorem is not a solution.

## 11. Audit stack

Run independent passes in this order:

1. **Contract audit:** statement, variants, conventions, negation.
2. **Source audit:** open status and dependency hypotheses.
3. **Mathematical audit:** line-by-line lemmas and constructions.
4. **Computational audit:** encoding, lineage, counts, certificates.
5. **Reconstruction audit:** rebuild the result without the original prose/code.
6. **Synthesis audit:** compare every executive-summary sentence with the accepted
   ledger.
7. **Novelty audit:** search statements, mechanisms, constructions, and subclasses.

Freeze artifacts before the stack begins. Auditors should write separate reports,
not edit the candidate underneath each other.

## 12. Stronger future-model protocol

Prepare two model inputs.

### Blind packet

```text
contract.md
variant-matrix.md
sources.md
known-case test specifications
```

Ask the new model for a fresh approach without exposing current routes.

### Informed packet

```text
accepted-ledger.md
quarantined-claims.md
failed-routes.md
frontier-obligations.md
test-corpus/
certificates/
environment.md
manifest.sha256
```

Onboarding sequence:

1. restate the contract and flag ambiguities;
2. reproduce one known positive case;
3. reproduce one known negative or restricted failure;
4. independently verify one stored certificate;
5. attempt to falsify the strongest accepted lemma;
6. solve one exact frontier obligation;
7. compare its mechanism with the blind restart.

Do not paste an unbounded historical transcript. Do not tell the blind model which
routes “obviously” fail. Record model/version, reasoning mode, prompt, inherited
assumptions, runtime, and artifacts.

## 13. User briefing

At each meaningful checkpoint:

```text
Outcome first:
What we tried:
Plain-language mechanism:
What survived:
What failed:
Exact evidence and denominator:
What remains unproved:
Source and novelty caveats:
Next artifact:
What the user can inspect:
```

Do not hide uncertainty behind notation. Do not make the user reconstruct the
distinction between a finite test, proper subclass, and complete result.

## 13A. Expert-verification packet

Internal agreement is not external verification. Once a candidate survives the
audit stack, make it unusually easy for an author or specialist to find the first
mistake.

Use this note structure:

```text
1. Exact source, question, and version/date
2. Model, definitions, timing, and excluded variants
3. Candidate theorem or counterexample, with cautious status
4. Smallest witness, diagram, or construction
5. Complete finite certificate, state table, or proof
6. Why the certificate implies the claimed conclusion
7. Published calibration cases and independent checks
8. Separate diagnosis of any conflicting published proof
9. Precise questions for the expert
10. AI-assistance and computation disclosure
11. Reproduction commands and artifact hashes
```

The note must be self-contained. Code may support the argument, but the reader
should not need to trust the search program to understand why the displayed
certificate is decisive.

For an author inquiry, use a neutral subject and a short body:

```text
Subject: Verification request about [exact question/theorem]

We found a candidate [counterexample/proof] under the following conventions:
[one-paragraph model]. The smallest witness is [one-line description]. A
self-contained note and checker are attached.

Could you please confirm:
1. whether these conventions match the intended statement;
2. whether the displayed certificate is mathematically valid;
3. whether we missed prior work or a corrected version; and
4. if relevant, whether [specific proof step] uses an unstated hypothesis?

This work was produced with substantial AI assistance and has passed the
internal checks listed in the note, but it has not yet been expert-reviewed.
```

Ask targeted questions, not “is this correct?” Keep a direct certificate
logically independent of any diagnosis of a published proof. Record replies as
new evidence in the ledger; do not silently rewrite earlier statuses.

Track mathematical verification and novelty on separate ladders:

```text
candidate
  -> property-checked
  -> independently reproduced
  -> source-calibrated
  -> expert-reviewed

novelty-unchecked
  -> targeted-search
  -> no-prior-art-found
  -> externally-confirmed
```

Progress on one ladder does not imply progress on the other. Until expert review,
prefer “candidate counterexample,” “candidate proof,” and “appears to conflict
with” over “disproof,” “proof,” or “error.”

## 14. Closeout packages

### Success package

```text
Exact theorem or counterexample:
Contract mapping:
Self-contained proof:
Dependency cards:
Certificates and independent checkers:
Published calibration cases:
Formalization, if any:
Hostile audits and repaired gaps:
Prompts/models/runtime:
Novelty search:
Expert-verification packet and response status:
Portable bundle and checksums:
```

### Blocked handoff

```text
Problem and exact source:
Open status checked on:
Solution contract:
Budget used:

Accepted partial results:
1. [statement, scope, audit, source, novelty status]

Ruled-out approaches:
1. [method, exact counterexample or failure]

Theorem-strength blockers:
1. [missing lemma and why it is comparable to the target]

Computational evidence:
- exact population and mode
- original outcomes
- later superseding certificates
- independent checks

Quarantined or unverified claims:
Frontier obligations for a stronger future model:
Required expertise/tools/sources:
Re-entry commands:
Portable bundle and manifest:
```

### Final closeout checklist

- Every summary claim appears in the accepted ledger.
- Every number names its denominator and run lineage.
- No result file was overwritten during audit.
- No solver-only claim was promoted.
- All `pending` statuses are current.
- Method refutations are labeled as method refutations.
- Proper subclasses are not described as the full conjecture.
- Source status and mathematical status are separate.
- Novelty is not announced from a targeted search alone.
- Ignored or ephemeral artifacts have been exported.

A precise blocked handoff is a successful research artifact. It is not a
breakthrough, and it should never be marketed as one.
