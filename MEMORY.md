# tAilorCode — Technical handoff

Updated October 17, 2026. Author and project owner: **Araceli Fradejas Muñoz**.

The portfolio-facing project report is [MEMORIA.md](MEMORIA.md). This file is a
short handoff for continuing the work, not the formal project report.

## Current purpose

The project began with a Kaggle Gemma developer-agent competition experiment.
Araceli decided not to continue towards a competition submission and transformed
the work into her own educational skill and interactive learning lab.
The public presentation is **tAilorCode · Fix and learn**. Documentation and the
current demo are in English, as requested. Prior session notes were backed up
locally before the report was restructured.

## Published version

- Demo: https://tailorcode-corrige-y-aprende.streamlit.app/.
- Repository: https://github.com/AraceliFradejas/tailorcode-gemma-developer-agent.
- Streamlit Community Cloud, `main`, entry point `app.py`, Python 3.12.
- `requirements.txt` includes only the demo requirements, not the GPU stack.
- Three visual examples: zero price, shared basket lists, inclusive range.
- Tests ran on the public deployment: 3 price tests, 3 basket tests, 4 range tests.
- Anonymous access was checked in a new incognito window.
- Both skill archives were downloaded and inspected.
- Local release checkpoint: 37 tests passed; AppTest covered all three screens.
- Footer: copyright, author name, GitHub, LinkedIn, X, Medium and YouTube links.

## Where the implementation lives

`skills/tailorcode/` is the portable source. The project-local installer targets
`.agents/skills/tailorcode/` or `.claude/skills/tailorcode/` without overwriting an
existing installation. The web demo is in `app.py` and `demo/`. The lab and known
acceptance tests are under `scripts/repair_lab.py` and `examples/repair-lab/`.

The price screen replays a Codex correction. The basket and range screens use
prepared reference corrections. No screen generates new model responses.
Skill downloads contain only instructions, the explanation reference, and Codex
interface metadata where applicable.

## Evidence and limits

- [Publication evidence](evaluation/publication-2026-10-17.json).
- [Guided Codex smoke test](evaluation/skill-guided-demo-2026-10-17/result.json).
- [Exploratory comparison](evaluation/skill-comparison.json): one case, identical
  patch with/without the skill, all three original tests pass. No functional
  advantage demonstrated. Model and reasoning settings were not captured.
- Claude Code package available; execution inside Claude Code remains untested.
  Do not use the work account for a personal evaluation.
- Physical-device mobile testing remains pending.
- Original Colab evidence and local session artifacts remain private under
  `deliverables/session-*/`, excluded from Git.

## Preserved competition milestone

On October 16, Gemma solved public task `fastapi_14786` on a Colab A100. The
recorded result was `resolved: true`, test exit code 0, six tool calls, and
43.65 seconds of evaluator time. This is not a Kaggle score or a current-skill
benchmark. The FastAPI HTTP compatibility blocker was fixed by pinning 0.136.3.
The runtime was deleted and zero active sessions were observed afterwards.
Do not resume GPU work or competition submissions as the next project step.

## Operational notes

Restart Streamlit after structural changes to imported modules. A stale live
process caused a missing `basket_trace` import even though fresh-process tests
passed. A browser refresh alone did not update that imported module.

Keep authorship under Araceli's configured identity. Public commit messages are
in English. Do not add assistant co-author trailers. Historic measured commit
identifiers in evaluation records describe the original execution; if history
is rewritten, preserve that evidence and record equivalent source revisions.

## History maintenance

Unwanted assistant co-author trailers were removed from 11 historical commit
messages at the author's request. Every original commit tree, author, committer,
timestamp and parent order was preserved; descendant identifiers changed. A
verified Git bundle and revision map are retained privately under
`deliverables/session-20261017/history-backup/`. No signature was removed.
The Colab templates now pin the tree-equivalent clean historical revision.
Measured records keep their original identifiers and an additional equivalent
revision so that evidence is not represented as a new execution.
