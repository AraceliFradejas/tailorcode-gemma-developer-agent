"""Validate the baseline and generate an offline, deterministic Kaggle notebook.

These are project preflight checks, not the official adk-submission compiler.
The generated notebook needs only Python's standard library.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = "gemma-4-31b-it-qat-w4a16-ct"
TOOLS = {
    "run_command", "read_file", "edit_file", "write_file", "get_status",
    "submit_patch", "get_code_neighbors", "search_similar_code", "get_code_subgraph",
}
EXPECTED = {"agent.yaml", "eval_config.yaml", "sub_agents/code_analyzer.yaml"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject accidental duplicate keys rather than silently overwriting them."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def load_files(source):
    files = {}
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not supported: {path}")
        if path.is_file():
            files[path.relative_to(source).as_posix()] = path.read_text(encoding="utf-8")
    return files


def validate(files):
    if set(files) != EXPECTED:
        raise ValueError(f"Baseline files must be exactly {sorted(EXPECTED)}")
    configs = {}
    for name, text in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Unsafe path: {name}")
        config = yaml.load(text, Loader=UniqueKeyLoader)
        if not isinstance(config, dict):
            raise ValueError(f"Expected YAML mapping: {name}")
        configs[name] = config
    names = set()
    for path in ("agent.yaml", "sub_agents/code_analyzer.yaml"):
        config = configs[path]
        name = config.get("name", "")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"Invalid agent name: {path}")
        if name in names:
            raise ValueError("Agent names must be distinct")
        names.add(name)
        if config.get("model") != MODEL:
            raise ValueError(f"Wrong competition model: {path}")
        if not isinstance(config.get("instruction"), str) or not config["instruction"].strip():
            raise ValueError(f"Missing instruction: {path}")
        tools = config.get("tools")
        if not isinstance(tools, list) or not tools:
            raise ValueError(f"Missing tools: {path}")
        for tool in tools:
            if isinstance(tool, str):
                if tool not in TOOLS:
                    raise ValueError(f"Unknown tool: {tool}")
            elif isinstance(tool, dict) and set(tool) == {"agent_tool"}:
                reference = tool["agent_tool"]
                if not isinstance(reference, dict):
                    raise ValueError("agent_tool must be a mapping")
                target = reference.get("config_path")
                if path != "agent.yaml" or target != "sub_agents/code_analyzer.yaml":
                    raise ValueError("Unexpected or unsafe agent_tool reference")
                if reference.get("skip_summarization") is not True:
                    raise ValueError("Baseline analyzer must skip summarization")
            else:
                raise ValueError(f"Unsupported tool declaration in {path}")
        sampling = config.get("generate_content_config", {})
        if not isinstance(sampling, dict):
            raise ValueError("Sampling configuration must be a mapping")
        allowed = {"temperature", "top_p", "top_k", "max_output_tokens", "seed",
                   "presence_penalty", "frequency_penalty", "stop_sequences",
                   "response_mime_type", "thinking_config"}
        if set(sampling) - allowed:
            raise ValueError("Unsupported sampling field")
        max_tokens = sampling.get("max_output_tokens")
        if type(max_tokens) is not int or not 1 <= max_tokens <= 32768:
            raise ValueError("Invalid max_output_tokens")
        thinking = sampling.get("thinking_config", {})
        if not isinstance(thinking, dict):
            raise ValueError("thinking_config must be a mapping")
        budget = thinking.get("thinking_budget", 0)
        if type(budget) is not int or not 0 <= budget <= 32768:
            raise ValueError("Invalid thinking_budget")
    if "submit_patch" not in configs["agent.yaml"]["tools"]:
        raise ValueError("Root agent must have submit_patch")
    readonly = {"read_file", "search_similar_code", "get_code_neighbors", "get_code_subgraph"}
    if any(not isinstance(t, str) or t not in readonly
           for t in configs["sub_agents/code_analyzer.yaml"]["tools"]):
        raise ValueError("Analyzer must remain read-only")
    evaluation = configs["eval_config.yaml"].get("evaluation")
    if not isinstance(evaluation, dict) or set(evaluation) != {
        "timeout_seconds", "max_tool_calls", "max_time_minutes", "max_turns"
    }:
        raise ValueError("Invalid baseline evaluation budget fields")
    for key, value in evaluation.items():
        if type(value) not in (int, float) or value <= 0:
            raise ValueError(f"Invalid evaluation budget: {key}")
        if key != "max_time_minutes" and type(value) is not int:
            raise ValueError(f"Budget must be an integer: {key}")
    return configs


def payload_digest(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def render_notebook(files):
    code = '''from pathlib import Path
import hashlib
import zipfile

# Embedded configuration: no external input, network, GPU, or package installation.
embedded_files = ''' + repr(dict(sorted(files.items()))) + '''

working_root = Path('/kaggle/working') if Path('/kaggle').is_dir() else Path.cwd()
working_root.mkdir(parents=True, exist_ok=True)
archive_path = working_root / 'submission.zip'

# Fixed timestamps and permissions make unchanged builds byte-for-byte identical.
with zipfile.ZipFile(archive_path, 'w') as archive:
    for name, content in sorted(embedded_files.items()):
        info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_STORED
        archive.writestr(info, content.encode('utf-8'))

with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(embedded_files)
    assert 'agent.yaml' in archive.namelist()
    for name, content in embedded_files.items():
        assert archive.read(name).decode('utf-8') == content
    assert sum(info.file_size for info in archive.infolist()) < 3 * 1024**3
    print('Contents:', ', '.join(archive.namelist()))

print('ZIP created and verified:', archive_path)
print('Bytes:', archive_path.stat().st_size)
print('SHA256:', hashlib.sha256(archive_path.read_bytes()).hexdigest())
print('Packaging passed. Agent compilation and scoring have not been performed.')
'''
    def cell(kind, content, number):
        value = {"cell_type": kind, "id": f"tailorcode-submit-{number}",
                 "metadata": {}, "source": content.splitlines(keepends=True)}
        if kind == "code":
            value.update(execution_count=None, outputs=[])
        return value
    intro = (
        "# tAilorCode — reproducible submission baseline\n\n"
        "Generated from `agents/baseline/` by `scripts/build_submission.py`. "
        "Edit the source YAML and rebuild; do not maintain a second copy in Kaggle.\n\n"
        f"Configuration digest: `{payload_digest(files)}`\n\n"
        "Run all cells to create `/kaggle/working/submission.zip`. "
        "This notebook uses only the Python standard library. "
        "The ZIP contains agent configuration; Kaggle separately runs and scores the agent."
    )
    outro = (
        "## Kaggle workflow\n\n"
        "1. Import this notebook into the competition notebook editor.\n"
        "2. Disable Internet in notebook settings.\n"
        "3. Save a new version using **Save & Run All** and wait for completion.\n"
        "4. Verify that this version outputs `submission.zip`.\n"
        "5. Submit that version when ready and record the version number and error category.\n\n"
        "A successful packaging run does not confirm agent compilation or a competition score."
    )
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "kaggle": {"accelerator": "none", "isInternetEnabled": False,
                   "language": "python", "sourceType": "notebook", "isGpuEnabled": False}},
        "cells": [cell("markdown", intro, 0), cell("code", code, 1), cell("markdown", outro, 2)]}
    return json.dumps(notebook, ensure_ascii=False, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "agents/baseline")
    parser.add_argument("--output", type=Path, default=ROOT / "deliverables/tailorcode-submit-ready.ipynb")
    parser.add_argument("--check", action="store_true", help="Fail if the generated notebook is stale")
    args = parser.parse_args()
    files = load_files(args.source)
    validate(files)
    rendered = render_notebook(files)
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            parser.exit(1, "Notebook is stale. Run scripts/build_submission.py.\n")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(f"PASS: baseline preflight; configuration SHA256 {payload_digest(files)}")
    print("Official compiler validation and agent evaluation are still required.")


if __name__ == "__main__":
    main()
