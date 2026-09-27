# Official compiler construction check — September 27, 2026

## Result

The unchanged baseline compiled successfully into a real Google ADK `LlmAgent` named `tAilorCode`, with a real `AgentTool` wrapping `tAilorCode_analyzer`. Official model discovery found only `gemma-4-31b-it-qat-w4a16-ct`.

See `evaluation/compiler-check-2026-09-27.json` for the configuration digest, package versions, and compiler wheel digest.

## Method and limits

Downloaded `adk_submission-0.2.11-py3-none-any.whl` directly from the organizer's [Kaggle wheelhouse](https://www.kaggle.com/datasets/metric/gemma-4-developer-agent-wheelhouse), whose UI showed version 25. Installed it with `google-adk==1.36.1` in a separate temporary Python environment on the Mac. The stock Colab runtime inspected earlier had Google ADK 2.7.1; the compiler's package metadata requires ADK below 2.0, so installing it into that shared runtime without isolation could cause a dependency conflict.

The script invokes the real `discover_declared_models` and `compile_submission`. The nine tool names bind to disabled placeholder functions; the model binds to its declared string. No tools execute, no model is loaded, and no network inference occurs. Limits use compiler defaults plus documented file and token restrictions, not an imported swegemma configuration.

This confirms parsing, schema acceptance, reference resolution, and ADK object construction for this baseline. It does not validate actual tool implementations, serving, the evaluation budget loader, Docker, repository fixes, or Kaggle acceptance. It does not explain the existing `Kaggle Error`.

## Repeat the check

Download the compiler wheel from the official dataset. In a separate virtual environment, install the wheel and the matching ADK version:

```bash
python3 -m venv /tmp/tailorcode-compiler-venv
/tmp/tailorcode-compiler-venv/bin/python -m pip install /path/to/adk_submission-0.2.11-py3-none-any.whl 'google-adk==1.36.1'
/tmp/tailorcode-compiler-venv/bin/python scripts/check_official_compiler.py --report /tmp/compiler-check.json
```

Do not add organizer wheels or credentials to GitHub. The checked-in report records the actual run rather than promising all future dependency combinations will behave identically.

## Colab preservation

The development checks also passed in a CPU Colab session. At the user's request, a copy named `tAilorCode - Development Checks - 2026-09-27.ipynb` was saved in their Google Drive with the visible outputs, and Colab confirmed all changes saved. The private Drive URL is not published in this repository. The separate compiler test above ran locally, not in that saved Colab notebook.
