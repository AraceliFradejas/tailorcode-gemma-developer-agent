# Evaluating tAilorCode

## Question and scope

Does the skill improve correction, verification or explanation of focused Python
bugs? We do not assume that it does. Three educational examples are an initial
check, not a representative benchmark. The earlier Gemma run is a separate result.

## Matched comparisons within each assistant

The proposed initial comparison is three cases × two conditions × two assistants:
twelve runs. Record the model identifier, client version, date, relevant settings
and available limits. Compare with/without the skill within the same assistant;
differences between products may have other causes.

1. Prepare a new folder with `scripts/repair_lab.py prepare` for each run. Do not
   supply the reference corrections in `tests/test_tailorcode_skill.py` or earlier
   conversations to the assistant under test.
2. Use a fresh conversation for each condition with the same model, reasoning,
   tools, permissions and common task prompt. Only the skill condition adds its
   invocation. Check that the baseline does not inherit a personal/global skill.
3. Alternate condition order across cases. Do not reuse a prior repair or give
   extra hints to only one condition. Record interventions and repeat a matched
   pair if an intervention invalidates the comparison.
4. Install the skill only in its condition folder. Preserve the response, diff,
   command trace and outcomes before evaluating them.
5. Run `scripts/repair_lab.py check` independently. It rejects changes to the
   original acceptance test file and executes the known test. Keep exit code,
   number of tests and full output, rather than accepting the assistant's claim.
6. Score both attempts using the rubric below, preferably with condition labels
   hidden from the reviewer. Preserve failed attempts too.

The lab does not launch assistant sessions, paid APIs or models. It prepares
files and executes local Python. It is not a sandbox for arbitrary code.

## Rubric

| Dimension | Observable criterion |
| --- | --- |
| Correction, 0–1 | Original acceptance tests unchanged and all pass. |
| Verification, 0–2 | 0: absent or unsupported claim; 1: post-edit check only; 2: before-edit reproduction and after-edit verification with commands/outcomes. |
| Explanation, 0–2 | 0: absent/incorrect; 1: identifies the cause; 2: correctly connects cause, change and a concrete example. |
| Scope, 0–1 | No unrelated edits or weakened tests. |
| Honesty, 0–1 | Distinguishes checked behavior from unresolved claims; invents no results. |

Record total duration and usage/cost if available. Better explanations may take
longer; report that trade-off rather than hiding it in an aggregate score. A
single paired difference does not establish general improvement.

## Results record

[evaluation/skill-comparison.json](../evaluation/skill-comparison.json) currently
has `status: partial`. Future entries should include run ID, case, assistant,
model/client versions, condition, date, skill hash (or `null` in the baseline),
actual prompt, limits, test count/exit code, duration if measured, rubric notes,
and reviewed transcript/diff/output paths.

Do not populate model results with handwritten reference repairs. Those validate
the lab, not the model. Keep unknown metadata explicitly unknown.

## October 17 exploratory observation

Both `zero-price` conditions produced the same patch and independently passed
three original tests. The user-supplied explanations were similar; the condition
with the skill included an explicit verification status. No functional or measured
educational improvement was demonstrated.

A folder-selection mistake changed the order to with-skill then without-skill.
Model, reasoning settings, client version and actual reading of the skill were
not captured. Responses were pasted by the user without full tool traces.
The UI-reported 12 and 10 seconds are not controlled latency measurements.
Treat this as partial exploratory evidence, not a conclusive experiment.
