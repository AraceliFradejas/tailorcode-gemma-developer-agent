# Colab preparation checkpoint — September 27, 2026

Status: candidate setup prepared, **not installed or validated on Colab**. No GPU
evaluation has run. Opening the saved notebook is safe; connecting any runtime
can consume the user's paid compute units and requires prior cost approval.

## October 4 continuation decision

Colab is the chosen path for continued development; no local Linux installation
on the Mac is needed. Kaggle submissions are deferred while the scoring error
remains unresolved. See [the support update](progress-2026-09-27.md#october-4-update).
The candidate installation and one-task evaluation are still unvalidated.

Start by opening the [one-task notebook](https://colab.research.google.com/github/AraceliFradejas/tailorcode-gemma-developer-agent/blob/main/notebooks/tailorcode-public-smoke.ipynb)
without connecting a runtime. Review runtime availability and consumption before
connecting; keep both execution approval flags false until the corresponding
steps are approved. The runtime version below is the September 27 candidate,
not a claim that it is currently available or that any available GPU will fit Gemma.

Record the project revision, environment versions, setup logs and any future
task outcome. Publish only non-sensitive reports in GitHub; keep model weights,
competition data, credentials and private Drive links outside the repository.
Saving a notebook does not preserve files on a temporary Colab machine.

## Runtime choice

Use **2026.04** as the candidate runtime. The [Colab runtime table](https://research.google.com/colaboratory/runtime-version-faq.html)
lists Python 3.12.13 and PyTorch 2.10.0. Although 2026.07 also has Python 3.12,
its PyTorch 2.11.0 differs from vLLM 0.19.1's declared `torch==2.10.0` requirement
([published metadata](https://pypi.org/pypi/vllm/0.19.1/json)). An isolated venv
will resolve its own dependencies instead of changing Colab's notebook packages.
This is a compatibility candidate, not proof of sufficient GPU memory/CUDA support.

## Official harness packages

An unauthenticated Kaggle CLI 2.2.4 query successfully listed the organizer's
wheelhouse. Three small official wheels were downloaded and inspected on the Mac;
they were not installed into the project environment. Their hashes and requirements
are saved in `evaluation/official-harness-wheels.json`.

In an approved cloud runtime with Kaggle CLI available, download these three files:

```bash
kaggle datasets download metric/gemma-4-developer-agent-wheelhouse -f adk_submission-0.2.11-py3-none-any.whl -p /content/harness-wheels
kaggle datasets download metric/gemma-4-developer-agent-wheelhouse -f adk_eval_core-0.1.0-py3-none-any.whl -p /content/harness-wheels
kaggle datasets download metric/gemma-4-developer-agent-wheelhouse -f swegemma-0.2.7-py3-none-any.whl -p /content/harness-wheels
python scripts/install_gpu_environment.py --wheelhouse /content/harness-wheels --venv /content/tailorcode-gpu-venv --install
```

The installer verifies the hashes, refuses other platforms/Python versions and
existing environment paths, resolves pinned top-level GPU packages from PyPI,
runs `pip check` and import checks, and records installed versions. Dependency
resolution may still reveal conflicts. It downloads dependencies but no model,
starts no inference, and does not disconnect a billable machine.

Use `/content/tailorcode-gpu-venv/bin/python` for `check_smoke_environment.py` and
`run_public_smoke.py`; the notebook's default `sys.executable` must be changed to
this interpreter after successful setup. The saved Drive notebook remains a
prepared template, not a ready-to-run environment.

## Model and task access

The browser displays [the required model version](https://www.kaggle.com/models/google/gemma-4/other/gemma-4-31b-it-qat-w4a16-ct/2)
as 23.3 GB. No weights have been downloaded. Model size is not a GPU VRAM estimate.
The CLI model-file listing requires authentication; no local credentials were found.
Use Kaggle's official OAuth login when authorized, not tokens pasted into notebooks,
chat or GitHub. Browser sign-in alone does not authenticate a separate CLI.

The public task data already exists on the Mac, but is not mounted in Colab. It
still needs an authorized download or private transfer into the temporary runtime.
Do not upload the dataset to the public repository. Before starting the GPU, verify
model/data access, available disk space, required GPU memory and the displayed credit rate.

## Resume

1. Complete the authorized Kaggle CLI sign-in and verify read-only access.
2. Agree on a bounded CPU setup session if cloud installation testing is needed.
3. Install and check the candidate environment, preserving logs and package versions.
4. Review GPU consumption separately before starting the one-task evaluation.
5. Save result files, then disconnect/delete the runtime and verify no active sessions.
