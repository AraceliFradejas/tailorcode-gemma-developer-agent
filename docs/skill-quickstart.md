# First guided exercise: a free product

You need Python and access to Codex or Claude Code. No Colab runtime or additional
API service is required. Assistant availability and usage limits depend on your account.

## 1. Prepare a small project

From the repository root:

```bash
python3 scripts/repair_lab.py prepare --case zero-price --workspace /tmp/tailorcode-first-demo
python3 scripts/repair_lab.py check --case zero-price --workspace /tmp/tailorcode-first-demo
```

The check should fail: the original function mistakes a zero price for a missing
price. This is the intended reproduction, not an installation failure. The
preparer refuses to overwrite an existing folder; choose a new path if necessary.

## 2. Install for your assistant

```bash
python3 scripts/install_tailorcode_skill.py --target codex --project /tmp/tailorcode-first-demo
```

For Claude Code, use `--target claude`. Open that project folder in a new assistant
conversation and check that the skill is available. Copying files successfully
does not prove that a conversation already in progress has discovered them.

## 3. Ask for a repair

In Codex:

> Use $tailorcode. Zero is a valid price: a free product must not use the fallback
> price. Only None means the price is missing. Preserve negative prices too.
> Fix the bug and explain how you checked the correction.

In Claude Code, begin the same request with `/tailorcode`.

Observe whether the assistant identifies the cause, reproduces the bug before
editing, preserves the requirements and distinguishes checks from assumptions.
The skill does not guarantee those outcomes; this is a usage test.

## 4. Independently verify the result

From the tAilorCode repository:

```bash
python3 scripts/repair_lab.py check --case zero-price --workspace /tmp/tailorcode-first-demo
```

Keep the complete output. All three original tests should run. The checker
rejects altered acceptance tests. If the check fails, preserve the error and diff
rather than reporting the task as solved.

The folder is temporary. Copy any conversation, patch and output you want to keep
to a permanent location, and review it before publication.

## 5. Explain what you learned

You should be able to explain why zero was confused with a missing value, what
the correction changes, and which inputs the tests cover. That explanation and
the actual diff/test output form a useful project demonstration.

This guided exercise is not a controlled experiment. Follow the
[comparison protocol](skill-evaluation.md) before claiming that the skill improves
the assistant, and do not treat a run with prior knowledge of the solution as an
uncontaminated benchmark attempt.
