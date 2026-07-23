# Research playbook

Use these templates to operate the coordinator/solver loop. Replace bracketed text
with problem-specific content. Keep outputs in a durable research record.

## 1. Problem intake

```text
Problem title:
Primary source and date:
Exact original statement:
Definitions and conventions:
Equivalent formulations, if verified:
Current open-status evidence and search date:
Known partial results:
Why this problem is tractable enough to attempt:
Reasons to defer it:
```

## 2. Exact solution contract

```text
Investigate the statement below without assuming it is true, false, open, or novel.

[Exact statement]

A complete affirmative result must:
1. [...]

A complete negative result must:
1. exhibit [an explicit object or construction];
2. verify [every defining hypothesis];
3. demonstrate [the exact failed conclusion].

The following do not count as a solution:
- testing finitely many cases without an exhaustive argument;
- proving a special, asymptotic, weakened, or conditional version;
- assuming the central claim in different language;
- reducing the problem to an unproved statement of comparable strength;
- relying on a computation without reproducible code or a checkable certificate.

Required edge cases and conventions:
- [...]

Allowed external theorems:
- [Name, exact version, source, and hypotheses]

Verification plan:
- [...]

First compare this contract character by character with the primary-source
statement. Report any altered quantifier, definition, domain, or convention before
attempting a solution.
```

Define both affirmative and negative completion criteria even when one direction
looks more likely.

## 3. Approach-family registry

Use a table like this:

| ID | Family | Core mechanism | Next falsifiable claim | Artifact | Status | Blocker |
|---|---|---|---|---|---|---|
| A | Constructive | Build [...] | Lemma A1 | notes/A.md | conjectured | |
| B | Minimal counterexample | Choose smallest [...] | Lemma B1 | notes/B.md | tested | |
| C | Computational | Enumerate [...] | Search space bound | code/C.* | tested | |

Keep incompatible approaches separate. Synthesize them only after identifying the
exact lemma, witness, invariant, or obstruction each contributes.

## 4. Solver kickoff

```text
Act as the primary mathematical researcher. Work against the attached solution
contract, not a remembered version of the problem.

Begin with at least three incompatible approach families. For each, state:
1. its mechanism;
2. its first falsifiable lemma or construction target;
3. a quick counterexample test;
4. what artifact you will produce next;
5. what would make the route theorem-strength blocked.

Then pursue the two best routes far enough to produce mathematics, not a status
report. Record unsupported steps explicitly. Do not call a reduction, numerical
evidence, or a conditional result a solution.
```

## 5. Nudge ladder

The coordinator chooses the lowest rung that matches the stall. Each nudge must
request a concrete artifact. Do not simply say "try harder."

### Rung 1: Continue with a deliverable

Use when the solver has a viable route but stops early.

```text
Continue the research. Before reporting status, produce one of: a proved lemma, a
fully specified candidate witness, a counterexample to the current lemma, or a
reproducible experiment with its interpretation. State the first unresolved step
exactly.
```

### Rung 2: Diagnose the structure

Use when partial results accumulate without convergence. This adapts Rybin's
request for a clear strategy from deeper structural understanding.

```text
Pause local algebra and diagnose the structure. Which invariant, obstruction, or
duality actually controls the problem? Classify the current failure precisely.
Give a clear strategy derived from that diagnosis, identify the one pivotal
falsifiable claim, and attack it now.
```

### Rung 3: Break the frame

Use when the same mechanism repeats or the pivotal lemma appears false.

```text
Abandon the current mechanism. Start an incompatible approach that does not reuse
the blocked lemma or an equivalent assumption. Reverse the likely truth value,
inspect the smallest and most degenerate cases, and search for a structured
counterexample before attempting another general proof.
```

### Rung 4: Demand unconditional completion

Use when the solver retreats to a conditional or reduction-only result despite a
live route. This adapts Rybin's "complete unconditional counterexample" and
"enough partial results" prompts, while preserving honesty.

```text
Partial and conditional results do not satisfy the contract. Attempt a complete
unconditional proof or counterexample now. List every remaining gap, then either
close each gap with an argument or explicit certificate, or mark the route blocked
and immediately pursue a materially different mechanism. Do not return vague
progress.
```

### Rung 5: Hostile verifier

Use when a candidate looks complete or confidence rises.

```text
Assume the candidate is wrong. Find the earliest invalid inference. Check every
quantifier, theorem hypothesis, boundary case, hidden division-by-zero or
nondegeneracy assumption, and computational claim. Try to construct a
counterexample to every lemma. Return a numbered gap list with the smallest repair
that would close each gap.
```

### Rung 6: Repair and reconstruct

Use after hostile audit.

```text
Repair the numbered gaps one by one. Do not patch prose around a false lemma.
Replace its mechanism or weaken the final claim honestly. Then reconstruct the
entire proof or counterexample from the contract without referring to prior drafts.
Include a dependency list and a verification obligation for every nontrivial step.
```

If a rung produces no artifact, diagnose why and move up. After rung 6, return to
rung 1 with the repaired artifact or switch approach families.

## 6. Adversarial audit checklist

- Recopy the exact statement and map each conclusion to a proof step.
- Negate the statement formally and confirm that the proposed counterexample
  satisfies that negation.
- Check all quantifiers, domains, equality cases, empty cases, minimal sizes,
  orientation conventions, integrality conditions, and parameter endpoints.
- Attempt to falsify every supporting lemma on small and degenerate instances.
- Detect any appeal to the desired result, an equivalent result, or an unproved
  theorem-strength lemma.
- Confirm every cited theorem from a primary source and match its hypotheses.
- Recompute symbolic manipulations independently.
- Reimplement computational verification from the specification, not by copying
  the original code. Check completeness of the search space separately.
- Distinguish exact arithmetic from floating-point evidence.
- Search the literature for the construction, proof idea, and equivalent statement
  before claiming novelty.

## 7. Accessible user briefing

At each meaningful checkpoint, explain:

```text
What we tried:
What the key mathematical idea means in plain language:
What failed or survived:
What evidence exists:
What is still unproved:
What the next nudge will demand:
What you can inspect without specialist knowledge:
```

Do not hide uncertainty behind notation. Define each symbol once and include a
small worked instance when it clarifies the mechanism.

## 8. Blocked-research handoff

```text
Problem and exact source:
Open-status checked on:
Solution contract:
Budget used:

Strongest surviving artifacts:
1. [...]

Ruled-out approaches:
1. [route, exact failure, evidence]

Blocked routes:
1. [missing lemma, why it is comparable in strength to the original]

Computational evidence and reproducibility:
Unverified claims:
Prompts and model outputs retained at:
Most promising materially new next approaches:
Expertise or tools required:
```

Do not describe a blocked handoff as a breakthrough. A precise account of failure
is a useful research result.
