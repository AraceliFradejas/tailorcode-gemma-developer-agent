# Project conventions

## Ownership and language

- This project is created, directed and owned by Araceli Fradejas Muñoz. Preserve
  the configured Git author identity. Do not add assistant or automation co-author
  trailers to commits. Add human co-authors only when the user explicitly requests it.
- Do not add AI-assistance credits or assistant bylines to project authorship text
  unless the user explicitly requests them.
- Maintain current UI text, README, guides, project report and commit messages in
  English. The conversation may use the user's preferred language.
- `MEMORIA.md` is the formal portfolio report. `MEMORY.md` is a concise technical
  handoff. Keep the report organised by context, goals, architecture, evidence,
  decisions and learning; do not replace it with a raw chat/session transcript.

## Evidence

- The project began as a Kaggle competition experiment and became an independent
  educational skill and lab. Make that evolution clear without implying a score.
- Keep model runs, fixture self-checks, prepared reference corrections, UI checks
  and exploratory comparisons distinct. Never invent tests or model evaluations.
- Original logs, prompts and measured identifiers remain historical evidence.
  Do not translate a recorded input or replace its revision as if it were newly run.
- Both skill packages are available. Actual execution inside Claude Code remains
  untested; do not use an employer account for personal validation.
- Keep session archives, Git history backups, account links and secrets out of Git.

## Verification and deployment

- Run relevant local checks after code changes. Use AppTest for changed interaction
  paths, and check the live Streamlit app after deployment when browser access is available.
- Restart the local Streamlit server after structural module changes.
- Public app entry point: `app.py`; Python 3.12; demo requirements remain separate
  from historical GPU dependencies. Do not start GPU sessions for demo maintenance.
