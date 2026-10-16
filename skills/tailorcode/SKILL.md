---
name: tailorcode
description: Fix a focused Python bug and teach the user why the correction works, with a reviewable diff and evidence from relevant checks. Use for debugging requests that ask to learn or understand the repair, rather than broad feature development.
---

# tAilorCode — corrige y aprende

Work in the user's repository and reply in their language. Use the assistant's
existing model and tools; this skill does not start Gemma or require Kaggle.

## Investigate and repair

- Identify the expected behavior from the issue and repository evidence. Ask only
  when an unresolved ambiguity would change the correction. For an explanation-only
  request, inspect and explain without editing.
- Inspect relevant source, callers and tests. Before changing source, attempt a
  focused reproduction in the available environment. Keep the original outcome:
  an import failure is an environment blocker, not a reproduced application bug.
- Explain the likely cause briefly, citing a concrete function or line. Give
  observable evidence, not a transcript of private reasoning. Proceed with an
  authorized repair without imposing a separate approval after the explanation.
- Make a focused correction that preserves the specified behavior and existing
  user changes. Avoid unrelated refactors. Existing acceptance tests are evidence:
  do not weaken them to make a patch pass. Add a regression test when it captures
  the bug meaningfully; unlike the old competition agent, normal development may
  include new tests. If an existing test contradicts the request, explain the
  conflict before changing its expectation.
- Repeat the reproduction and run relevant tests. Broaden checks when the change
  affects shared behavior. Use repository tooling; do not assume pytest is present.
  If a check cannot run, record the blocker and leave verification incomplete.
- Inspect the diff for unrelated edits and temporary artifacts. If the same check
  still fails after two repair attempts, report the observed failure and what
  remains unresolved before further speculative changes. Never report success
  merely because a patch looks plausible.

## Explain the result

Adapt length to the user's experience. Include:

- What failed, with a small input/output example when useful.
- What changed and why that change addresses the cause; reference the actual diff.
- What was checked: exact command, observed result, and limits of that evidence.
  Clearly distinguish executed tests, syntax-only checks, and unverified proposals.
- One learning point tied to this fix. Offer a short exercise only when helpful.

Use the following statuses when producing a report: **Verified by relevant tests**,
**Syntax checked only**, **Not verified**, or **Unresolved**. Passing focused tests
supports the tested behavior, not a guarantee for all inputs or the full project.
The skill does not authorize commits, pushes, deployments or paid services beyond
what the user requested.

For adapting a report to beginners or experienced users, consult
[references/explanation.md](references/explanation.md) only when needed.
