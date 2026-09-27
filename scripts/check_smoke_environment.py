"""Read-only checks for the published Python 3.12 Linux GPU wheelhouse workflow.

No model download, package installation, GPU allocation or inference occurs.
GPU memory is reported, not treated as proof that a model will fit.
"""
import argparse
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def compatibility_issues(system, machine, python_version, packages, gpu_available):
    issues = []
    if system != "Linux" or machine != "x86_64":
        issues.append("Published GPU wheels require Linux x86_64 for this workflow")
    if tuple(python_version[:2]) != (3, 12):
        issues.append("This published wheelhouse workflow requires Python 3.12")
    for package in ("swegemma", "adk-submission", "adk-eval-core", "google-adk", "vllm"):
        if not packages.get(package):
            issues.append(f"Missing package: {package}")
    for package, expected in (("adk-submission", "0.2.11"), ("google-adk", "1.36.1"), ("vllm", "0.19.1")):
        if packages.get(package) and packages[package] != expected:
            issues.append(f"Expected {package} {expected}; found {packages[package]}")
    if not gpu_available:
        issues.append("No functioning NVIDIA GPU detected")
    return issues


def inspect_environment(data_root, model_path, task_id):
    packages = {}
    for name in ("swegemma", "adk-submission", "adk-eval-core", "google-adk", "vllm"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    gpu = None
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                                    capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                gpu = result.stdout.strip() or None
        except (OSError, subprocess.TimeoutExpired):
            pass
    issues = compatibility_issues(platform.system(), platform.machine(), sys.version_info, packages, bool(gpu))
    required = [data_root / "tasks.jsonl", data_root / "snapshots" / f"{task_id}.tgz",
                data_root / "wheels", data_root / "graphs", data_root / "embeddings",
                model_path / "config.json"]
    for path in required:
        if not path.exists():
            issues.append(f"Missing input: {path}")
    if not model_path.is_dir() or not any(model_path.glob("*.safetensors")):
        issues.append("No model safetensors found; full weights and tokenizer still need validation")
    return {"python": platform.python_version(), "platform": platform.system(),
            "architecture": platform.machine(), "packages": packages, "gpu": gpu,
            "task_id": task_id, "blockers": issues,
            "status": "blocked" if issues else "basic_checks_passed",
            "inference": "not_run", "note": "Passing does not guarantee sufficient VRAM, working dependencies, or a working subprocess sandbox."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--model-path", required=True, type=Path)
    parser.add_argument("--task-id", default="fastapi_14786", choices=["fastapi_14786", "rich_4077", "requests_6592"])
    args = parser.parse_args()
    report = inspect_environment(args.data_root, args.model_path, args.task_id)
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if report["blockers"] else 0)


if __name__ == "__main__":
    main()
