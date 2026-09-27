"""Compile the baseline with the official package, without inference or tools.

Install adk-submission 0.2.11 from the organizer's Kaggle wheelhouse and
Google ADK 1.36.1 in a separate environment first. This checks construction of
real ADK agents with inert tool bindings, not the full swegemma runtime.
"""
import argparse
import importlib.metadata
import json
import platform
from pathlib import Path

from adk_submission import (
    GenerationConstraints, ModelRegistry, NumericRange, SubmissionLimits,
    ToolRegistry, compile_submission, discover_declared_models,
)
from google.adk.tools.agent_tool import AgentTool

from build_submission import MODEL, TOOLS, load_files, payload_digest

ROOT = Path(__file__).resolve().parents[1]


def inert_tool(name):
    def disabled():
        raise RuntimeError("Compile-only check: tool execution is disabled")
    disabled.__name__ = name
    return disabled


def compile_baseline(source):
    versions = {name: importlib.metadata.version(name)
                for name in ("adk-submission", "google-adk", "google-genai", "pydantic")}
    if versions["adk-submission"] != "0.2.11" or versions["google-adk"] != "1.36.1":
        raise RuntimeError("Use the recorded compiler 0.2.11 / Google ADK 1.36.1 environment")
    declared = discover_declared_models(source)
    if declared != {MODEL}:
        raise ValueError(f"Unexpected declared models: {declared}")
    tools = ToolRegistry()
    for name in sorted(TOOLS):
        tools.register(name, inert_tool(name))
    models = ModelRegistry()
    models.register(MODEL, MODEL)
    # Compiler defaults plus file/token restrictions from the local harness guide.
    # These are not imported from swegemma and do not reproduce its runtime.
    limits = SubmissionLimits(
        allowed_file_extensions=frozenset({".yaml", ".yml", ".md", ".txt", ".py", ".json", ".safetensors"}),
        adapter_extensions=frozenset({".safetensors"}),
    )
    agent = compile_submission(
        source, tool_registry=tools, model_registry=models, limits=limits,
        generation_constraints=GenerationConstraints(
            max_output_tokens=NumericRange(1, 32768),
            thinking_budget=NumericRange(0, 32768),
        ),
    )
    analyzers = [tool.agent for tool in agent.tools if isinstance(tool, AgentTool)]
    if len(analyzers) != 1 or analyzers[0].name != "tAilorCode_analyzer":
        raise ValueError("Expected one compiled analyzer AgentTool")
    return {
        "check": "official_compiler_construction", "status": "passed",
        "configuration_sha256": payload_digest(load_files(source)),
        "python": platform.python_version(), "platform": platform.system(),
        "packages": versions, "root_agent": agent.name,
        "root_class": type(agent).__name__, "analyzer_agent": analyzers[0].name,
        "declared_models": sorted(declared), "registered_tool_count": len(TOOLS),
        "tool_bindings": "inert placeholders; never invoked",
        "model_binding": "declared model string; no inference server or weights loaded",
        "limits": "compiler defaults plus file/token restrictions from HARNESS_README; not imported from swegemma",
        "inference": "not_run", "sandbox_evaluation": "not_run", "score": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "agents/baseline")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = compile_baseline(args.source)
    output = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
