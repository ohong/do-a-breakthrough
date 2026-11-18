# Examples of AI-assisted mathematical discovery

These examples are based on the discoverers' own public accounts. The model or
agent attributions below identify the AI system they say did the main discovery
work; they do not independently validate the mathematical results. Additional
details attributed to Grok are explicitly labeled and should be treated as
leads until checked against primary sources.

## Jacobian conjecture

- **Result:** A claimed low-degree polynomial counterexample in three variables
  to the conjecture, which dates to 1939.
- **Primary LLM:** **Claude Fable 5**, according to the announcement.
- **Evidence:** Levent Alpöge credits Fable with the result and also mentions
  prompting assistance.
- **Source:** [“Jacobian conjecture is false.”](https://x.com/__alpoge__/status/2079028340955197566)
- **Notes:** Grok describes the construction as having constant nonzero
  Jacobian determinant while not being injective. Alpöge is a professional
  mathematician, so this is an example of AI-assisted expert research rather
  than a novice solving outside their field.

## Dinitz-Garg-Goemans conjecture

- **Result:** A counterexample to the roughly 30-year-old conjecture.
- **Primary LLM:** **GPT-5.6 Pro**, used through ChatGPT.
- **Evidence:** Dmitry Rybin writes that the counterexample was found in a
  linked GPT-5.6 Pro chat.
- **Source:** [“Dinitz-Garg-Goemans conjecture is false.”](https://x.com/DmitryRybin1/status/2079904005652893709)
- **Notes:** Grok describes the witness as a graph with fractional flow cost 58
  but unsplittable flow cost at least 60 under capacity violation at most 15.

## McKee's pentagulation conjecture

- **Result:** A counterexample to the conjecture.
- **Primary LLM:** **GPT-5.6 Sol Pro**.
- **Evidence:** Anirudh Chakravarthy says he used GPT-5.6 Sol Pro to resolve
  this problem and the perfect Mendelsohn design problem below.
- **Source:** [“McKee's pentagulation conjecture is false.”](https://x.com/anirudhchak/status/2080338128922108085)
- **Notes:** Chakravarthy describes having no mathematical background and using
  a broad prompt asking the model to find and fully solve an old open
  conjecture.

## The (9,6,1)-perfect Mendelsohn design

- **Result:** A proof that the design does not exist.
- **Primary LLM:** **GPT-5.6 Sol Pro**.
- **Evidence:** Chakravarthy attributes both results in the same post to
  GPT-5.6 Sol Pro.
- **Source:** [“The (9,6,1)-perfect Mendelsohn design does not exist.”](https://x.com/anirudhchak/status/2080338128922108085)
- **Notes:** This result came from the same broad, low-domain-context prompting
  session as the McKee counterexample.

## Graffiti Conjectures 39, 40, and 154

- **Result:** Claimed proofs of Graffiti Conjectures 39 and 40 and a claimed
  refutation of Graffiti Conjecture 154.
- **Primary AI agent:** **Devin**; the underlying LLM is not identified in the
  supplied source.
- **Evidence:** Jared Zoneraich says he showed Devin the preceding viral
  AI-mathematics examples and asked it to find and crack similar problems.
- **Source:** [Announcement of three Graffiti results and the Brandt result.](https://x.com/imjaredz/status/2080088341262033273)
- **Notes:** Grok reports that a community note identifies an earlier
  refutation of Conjecture 154. If so, that part is rediscovery rather than a
  new solution.

## Brandt's Regular Supergraph Problem

- **Result:** A claimed counterexample to the roughly 20-year-old problem.
- **Primary AI agent:** **Devin**; the underlying LLM is not identified in the
  supplied source.
- **Evidence:** Zoneraich attributes this result and the three Graffiti results
  above to one day of work by Devin.
- **Source:** [Announcement of three Graffiti results and the Brandt result.](https://x.com/imjaredz/status/2080088341262033273)
- **Notes:** Grok identifies the problem as appearing on Douglas West's list of
  open problems.

## Graffiti Conjecture 284

- **Result:** A counterexample to the roughly 30-year-old graph-theory
  conjecture.
- **Primary LLM:** **Grok 4.5 Medium**, operating as the Capy agent in Slack.
- **Evidence:** Justin Sun says Capy chose to investigate the conjecture and
  found a novel refutation in eight minutes while running on Grok 4.5 Medium.
- **Source:** [“REFUTED: Graffiti Conjecture 284.”](https://x.com/justinsunyt/status/2080116559352316409)
- **Notes:** Grok says the counterexample uses the Hoffman-Singleton graph and
  was adversarially checked by other models.

## Erdős problem 870

- **Result:** A claimed solution concerning order-\(k\) bases and
  representations, accompanied by a large Lean 4 formalization.
- **Primary LLM:** **ChatGPT-5.5-Pro**.
- **Evidence:** David Turturean attributes the solution to ChatGPT-5.5-Pro.
- **Source:** [Announcement of the Erdős #870 solution.](https://x.com/DavidTurturean/status/2070531663461756950)
- **Notes:** Grok describes the formalization as approximately 180,000 lines
  and reports that Turturean claimed it was the largest single-person
  formalization of one problem. That superlative has not been independently
  checked.

## Petersen coloring conjecture

- **Result:** A claimed 68-vertex cubic bridgeless counterexample.
- **Primary LLM:** **GPT-5.6 Sol** with **Ultra** reasoning effort.
- **Evidence:** The announcement attributes the counterexample to GPT-5.6 Sol
  Ultra.
- **Source:** [“Petersen coloring conjecture is false.”](https://x.com/NeuralReformist/status/2080153035045839069)
- **Notes:** The graph size and structural description are from Grok's summary
  and have not been independently checked.

## Six open Erdős problems

- **Result:** Solutions to six open Erdős problems in five days.
- **Primary LLM:** **GPT-5.6 Sol** with **Ultra** reasoning effort, running in
  Codex.
- **Evidence:** Shouqiao Wang names GPT-5.6 Sol in the opening post and later
  specifies Ultra reasoning effort as a key part of the workflow.
- **Source:** [“I solved 6 open Erdős problems in 5 days, using OpenAI GPT-5.6 Sol.”](https://x.com/Qiaoqiao2001/status/2080003441821163958)
- **Notes:** The reported problems are 390, 486, 536, 788, 1002, and 1038.
  Wang describes a long-horizon, contract-style workflow: restate the problem,
  define what counts as a complete solution, and require adversarial
  self-critique.

## Cycle Double Cover Conjecture

- **Result:** A claimed proof that every bridgeless graph has a cycle double
  cover.
- **Primary LLM:** **GPT-5.6 Sol** with **Ultra** reasoning effort.
- **Evidence:** OpenAI published the model-generated proof and the prompt used to
  produce it. A later exposition by Sang-il Oum reconstructs the argument.
- **Sources:** [OpenAI proof.](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf)
  [Oum's exposition.](https://sangil.dimag.kr/2026/cdc/)
- **Notes:** This addresses a central structural graph-theory conjecture from
  the 1970s. The exposition is encouraging evidence, but expert uptake and
  scrutiny will determine its lasting influence.

## Erdős planar unit-distance conjecture

- **Result:** A counterexample to Erdős's conjectured upper bound for the number
  of unit-distance pairs in a planar point set.
- **Primary LLM:** An unreleased **OpenAI reasoning model**.
- **Evidence:** OpenAI published the generated proof, and nine mathematicians
  subsequently wrote a shorter, human-verified account of the construction.
- **Sources:** [OpenAI's announcement.](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)
  [Human-verified account.](https://arxiv.org/abs/2605.20695)
- **Notes:** This overturns a belief dating to 1946 and unexpectedly connects
  discrete geometry with algebraic number theory.

## Erdős problem 1051

- **Result:** A proof of the irrationality claim for rapidly growing integer
  sequences.
- **Primary AI agent:** **Aletheia**, powered by **Gemini Deep Think**.
- **Evidence:** Google DeepMind reports that Aletheia solved the problem
  autonomously; the Erdős Problems database records the affirmative solution
  and a Lean formalization.
- **Sources:** [Google DeepMind's research report.](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/)
  [Erdős problem 1051.](https://www.erdosproblems.com/1051)
- **Notes:** Later work generalized the result substantially. DeepMind classifies
  the original solution as a modest but nontrivial autonomous research result.

## Erdős problem 728

- **Result:** A proof of the intended nontrivial factorial-divisibility
  formulation of the problem.
- **Primary LLM:** **GPT-5.2 Pro**; **Aristotle** formalized and repaired the
  proof in Lean.
- **Evidence:** Kevin Barreto gives a detailed first-person account of the
  prompting, ambiguity in the original statement, literature search, and
  formalization.
- **Source:** [“Problem 728 and the use of AI on Erdős problems.”](https://www.erdosproblems.com/forum/thread/blog%3A2)
- **Notes:** The result is specialized and depends on a clarified interpretation,
  but it became an early credited example of an LLM producing a novel solution
  to an Erdős problem.

## Anderson's quasi-complete local-ring problem

- **Result:** A counterexample: a weakly quasi-complete Noetherian local ring
  that is not quasi-complete.
- **Primary AI agents:** **Rethlas** found the construction and **Archon**
  generated its Lean formalization.
- **Evidence:** The project paper describes the autonomous search and formal
  verification; the public repository contains the approximately 20,000-line
  Lean development.
- **Sources:** [Project paper.](https://arxiv.org/abs/2604.03789)
  [Lean formalization.](https://github.com/frenzymath/Anderson-Conjecture)
- **Notes:** The theorem is a genuine commutative-algebra result, while the large
  formalization may be at least as important as a demonstration of method.

## Erdős problem 652

- **Result:** A proof that the constants governing the \(k\)-th smallest number
  of distinct distances tend to infinity with \(k\).
- **Primary AI agent:** **Aletheia**, powered by **Gemini Deep Think**.
- **Evidence:** Google DeepMind lists problem 652 among Aletheia's autonomous
  results, and the Erdős Problems database records the problem as proved.
- **Sources:** [Google DeepMind's research report.](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/)
  [Erdős problem 652.](https://www.erdosproblems.com/652)
- **Notes:** The closing argument follows quickly from an existing incidence
  theorem, so it resolves the listed problem without introducing a comparably
  broad new theorem.

## Erdős problem 1196

- **Result:** A proof of the 1968 primitive-set conjecture, including a sharp
  asymptotic bound.
- **Primary LLM:** **GPT-5.4 Pro**, prompted by Liam Price.
- **Evidence:** The Erdős Problems record links the proof, subsequent
  extensions, and a Lean formalization; its discussion preserves the
  GPT-5.4 Pro provenance audit.
- **Sources:** [Erdős problem 1196.](https://www.erdosproblems.com/1196)
  [Provenance discussion.](https://www.erdosproblems.com/forum/thread/1196?order=oldest)
- **Notes:** The result has been checked, extended by a group of mathematicians,
  and formalized, although its broader influence is still being assessed.

## Written on the Wall II Conjecture 91

- **Result:** A reported counterexample to a computer-generated graph
  conjecture posted in 2004.
- **Primary LLM:** **ChatGPT-5.6 Pro**, according to a secondary report.
- **Evidence:** The report says the model selected the conjecture from a supplied
  list and returned a small exact witness.
- **Source:** [Wissner-Gross's report.](https://theinnermostloop.substack.com/p/welcome-to-july-24-2026)
- **Notes:** No primary discovery post or independent write-up was located. The
  exact witness may make correctness easy to check, but the isolated conjecture
  appears unlikely to have broad mathematical impact.

## Alleged Röll conjecture

- **Result:** A posted counterexample using the square of a spherical twist on a
  projective K3 surface.
- **Primary LLM:** **Claude Fable**, according to the announcement.
- **Evidence:** The announcement says Fable supplied an autoequivalence acting
  trivially on the Mukai lattice but not equal to an even shift.
- **Source:** [Kevin's announcement account.](https://x.com/dj_d_sol)
- **Notes:** The example is standard and predates the announcement, and no
  credible provenance for a named open “Röll conjecture” was found. This should
  be treated as a correction or rediscovery, not a new mathematical solution.

## Further leads to verify

The supplied Grok summary also names the following cases but does not provide a
direct announcement or proof link. They are preserved here as research leads,
not as fully sourced examples:

- A prover-verifier LLM harness announced by Omri Weinstein reportedly solved
  nine open problems in theoretical computer science.
- Adam Holter reportedly announced a batch of ten smaller conjecture results.
