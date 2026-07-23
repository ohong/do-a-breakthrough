# Do a Breakthrough

`do-a-breakthrough` is an installable skill for using frontier language models as
persistent mathematical research collaborators. It turns an open problem into a
precise solution contract, keeps several incompatible approaches alive, and runs
the loop

> attempt → failure → diagnosis → new approach → proof draft → adversarial audit → repair

The workflow is designed to be understandable by someone with elementary
mathematics. The agent defines notation, explains each major idea in plain
language, preserves a research ledger, and makes uncertainty explicit.

It does **not** guarantee a breakthrough. Language models can produce plausible
but false mathematics, misquote the literature, or rediscover a known result.
Treat every output as a candidate until it has been independently checked. Get
qualified expert review before announcing, publishing, or submitting a claimed
result.

## Install

Install it with the Skills CLI:

```sh
npx skills add https://github.com/ohong/do-a-breakthrough
```

See the [Skills documentation](https://www.skills.sh/docs) for supported agents
and CLI options.

## Use

Invoke the installed skill in your agent and provide a problem or ask it to help
select one:

```text
Use $do-a-breakthrough to investigate this conjecture: [exact statement and source].
I have 8 hours of compute. Explain the mathematics in plain language and keep a
durable research record.
```

Or:

```text
Use $do-a-breakthrough to help me choose a bounded, verifiable open problem from
[authoritative problem list]. Build the exact solution contract before searching.
```

The skill first verifies the statement and whether the problem is still open. It
then defines exactly what would count as a proof or disproof, including what does
not count. During research it:

- keeps multiple incompatible proof and counterexample routes;
- searches aggressively for counterexamples to proposed lemmas;
- rejects circular arguments and reductions to equally difficult open statements;
- treats computation as evidence until it becomes a verified exhaustive argument
  or checkable certificate;
- sends targeted nudges when the solver stalls;
- audits and repairs every candidate result; and
- stops honestly with either a verified candidate package or a useful blocked
  research handoff.

## A smaller model can nudge a stronger model

The skill separates two logical roles. A coordinator can be a smaller, faster, or
cheaper agent that maintains the contract and research ledger. It repeatedly gives
the strongest available solver model a focused objective and escalates through a
specific nudge ladder:

1. demand the next mathematical artifact;
2. diagnose the controlling structure;
3. restart from an incompatible mechanism;
4. insist on unconditional completion or an explicit blocked route;
5. switch to hostile verification; and
6. repair and reconstruct the result.

This architecture is model- and agent-agnostic. Use whatever coordinator,
long-running harness, and solver models are available. With only one model, the
skill alternates solver and hostile-verifier roles in separate passes, though that
is weaker than independent review.

## What to provide

The best starting material includes:

- an exact statement copied from a primary source;
- definitions and conventions;
- a link or citation showing its current status;
- known partial results, if any;
- your time, token, and compute budget; and
- any tools available for symbolic computation, code, search, or formal proof.

You do not need to know the advanced mathematics in advance. You do need patience,
skepticism, and willingness to seek expert review.

## Repository layout

- [`skills/do-a-breakthrough/SKILL.md`](skills/do-a-breakthrough/SKILL.md) contains
  the agent workflow.
- [`skills/do-a-breakthrough/references/research-playbook.md`](skills/do-a-breakthrough/references/research-playbook.md)
  contains the reusable contract, prompt, nudge, audit, and handoff templates.
- [`wang-method.md`](wang-method.md) records Shouqiao Wang's public description of
  his long-horizon workflow.
- [`rybin-method.md`](rybin-method.md) records Dmitry Rybin's short continuation
  prompts.
- [`examples.md`](examples.md) collects public reports of AI-assisted mathematical
  discoveries, with caveats about independent validation.

## Inspirations

The core workflow is based on
[Shouqiao Wang's public account](https://x.com/Qiaoqiao2001/status/2080003441821163958)
of problem selection, contract-style prompts, incompatible approaches,
counterexample search, long-running research, adversarial critique, and repair.
The nudge ladder adapts
[Dmitry Rybin's published prompts](https://x.com/DmitryRybin1/status/2079904005652893709),
which repeatedly asked a model to continue, find a deeper structural strategy, and
finish an unconditional counterexample rather than settle for partial results.

These are methodological inspirations, not independent validation of every
reported mathematical result. The skill deliberately does not assume a result
exists and does not suppress open-status or novelty checks.

## Contribute

Successful case studies, failed-search lessons, prompt improvements, verification
techniques, and new nudge patterns are welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE)
