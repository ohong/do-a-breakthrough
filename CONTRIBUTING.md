# Contributing

Contributions should make AI-assisted mathematical research more rigorous,
reproducible, accessible, or effective.

Especially useful contributions include:

- successful breakthrough or rediscovery case studies;
- honest failed-search reports and diagnosed dead ends;
- problem-selection and solution-contract improvements;
- exact prompts and nudge sequences that produced useful progress;
- visible model outputs and reasoning traces, process logs, and full chat
  transcripts when they may be legally and permissibly published;
- proof audits, counterexample checks, reproducible code, certificates, or formal
  verification;
- techniques that help non-specialists understand and supervise the process; and
- corrections to reported results, sources, or attributions.

## Case-study format

Include enough information for another person to reproduce and challenge the work:

```text
Problem and primary source:
Status checked on:
Models, agents, tools, and settings:
Time, token, and compute budget:
Exact initial prompt:
Exact follow-up nudges:
Approach families attempted:
Key failures and diagnoses:
Candidate proof or counterexample:
Verification performed:
Independent or expert review:
Novelty search:
Links to publishable outputs or transcript:
Remaining gaps:
```

Distinguish a new result, rediscovery, partial result, and failed attempt. Do not
describe a model's confidence as verification. If a claim has not received expert
review, say so prominently.

## Reasoning traces and privacy

Share exact prompts, visible reasoning traces and model responses, tool outputs,
process logs, and chat transcripts when the service terms, applicable law, and
every participant permit it. Redact API keys, account data, private
correspondence, unpublished third-party work, personal information, and
confidential material.

Do not attempt to extract, reconstruct, or demand hidden chain-of-thought. Many
systems do not expose it, and private internal reasoning is not required for a
reproducible contribution. Share the reasoning the model explicitly returned,
concise rationale summaries, mathematical scratch work, artifacts, and
verification records instead.

Obtain consent before publishing another person's messages or identifying
information. Link to large transcripts or artifacts rather than placing unwieldy
files directly in a pull request.

## Proposing changes

1. Open an issue or pull request that identifies the failure mode or opportunity.
2. Keep the skill model- and agent-agnostic.
3. Preserve the exact-solution-contract and adversarial-verification safeguards.
4. Prefer concrete prompt or workflow changes over generic encouragement.
5. Run the skill validator and report the result.
6. Explain any new files, dependencies, or user-visible behavior.

By contributing, you agree that your contribution is licensed under this
repository's MIT License and that you have the right to submit the included
material.
