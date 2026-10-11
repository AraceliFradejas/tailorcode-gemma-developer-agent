"""Opt-in pinned public inputs for a Colab diagnostic run, never inference.

Task files are checked against the locally inspected public competition inputs.
Downloading the model separately requests the full pinned version (~23.3 GB).
Run only after approving the runtime consumption and downloads.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "google/gemma-4/other/gemma-4-31b-it-qat-w4a16-ct/2"
MODEL_FILES = (
    "config.json", "generation_config.json", "model.safetensors",
    "tokenizer.json", "tokenizer_config.json", "chat_template.jinja",
    "processor_config.json",
)


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_task(manifest, output, download):
    output.mkdir(parents=True, exist_ok=True)
    for entry in manifest["files"]:
        name = entry["path"]
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe manifest path: {name}")
        destination = output / relative
        if destination.is_symlink():
            raise ValueError(f"Refusing symlink input: {name}")
        if destination.exists():
            if not destination.is_file() or file_hash(destination) != entry["sha256"]:
                raise ValueError(f"Existing input does not match: {name}; preserve and inspect it.")
        else:
            print(f"Downloading task input: {name}", flush=True)
            cached = Path(download("gemma-4-developer-agent", path=name))
            if cached.stat().st_size != entry["bytes"] or file_hash(cached) != entry["sha256"]:
                raise ValueError(f"Downloaded input does not match pinned manifest: {name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cached, destination)
        print(f"Verified: {name}", flush=True)
    expected = manifest["task"]
    matches = []
    with (output / "tasks.jsonl").open(encoding="utf-8") as source:
        for line in source:
            task = json.loads(line)
            if task.get("instance_id") == expected["instance_id"]:
                matches.append(task)
    if len(matches) != 1 or any(matches[0].get(k) != v for k, v in expected.items()):
        raise ValueError("Downloaded task identity does not match the pinned public task.")
    report = {
        "task": expected, "verified_files": len(manifest["files"]),
        "manifest_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest(),
        "data_root": str(output.resolve()), "inference": "not_run",
    }
    (output / "input-check.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def validate_model(directory):
    for name in MODEL_FILES:
        path = directory / name
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"Missing or empty model input: {name}")
    config = json.loads((directory / "config.json").read_text())
    quantization = config.get("quantization_config", {})
    if config.get("architectures") != ["Gemma4ForConditionalGeneration"]:
        raise ValueError("Unexpected model architecture")
    if (quantization.get("quant_method"), quantization.get("quantization_status")) != (
        "compressed-tensors", "compressed",
    ):
        raise ValueError("Unexpected model quantization")
    return {
        "handle": MODEL, "model_path": str(directory.resolve()),
        "required_files_present": list(MODEL_FILES),
        "note": "File presence and configuration checked, not a full weight integrity or GPU serving check.",
        "inference": "not_run",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--download-task", action="store_true")
    parser.add_argument("--download-model", action="store_true")
    args = parser.parse_args()
    if not args.download_task and not args.download_model:
        parser.exit(2, "Downloads disabled. Approve runtime and downloads before opting in.\n")
    manifest = json.loads((ROOT / "evaluation/colab-inputs.json").read_text())
    required_bytes = sum(e["bytes"] for e in manifest["files"]) if args.download_task else 0
    if args.download_model:
        required_bytes += 24 * 1024**3
    args.output.mkdir(parents=True, exist_ok=True)
    # Cache and task copies can coexist; also leave headroom for installation.
    if shutil.disk_usage(args.output).free < required_bytes * 2 + 5 * 1024**3:
        parser.exit(1, "Insufficient free disk headroom. No downloads started.\n")
    import kagglehub

    if args.download_task:
        print(json.dumps(prepare_task(manifest, args.output, kagglehub.competition_download), indent=2))
    if args.download_model:
        print("Downloading full pinned model (~23.3 GB); no inference.", flush=True)
        model_path = Path(kagglehub.model_download(MODEL))
        report = validate_model(model_path)
        (args.output / "model-check.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
    print("Input preparation finished. No repository code or model was executed.")


if __name__ == "__main__":
    main()
