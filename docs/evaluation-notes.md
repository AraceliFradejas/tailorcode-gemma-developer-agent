# Evaluation Notes

This file will record local and Kaggle evaluation runs for tAilorCode.

## First evaluation targets

The first public tasks selected for baseline testing are:

- `fastapi_14786`: a localized authorization credential parsing fix.
- `rich_4077`: a small change in `file_proxy.py`.
- `requests_6592`: support for the HTTP 425 `TOO_EARLY` status type.

These tasks were selected because their reference changes are small and their verification tests are focused.

## Current environment

The local macOS workspace contains the public competition data and the submission files, but it does not currently have the `swegemma` CLI, Google ADK, Gemma 4 model server, or Docker available. Full evaluation will therefore be run in the competition environment or a prepared compatible environment.

## Results table

| Run | Task | Tool calls | Result | Notes |
| --- | --- | ---: | --- | --- |
| Pending | `fastapi_14786` | - | Not run | Awaiting a compatible evaluation environment |
| Pending | `rich_4077` | - | Not run | Awaiting a compatible evaluation environment |
| Pending | `requests_6592` | - | Not run | Awaiting a compatible evaluation environment |

## Author

**Araceli Fradejas Munoz**
