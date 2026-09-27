# Reproducible development and evaluation

## Current source of truth

Edit `agents/baseline/`, then regenerate `deliverables/tailorcode-submit-ready.ipynb`. The generated notebook embeds exactly these files and is independent of GitHub at Kaggle execution time. This avoids editing one configuration locally and accidentally submitting a different one.

The agent instructions, model, tools, and budgets are unchanged from the September 27 support checkpoint. Packaging now uses fixed ZIP metadata without compression for byte-identical archives across environments. A different ZIP size or hash from Version 11 is expected; the three uncompressed configuration files are unchanged.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/build_submission.py
.venv/bin/python scripts/build_submission.py --check
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/check_submission_notebook.py
```

GitHub Actions runs the same checks on pushes and pull requests without Kaggle data or credentials. The validator is intentionally limited to this baseline's structure. It is not a substitute for the official `adk-submission` compiler.

## Colab checks

Open [the development notebook in Colab](https://colab.research.google.com/github/AraceliFradejas/tailorcode-gemma-developer-agent/blob/main/notebooks/tailorcode-colab-checks.ipynb).

A CPU runtime is sufficient for the checks. It downloads the public repository, installs PyYAML, runs the preflight tests, and records the environment. It does not run the agent or download competition data/model weights. Colab GPU types and availability vary; see the [official FAQ](https://research.google.com/colaboratory/faq.html). Do not assume a Colab runtime can reproduce the full competition infrastructure.

## Public smoke suite

The suite in `evaluation/smoke-suite.json` pins three public task IDs, repositories, and base commits. Given the downloaded competition data:

```bash
python3 scripts/prepare_evaluation.py --data-root . --output /tmp/tailorcode-smoke-01
```

Choose a new output directory each time. The script verifies task identities and snapshot presence, writes the three original task records to a local subset, and reports runtime blockers. This is data preparation, not evaluation. Keep the task records and reference/test patches out of the submitted agent archive.

On September 27 the local check found all three tasks and snapshots, but no `swegemma`, Docker daemon, or NVIDIA runtime. No resolution rate is available. Model server availability is a separate check even on a machine where these executables exist.

## Running the agent later

The [prepared one-task notebook](https://colab.research.google.com/github/AraceliFradejas/tailorcode-gemma-developer-agent/blob/main/notebooks/tailorcode-public-smoke.ipynb) now follows the organizer's [getting-started example](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent) using `sandbox='subprocess'`. Docker is not needed for this path. `prepare_evaluation.py --sandbox subprocess` reports prerequisites accordingly; its default remains Docker for the CLI workflow below.

This notebook is **not yet tested with a model** and does not provision Colab. The inspected Colab session had Python 3.13 and incompatible/missing dependencies. The prepared workflow checks Linux x86_64, Python 3.12, package versions, GPU visibility and input presence before launching anything. GPU memory sufficiency and full dependency compatibility still need validation. It requires preinstalled official dependencies and predownloaded data/model files.

`scripts/run_public_smoke.py` requires explicit `--run-agent`, selects one pinned task and records its inputs, configuration hashes, environment, outcome and generated patch in a new output directory. Its 5-minute agent budget is a diagnostic override of the baseline's 30-minute budget. Startup and verification take additional time; this is not a spending cap. Cleanup stops the model server but does not disconnect the cloud machine. Save output files separately before terminating a runtime.

The user's inspected Colab account consumed paid compute units even on CPU. Review and approve consumption **before connecting**, and disconnect/delete the runtime after use. The prior session was closed and no GPU evaluation has been started.

On a properly provisioned Linux GPU host, install the organizer's [evaluation wheelhouse](https://www.kaggle.com/datasets/metric/gemma-4-developer-agent-wheelhouse), configure the required model and sandbox following `HARNESS_README.md`, then verify the installed `swegemma eval --help` options. Do not install Linux GPU wheels into the Mac environment.

The local dataset guide documents this command pattern, adapted to the prepared task subset:

```bash
swegemma eval \
  --tasks /tmp/tailorcode-smoke-01/tasks.jsonl \
  --snapshots-dir snapshots \
  --submission-dir agents/baseline \
  --results-dir results/baseline-smoke-01 \
  --sandbox docker \
  --max-tool-calls 50 \
  --max-time-minutes 30 \
  --concurrency 1 \
  --display auto
```

This command has NOT been executed here. The three selected public tasks are development cases; their results will not establish generalization to hidden tasks. Preserve the commit/configuration digest, package versions, task outcomes, runtimes, patches, and logs for every real run. Compare prompt or budget changes against the same baseline before promoting a new submission.

Cloud allocation and spending require a separate decision after hardware and budget are known. No cloud resources have been created.

## Official compiler checkpoint

The baseline subsequently passed an [official compiler construction check](compiler-check-2026-09-27.md) using `adk-submission 0.2.11` and `google-adk 1.36.1`. This uses real ADK objects with inert tool bindings and no inference. The report is in `evaluation/compiler-check-2026-09-27.json`; full harness evaluation remains outstanding.
