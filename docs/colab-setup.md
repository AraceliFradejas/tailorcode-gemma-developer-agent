# Colab preparation checkpoint — September 27, 2026

Status: the October 4 CPU installation passed dependency and selected import
checks; **GPU serving and task evaluation remain unvalidated**. Opening the saved notebook is safe; connecting any runtime
can consume the user's paid compute units and requires prior cost approval.

## October 4 continuation decision

Colab is the chosen path for continued development; no local Linux installation
on the Mac is needed. Kaggle submissions are deferred while the scoring error
remains unresolved. See [the support update](progress-2026-09-27.md#october-4-update).
The subsequent CPU installation checkpoint is recorded below. GPU serving and
one-task evaluation remain unvalidated.

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

### October 4 CPU observation

Araceli supplied output from a diagnostic cell in her private Colab copy after
authorizing only a roughly five-minute CPU check. The reported environment was:

| Check | Reported value |
| --- | --- |
| Python | 3.12.13 |
| Platform | Linux x86_64 |
| Free disk | 210.5 GiB |
| kagglehub | 1.0.0 |
| kaggle | 2.0.0 |
| torch | 2.10.0+cpu |
| transformers | 5.0.0 |
| vllm | Not installed |

The runtime settings screenshot offered 2026.04 and allowed selecting A100;
H100 was disabled. No GPU allocation, memory capacity or credit rate was verified.
The supplied model configuration declares `Gemma4ForConditionalGeneration`,
`quant_method: compressed-tensors` and `quantization_status: compressed`.
The expanded quantization groups were not supplied in the first check; the
subsequent small-file download below supplied those settings.

This establishes basic CPU platform/version observations, not a working serving
stack or authenticated download access. No model inference was performed.
At 13:38 Europe/Madrid, Araceli confirmed saving the notebook and disconnecting.
Runtime deletion and absence of active sessions were not independently verified.
The previous CPU authorization does not extend to another session or installation.

The next preparation step is to verify access to the public task inputs
without downloading weights, then plan the isolated installation
and persistence of its logs before requesting further runtime consumption.

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

### October 4 Colab download verification

Araceli separately authorized a CPU check of up to roughly five minutes to
download only these three wheels, without installation. Her supplied output
at 16:12 Europe/Madrid confirms downloads via KaggleHub from wheelhouse
version 25 and SHA256 matches against the recorded manifest:

| Wheel | Bytes | SHA256 check |
| --- | --- | --- |
| adk_submission-0.2.11-py3-none-any.whl | 62,404 | Matched |
| adk_eval_core-0.1.0-py3-none-any.whl | 89,306 | Matched |
| swegemma-0.2.7-py3-none-any.whl | 111,548 | Matched |

No packages were installed or executed. Dependency resolution, serving and
task-data access remain unverified. These cache files are on a temporary
runtime and will need downloading again after deletion. Saving cell outputs
does not preserve the downloaded files. Shutdown of this check's runtime has
not yet been confirmed.

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

### Colab environment creation without ensurepip

At 18:51 on October 4, the first Colab installation attempt failed while creating
the venv, before dependency installation. The diagnostic output confirmed that
`/usr/bin/python3` has pip but no `ensurepip` or `virtualenv`.
The installer now uses standard `venv` when `ensurepip` exists, otherwise
`virtualenv` if installed. If neither is available, it stops with an explicit
setup requirement before creating a directory.

In an approved setup session, install `requirements-setup.txt` using the notebook
interpreter, then rerun the updated installer with a new venv path. Never reuse
or overwrite the partial environment from the failed attempt. This changes only
environment creation; dependency resolution and real GPU execution remain unverified.

Use `/content/tailorcode-gpu-venv/bin/python` for `check_smoke_environment.py` and
`run_public_smoke.py`; the notebook's default `sys.executable` must be changed to
this interpreter after successful setup. The saved Drive notebook remains a
prepared template, not a ready-to-run environment.

## Model and task access

### October 4 small-file download

After separately authorizing another CPU check of up to roughly five minutes,
Araceli ran `kagglehub.model_download` with the pinned handle
`google/gemma-4/other/gemma-4-31b-it-qat-w4a16-ct/2` and `path="config.json"`.
The supplied output at 13:56 Europe/Madrid reported a successful 18,711-byte
configuration download:

- Architecture: `Gemma4ForConditionalGeneration`.
- Quantization: `compressed-tensors`, status `compressed`.
- Group format: `pack-quantized`, targeting `Linear`.
- Weights: 4-bit integers, group size 32, symmetric group quantization.
- Input and output activation quantization: null in the reported group.

This confirms access from that Colab session to this particular small file.
It does not establish whether authentication was used, that all model files
can be downloaded, GPU memory sufficiency, or serving compatibility.
No weights were requested and no inference was performed. Araceli reported
the session disconnected at 16:09, before the subsequent wheel-download check;
runtime deletion was not independently verified.

The browser displays [the required model version](https://www.kaggle.com/models/google/gemma-4/other/gemma-4-31b-it-qat-w4a16-ct/2)
as 23.3 GB. No weights have been downloaded. Model size is not a GPU VRAM estimate.
The CLI model-file listing requires authentication; no local credentials were found.
For the verified KaggleHub 1.0.0 Colab path, store an API token in Colab Secrets
under `KAGGLE_API_TOKEN` and enable notebook access only for trusted code.
KaggleHub reads this secret automatically; this is token authentication, not OAuth.
Never paste the token into notebook source, outputs, chat or GitHub.
Browser sign-in alone does not authenticate a separate runtime.

### October 4 authenticated task metadata check

The initial request for `tasks.jsonl` failed with `UnauthenticatedError`.
After configuring Colab Secrets and separately authorizing a CPU session of up
to roughly five minutes, Araceli supplied successful output at 16:30 Europe/Madrid.
`kagglehub.whoami(verbose=False)` completed, followed by a request for only
`tasks.jsonl` through `kagglehub.competition_download`:

- File size: 1,984,455 bytes.
- Records: 129.
- Exactly one matching task: `fastapi_14786`.
- Repository: `fastapi/fastapi`.
- Base commit: `eacbce24c9d299c6a28110d9fc8ac50f53cddb08`.

This confirms authenticated access to the metadata and the pinned task identity.
No snapshots or model weights were downloaded, and no task code or inference
was executed. Runtime shutdown after this check has not yet been confirmed.

Secrets values are not included in an exported notebook, but trusted notebook
code with secret access can read them. Do not expose them through expressions,
logs, shell commands or saved widget outputs. Each person using a shared notebook
must configure their own credentials and accept the competition terms.

Full task inputs still need preparation in the eventual evaluation runtime:
the snapshot, graph, embeddings and offline dependencies are not established
by the metadata download.
Do not upload the dataset to the public repository. Before starting the GPU, verify
model/data access, available disk space, required GPU memory and the displayed credit rate.

## Resume

### October 4 installation and notebook organization

The uploaded owner notebook records a successful installation using installer
revision `a9bfa3e54f6d57936216dcf34d15a9290e26749b`, after the missing-ensurepip
fix. The captured output reports exit code 0, `No broken requirements found.`,
successful selected imports and `CUDA available: False` in the CPU session.
This is not proof of working GPU inference or a preserved environment.

The public notebook now separates approvals, CPU inspection, Secrets-based
authentication, configuration/metadata checks, project/wheel preparation,
isolated installation, pending full-input preparation, and GPU evaluation.
Historical useful outputs are labeled Markdown records; executable cells have
no saved outputs and start with approval checks. Repetitive installation logs
are summarized; the owner's original download is unchanged.

The corrected installer revision is used from the start, so the ad hoc update
cell and duplicate wheel check are no longer needed. Installation progress is
streamed to the notebook and recorded in a log. Preflight and inference use the
isolated environment's Python. Existing project, venv and log paths are preserved.
Changing runtime may discard all temporary preparation.

The notebook still does not automate full model/snapshot/graph/embedding
provisioning. It explicitly stops at that pending stage. Inference approval stays
false. Revoke notebook Secret access before repository-code evaluation; do not
expose credentials or personal Drive files to that sandbox.

1. Prepare the remaining task inputs and their persistence strategy. The model's
   `config.json`, official wheels and authenticated task metadata access have
   been checked; full snapshot and model downloads remain outstanding.
2. Agree on a bounded CPU setup session if cloud installation testing is needed.
3. Install and check the candidate environment, preserving logs and package versions.
4. Review GPU consumption separately before starting the one-task evaluation.
5. Save result files, then disconnect/delete the runtime and verify no active sessions.

### October 4 evening handoff

The owner confirmed receiving the organized downloadable notebook at 19:26
Europe/Madrid after the direct Colab link failed to open. The maintained source
is `notebooks/tailorcode-public-smoke.ipynb`; import its downloaded `.ipynb` with
Colab's **File → Upload notebook** and save a private Drive copy. Local distribution
copies do not constitute another independently maintained source.

The complete local suite passed 17 tests at this checkpoint. No runtime was
connected for notebook organization. Colab appeared disconnected in the earlier
post-installation screenshot, but runtime deletion and current session status
have not been independently checked.

An OS paste-protection warning was reported during attempts to share installation
output. Its trigger was not determined. The protection was not bypassed; the
installation result was read from screenshots and the owner-provided notebook.
Do not characterize the warning as a confirmed false positive or a specific
package vulnerability.

Before the next session, finish full-input provisioning and decide how to retain
downloads and logs. Do not spend GPU time reviewing or editing preparation cells.
The original CPU approval does not carry over to another session or GPU inference.
