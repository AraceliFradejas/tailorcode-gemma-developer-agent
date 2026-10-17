# Public deployment on Streamlit Community Cloud

## Status

Published and verified on **October 17, 2026**.

**Public URL:** https://tailorcode-corrige-y-aprende.streamlit.app/

The initial deployment used revision `2239242` and Python 3.12. This historical
identifier records the deployment at that time; later history maintenance may
provide an equivalent rewritten revision. The public URL is independent of the
local development address `127.0.0.1:8501`.

## Deployment settings

- Repository: `AraceliFradejas/tailorcode-gemma-developer-agent`.
- Branch: `main`.
- Entry point: `app.py`.
- Python: **3.12**, matching local verification.
- Subdomain: `tailorcode-corrige-y-aprende`.
- Secrets: none; the app does not call model APIs or download model weights.

The root `requirements.txt` includes only `requirements-demo.txt`, pinning
Streamlit 1.66.0. The historical GPU dependencies are separate. The Streamlit
configuration sets a dark theme, violet accent and disabled usage telemetry.
Local secrets are excluded from Git.

The official [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
describes repository, entry-point and Python selection. The
[dependency guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
explains that `requirements.txt` is auto-detected; the demo-specific filename alone
is not the service's automatic dependency entry point.

## Checks completed on the public app

All three screens loaded in Chrome. Their real test buttons reported the original
bug and passing corrected behavior: 3 tests for price, 3 for baskets, and 4 for
the inclusive range. This checks known examples, not new model performance.

A fresh incognito window loaded the application without Streamlit sign-in.
Both skill ZIPs were downloaded and inspected. Codex contains `SKILL.md`, the
explanation reference and UI metadata; Claude Code contains the portable
instructions and reference. No session files or credentials were included.

The footer identifies the author and links to her social profiles. The current
interface and documentation are in English. Physical mobile-device validation
remains pending; the original screenshots were desktop captures.

## Screenshots and evidence

Four real screenshots were captured with CUA from the published app, with browser
bars hidden. They were reviewed before publication and were not generated or
assembled as mockups. A later English-language refresh replaces the image set;
the original release observation remains in the evidence record.

- [Price example](images/demo/01-precio.png).
- [Basket example](images/demo/02-cestas.png).
- [Calendar example](images/demo/03-calendario.png).
- [Tests and author footer](images/demo/04-pruebas-cestas.png).

The [structured record](../evaluation/publication-2026-10-17.json) preserves
results and hashes. The [project report](../MEMORIA.md) explains the project journey.

## Agreed public wording

“Available to download and install in Codex and Claude Code.”

Documentation also states that the usage test was completed in Codex and that
execution inside Claude Code has not been validated. Distribution does not imply
that both assistants were tested. The examples are prepared demonstrations, not
fresh model generation, and no performance advantage over Codex is claimed.
