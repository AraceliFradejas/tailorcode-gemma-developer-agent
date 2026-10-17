# Testing strategy

The current project has separate verification layers. A passing package build,
a working web screen and a correct model-generated repair answer different questions.

## Local project checks

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

At the first public release, 37 tests passed. They cover input manifest checks,
isolated-environment setup, guarded historical notebooks, reproducible submission
packaging, skill installation, fixture integrity, and the current demo engine.

The fixture tests confirm that original examples fail assertions and handwritten
reference corrections pass the unchanged acceptance tests. This validates the lab;
it is not a model evaluation. The demo tests additionally check actual behavior,
including independent basket simulations and inclusive range boundaries.

## Interface checks

Streamlit AppTest has exercised scenario changes, learning feedback, case switching,
and the real acceptance-check buttons. Such checks do not establish visual quality
or full accessibility. Screenshots and browser observations complement them.
The English-language revision requires checking the new labels and repeating the
screen walkthrough. No physical-mobile-device validation is claimed.

## Public deployment checks

The initial public deployment loaded anonymously and ran 3 price tests, 3 basket
tests and 4 range tests successfully after reproducing the respective original
bugs. Both skill archives were downloaded and inspected. The
[publication report](publicacion-streamlit.md) identifies the evidence and limits.

## Assistant behavior

A guided Codex correction was independently tested. The exploratory paired price
case produced the same passing patch with and without the skill. Actual reading
of the skill and matching model settings were not captured, so no causal advantage
is claimed. Follow [the evaluation protocol](skill-evaluation.md) for future runs.
Claude Code execution remains pending despite the available package.

## Preserved competition checks

```bash
.venv/bin/python scripts/build_submission.py --check
.venv/bin/python scripts/check_submission_notebook.py
```

These verify the historical baseline and self-contained artifact. They do not run
Gemma or validate current skill behavior. The October 16 public-task result is
preserved separately in `evaluation/public-smoke-2026-10-16.json`.
