# Evaluation Notes

This file will record local and Kaggle evaluation runs for tAilorCode.

## First evaluation targets

The first public tasks selected for baseline testing are:

- `fastapi_14786`: a localized authorization credential parsing fix.
- `rich_4077`: a small change in `file_proxy.py`.
- `requests_6592`: support for the HTTP 425 `TOO_EARLY` status type.

These tasks were selected because their reference changes are small and their verification tests are focused.

## First smoke test: `fastapi_14786`

This is the preferred first task because the acceptance criteria are unusually clear. The issue asks the agent to remove leading and trailing whitespace from credentials extracted from an `Authorization` header. The reference change is a focused `.strip()` on the parsed parameter in `fastapi/security/utils.py`, and the verification patch adds requests with repeated and trailing spaces.

Expected agent behavior:

1. Locate `get_authorization_scheme_param()` and its callers.
2. Confirm that the scheme and credential are split correctly but the credential is not normalized.
3. Apply the smallest source-only change.
4. Run the targeted security tests.
5. Submit the patch after checking the diff.

This task is useful as a first smoke test because it tests repository navigation, root-cause reasoning, minimal editing, and targeted verification without requiring a broad refactor.

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
