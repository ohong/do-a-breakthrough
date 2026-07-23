source: [Shouqiao Wang](https://x.com/Qiaoqiao2001/status/2080003441821163958)

The first secret is in problem selection.

I focused on problems mathematicians already cared about, especially ones actively discussed by people like Terence Tao.

I then used AI to filter out problems that seemed extremely difficult or were closely tied to major open conjectures.

The second secret is in prompt construction.

I used a prompt inspired by the one OpenAI used to solve the cycle double cover conjecture: https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf

The key was to make the prompt define exactly what counts as solving the problem.

Each prompt:
• restates the problem precisely,
• specifies what a complete proof or disproof must establish,
• lists weaker results that do not count,
• identifies problem-specific traps and edge cases,
• requires independent adversarial agents to challenge every candidate argument.

The prompt also tells the system how to manage the search:
• start with many independent approaches,
• keep several incompatible routes alive,
• search aggressively for counterexamples to proposed lemmas,
• mark a route as blocked if it only reduces the problem to another unproved statement of comparable strength.

The prompts I used for each problem are in the GitHub repository linked below.

To try this yourself, give GPT the problem together with a few of my successful prompts, and ask it to generate a new problem-specific prompt in the same style. Then verify that it preserves the original statement exactly.

The third secret is model selection.

I used GPT-5.6 Sol with Ultra reasoning effort. Compared with earlier models, it was effective across a much wider range of problems and much better at sustaining long, rigorous mathematical searches.

I then pasted the prompt into Codex, set it as the goal, and let it run. The reason is that Codex can work for long periods, retain the full research context, and use local files with no further interaction needed.

You need to be patient and give it enough time to explore.

Some problems produced a solution in around 6 hours. Others ran for roughly 32 hours before reaching a final answer.

The process was a continual research loop:

attempt → failure → diagnosis → new approach → proof draft → adversarial audit → repair

The model repeatedly abandoned broken ideas, attacked its own arguments, and strengthened the proof until it could no longer find substantive gaps.

I have published the materials here: https://github.com/ShouqiaoW/erdos

The repository includes the proof PDFs, LaTeX source files, and prompts used for each problem.

Some problems also include Python files for computational experiments. Two already have Lean formalizations, and formalization of the others is ongoing.
