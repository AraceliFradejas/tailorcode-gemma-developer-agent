# First Claude Code usage test

The skill has one source: `skills/tailorcode/SKILL.md`. The installer copies its
portable instructions and reference to `.claude/skills/tailorcode/`. Codex-only
interface metadata is omitted. No second workflow needs maintaining.

**Status:** package prepared and inspected; actual execution inside Claude Code
has not been validated. Do not use an employer's account for this personal test.

## Prepare a new project folder

```bash
python3 scripts/repair_lab.py prepare --case independent-lists --workspace /tmp/tailorcode-claude-demo
python3 scripts/install_tailorcode_skill.py --target claude --project /tmp/tailorcode-claude-demo
```

Both scripts preserve existing folders. Open this exact exercise folder as a new
project in Claude Code. If using its CLI, start it from that folder:

```bash
cd /tmp/tailorcode-claude-demo
claude
```

Ask:

> /tailorcode Two calls that add labels without supplying a list must produce
> independent lists. If I supply a list, add to that same list. Fix the bug and
> explain how you checked the correction.

The visual demo maps these generic lists onto shopping baskets. Save the response,
commands and observed outputs. Then check from the tAilorCode repository:

```bash
python3 scripts/repair_lab.py check --case independent-lists --workspace /tmp/tailorcode-claude-demo
```

A local copy was also prepared on October 17 at
`deliverables/session-20261017/claude-first-demo/`, excluded from Git. It is not
part of a fresh clone and may use the earlier language version of the instructions;
use a fresh installation for a new test.

Record discovery, model/client versions and observed behavior only after actual
execution. Installing the files alone does not establish those results. No Colab
runtime is needed; access and usage limits remain those of the assistant account.
