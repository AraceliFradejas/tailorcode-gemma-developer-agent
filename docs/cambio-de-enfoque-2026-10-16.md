# From a competition agent to my own learning project

**Decision date:** October 16, 2026, Europe/Madrid.
**Author and project director:** Araceli Fradejas Muñoz.

## Why I changed the goal

I began tAilorCode as a Gemma developer-agent competition experiment on Kaggle.
I wanted to learn, build something with AI, and add a project I could explain to
my portfolio. The original workflow investigated a repository issue, changed
source code, and asked an evaluator to check the patch.

After several days preparing Kaggle and Colab, Gemma resolved a real public
FastAPI task. That was evidence the pipeline could work, but the visible result
still felt too small and abstract compared with the time spent on infrastructure.
I decided not to continue towards a competition submission.

Instead of discarding the work, I kept the investigation, focused editing, testing
and evidence practices, and turned them into **tAilorCode · Fix and learn**.
The delivery goal became an independent educational product rather than another
benchmark attempt.

## The product decision

The first idea was a web application that accepted code and generated repairs
through a model API. Before introducing another provider and its usage costs,
I chose a portable skill that reuses an existing coding assistant. The visual
layer then became a lab for understanding known examples and checking their
behavior, without presenting prepared output as fresh model generation.

The current project has a reusable repair-and-explanation skill, three independent
Python exercises, a project-local installer, and a public Streamlit demo. A
visitor can understand the examples without installing an assistant; a developer
can download the skill and use it in their own project.

## What was reused and what changed

| Competition experiment | Independent learning product |
| --- | --- |
| Investigate a repository issue | Investigate a focused bug in the user's project. |
| Return a small source patch | Show a reviewable correction and explain its cause. |
| Verify with the competition evaluator | Run available relevant checks and report actual outcomes. |
| Preserve run evidence | Explain what was tested, what failed and what remains unknown. |
| Serve Gemma on an A100 | Use the host assistant's model and tools. |
| Competition prohibition on changing tests | Permit meaningful regression tests in normal development without weakening acceptance criteria. |

A skill is a bundle of instructions and resources, not a trained model. Its value
over an assistant's normal debugging ability must be evaluated rather than assumed.

## First implementation and subsequent feedback

The skill source is `skills/tailorcode/`. Its project-local installer targets
`.agents/skills/tailorcode/` for Codex and `.claude/skills/tailorcode/` for Claude
Code, preserving existing installations. The three examples are a zero price,
a shared default list and an inclusive range.

The original visual presentation was too technical. I asked for a simpler
explanation, and it was rebuilt around a free product incorrectly charged at
20 euros. The same approach shaped the basket and watering-calendar examples:
show the situation and expected outcome first, with code and technical output
available as optional detail.

The interface also gained visible case choices, skill downloads, installation
steps, and my authorship footer. The first public version was deployed on
October 17: https://tailorcode-corrige-y-aprende.streamlit.app/.

## What the evidence supports

The lab's original fixtures fail assertions and their reference corrections pass
unchanged tests. A real guided Codex price repair was independently checked.
The exploratory with/without-skill pair produced the same patch and passing tests,
so it did not demonstrate a functional advantage from the skill.

The public deployment's three buttons ran 3, 3 and 4 tests respectively. Both ZIPs
were downloaded and inspected, and the app opened anonymously in an incognito
window. Execution inside Claude Code remains untested. No employer account was
used for this personal evaluation.

The earlier Gemma success belongs to the original model/configuration and does
not validate this skill. The complete context, architecture, screenshots,
verification and lessons are in the [project report](../MEMORIA.md).

## How I present the project

“tAilorCode started as a Kaggle developer-agent experiment. I transformed the
workflow into my own educational skill and visual lab: understand a Python bug,
review a small correction, and check the result with real tests.”

The current scope is a finished first public version. Matched evaluations,
Claude Code execution and physical-device testing are potential follow-up work,
not prerequisites disguised as already completed features.
