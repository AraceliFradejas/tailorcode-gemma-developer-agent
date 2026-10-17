# Evaluation notes

## Results by layer

| Observation | Recorded result | Interpretation |
| --- | --- | --- |
| October 16 Gemma run | `fastapi_14786` resolved; verification exit 0; 6 tool calls; 43.65 seconds evaluation time. | One real public task, not a Kaggle score or current-skill benchmark. |
| October 17 guided Codex run | Price correction independently passed three original tests. | Working repair for that example. |
| October 17 exploratory pair | Same correction and passing tests with/without skill installed. | No functional advantage observed; incomplete condition metadata. |
| Local lab | Broken fixtures fail assertions; reference repairs pass. | Usable exercises, not model performance. |
| Public Streamlit app | The three buttons passed 3, 3 and 4 tests. | Hosted known-case execution works. |
| Claude Code | Package prepared and inspected; no execution. | Compatibility behavior remains unvalidated. |

Source evidence:

- [Gemma result](../evaluation/public-smoke-2026-10-16.json).
- [Guided Codex result](../evaluation/skill-guided-demo-2026-10-17/result.json).
- [Exploratory comparison](../evaluation/skill-comparison.json).
- [Public deployment checks](../evaluation/publication-2026-10-17.json).

The price case normalises the distinction between zero and a missing value.
The basket and range examples are handwritten educational reference repairs.
The project does not claim general performance, hidden evaluation success,
trained weights, or a measured learning improvement.

The earlier public development suite selected FastAPI, Rich and Requests tasks.
Only the FastAPI model execution was completed. The other tasks are not current
work items: the project changed scope to the educational skill and visual lab.

See the [project report](../MEMORIA.md) for the narrative and the
[comparison protocol](skill-evaluation.md) for future experimental controls.
