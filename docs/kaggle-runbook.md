# Kaggle Evaluation Runbook

This runbook explains the first manual evaluation of tAilorCode. It is written for the project owner and does not require sharing credentials or API keys with anyone else.

## What is already ready

- The Kaggle competition has been joined.
- The public dataset is downloaded locally.
- The tAilorCode submission is stored in `submission/`.
- The first smoke-test task is `fastapi_14786`.
- The local Mac does not currently have the `swegemma` CLI, Docker, or the Gemma model server.

## Permissions and account actions

Only the following actions need to be performed manually by the owner of the Kaggle account:

1. Open the [Gemma 4 Developer Agent Competition](https://www.kaggle.com/competitions/gemma-4-developer-agent).
2. Confirm that the competition rules have been accepted.
3. Open the competition's **Code** area and create a private Kaggle Notebook.
4. Attach the competition dataset if Kaggle asks for dataset access.
5. Keep the notebook private while the submission is being developed.

Do not paste Kaggle API keys, passwords, cookies, or private tokens into this repository or into chat.

## First evaluation objective

Run one task rather than the entire public set:

```text
fastapi_14786
```

This issue expects the agent to strip leading and trailing whitespace from credentials parsed from an `Authorization` header. The change should be minimal and the verification tests should pass in a clean sandbox.

## Submission contents

The Kaggle submission archive must contain the contents of `submission/` at its root:

```text
submission.zip
├── agent.yaml
├── eval_config.yaml
├── configs/
├── prompts/
└── sub_agents/
```

The archive must not contain the parent `submission/` directory as an extra level. `agent.yaml` must be directly at the archive root.

## Evaluation command

In a compatible Kaggle or harness environment, the first focused run is:

```bash
swegemma eval \
  --tasks tasks.jsonl \
  --snapshots-dir snapshots \
  --submission-dir submission \
  --results-dir results/fastapi_14786 \
  --sandbox docker \
  --task-id fastapi_14786 \
  --max-tool-calls 50 \
  --max-time-minutes 30
```

The results to keep for the project notebook are:

- `summary.json`;
- the task result JSONL record;
- the generated patch;
- the verification log;
- the agent trace, when permitted by the competition rules.

## What success looks like

A successful first run should show:

1. a non-empty source-code patch;
2. no test or harness files changed by the agent;
3. targeted tests passing in the clean verification sandbox;
4. `resolved: true` for `fastapi_14786`;
5. the result recorded in `docs/evaluation-notes.md` and the presentation notebook.

## Troubleshooting

- If Kaggle reports a permission issue, accept the competition rules with the same account that will submit.
- If the model is unavailable, check that the notebook or evaluation environment is using the competition's registered Gemma 4 model.
- If the archive is rejected, inspect its root with `unzip -l submission.zip` and confirm that `agent.yaml` is at the top level.
- If a task times out, record the failure first; do not immediately increase complexity or add an adapter.

## Author

**Araceli Fradejas Munoz**
