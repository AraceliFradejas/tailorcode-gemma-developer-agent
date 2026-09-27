"""Prepare a public task subset and report local evaluation prerequisites.

No inference, package installation, container launch, or cloud allocation occurs.
Public reference/test patches stay in the evaluation subset, never in the agent ZIP.
"""
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def select_tasks(tasks_path, suite):
    wanted = {task["instance_id"]: task for task in suite["tasks"]}
    if len(wanted) != len(suite["tasks"]):
        raise ValueError("Duplicate task IDs in suite")
    selected = {}
    with tasks_path.open(encoding="utf-8") as source:
        for line in source:
            task = json.loads(line)
            task_id = task.get("instance_id")
            if task_id in wanted:
                if task_id in selected:
                    raise ValueError(f"Duplicate task in dataset: {task_id}")
                for field in ("repo", "base_commit"):
                    if task.get(field) != wanted[task_id][field]:
                        raise ValueError(f"Dataset mismatch for {task_id}: {field}")
                selected[task_id] = task
    missing = wanted.keys() - selected.keys()
    if missing:
        raise ValueError(f"Missing tasks: {sorted(missing)}")
    return [selected[t["instance_id"]] for t in suite["tasks"]]


def runtime_checks():
    checks = {name: shutil.which(name) for name in ("swegemma", "docker", "nvidia-smi")}
    for name, args in (("docker", ["info"]), ("nvidia-smi", ["--query-gpu=name,memory.total", "--format=csv,noheader"])):
        if checks[name]:
            try:
                result = subprocess.run([checks[name], *args], capture_output=True, text=True, timeout=15)
                checks[name + "_ready"] = result.returncode == 0
            except (OSError, subprocess.TimeoutExpired):
                checks[name + "_ready"] = False
        else:
            checks[name + "_ready"] = False
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=ROOT)
    parser.add_argument("--suite", type=Path, default=ROOT / "evaluation/smoke-suite.json")
    parser.add_argument("--output", type=Path, required=True, help="New directory for local data and report")
    args = parser.parse_args()
    suite = json.loads(args.suite.read_text(encoding="utf-8"))
    tasks = select_tasks(args.data_root / "tasks.jsonl", suite)
    snapshots = []
    for task in tasks:
        snapshot = args.data_root / "snapshots" / (task["instance_id"] + ".tgz")
        if not snapshot.is_file():
            parser.exit(1, f"Missing snapshot: {snapshot}\n")
        snapshots.append({"instance_id": task["instance_id"], "bytes": snapshot.stat().st_size})
    if args.output.exists():
        parser.exit(1, "Output already exists; choose a new directory to preserve prior runs.\n")
    args.output.mkdir(parents=True)
    subset = "".join(json.dumps(t, ensure_ascii=False) + "\n" for t in tasks)
    (args.output / "tasks.jsonl").write_text(subset, encoding="utf-8")
    checks = runtime_checks()
    blockers = []
    if not checks["swegemma"]:
        blockers.append("Official swegemma CLI is unavailable")
    if not checks["docker_ready"]:
        blockers.append("Docker daemon is unavailable")
    if not checks["nvidia-smi_ready"]:
        blockers.append("No functioning NVIDIA GPU runtime detected")
    report = {
        "suite": suite["name"], "platform": platform.system(), "architecture": platform.machine(),
        "task_count": len(tasks), "snapshots": snapshots,
        "subset_sha256": hashlib.sha256(subset.encode()).hexdigest(),
        "runtime": checks, "blockers": blockers,
        "model_server": "not_checked", "official_compiler": "not_run",
        "agent_evaluation": "not_run", "resolution_rate": None,
        "note": "Even if executable checks pass, verify model weights, serving, dependencies and sandbox image before evaluation.",
    }
    (args.output / "preflight.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
