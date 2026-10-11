import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_colab_inputs import MODEL_FILES, prepare_task, validate_model


class ColabInputTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.task = {"instance_id": "a", "repo": "owner/repo", "base_commit": "abc"}
        self.cached = self.root / "cached"
        self.cached.write_text(json.dumps(self.task) + "\n")
        self.manifest = {
            "task": self.task,
            "files": [{
                "path": "tasks.jsonl", "bytes": self.cached.stat().st_size,
                "sha256": hashlib.sha256(self.cached.read_bytes()).hexdigest(),
            }],
        }

    def test_verified_task_can_resume_without_downloading_again(self):
        output = self.root / "data"
        download = Mock(return_value=str(self.cached))
        report = prepare_task(self.manifest, output, download)
        self.assertEqual(report["inference"], "not_run")
        self.assertTrue((output / "input-check.json").is_file())
        download.reset_mock()
        prepare_task(self.manifest, output, download)
        download.assert_not_called()

    def test_changed_download_is_not_copied(self):
        self.cached.write_text("changed")
        output = self.root / "data"
        with self.assertRaisesRegex(ValueError, "does not match pinned"):
            prepare_task(self.manifest, output, Mock(return_value=str(self.cached)))
        self.assertFalse((output / "tasks.jsonl").exists())

    def test_existing_mismatch_is_preserved(self):
        output = self.root / "data"
        output.mkdir()
        (output / "tasks.jsonl").write_text("preserve")
        with self.assertRaisesRegex(ValueError, "Existing input"):
            prepare_task(self.manifest, output, Mock())
        self.assertEqual((output / "tasks.jsonl").read_text(), "preserve")

    def test_wrong_task_identity_fails_after_hash_verification(self):
        self.manifest["task"] = {**self.task, "base_commit": "wrong"}
        with self.assertRaisesRegex(ValueError, "task identity"):
            prepare_task(self.manifest, self.root / "data", Mock(return_value=str(self.cached)))
        self.assertFalse((self.root / "data/input-check.json").exists())

    def test_parent_traversal_is_rejected(self):
        self.manifest["files"][0]["path"] = "../outside"
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            prepare_task(self.manifest, self.root / "data", Mock())

    def test_model_requires_tokenizer_and_compressed_configuration(self):
        directory = self.root / "model"
        directory.mkdir()
        for name in MODEL_FILES:
            (directory / name).write_text("present")
        (directory / "config.json").write_text(json.dumps({
            "architectures": ["Gemma4ForConditionalGeneration"],
            "quantization_config": {
                "quant_method": "compressed-tensors", "quantization_status": "compressed",
            },
        }))
        self.assertEqual(validate_model(directory)["inference"], "not_run")
        (directory / "tokenizer.json").unlink()
        with self.assertRaisesRegex(ValueError, "tokenizer.json"):
            validate_model(directory)

    def test_no_flags_means_no_download_or_output(self):
        output = self.root / "data"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/prepare_colab_inputs.py"),
             "--output", str(output)], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Downloads disabled", result.stderr)
        self.assertFalse(output.exists())

    def test_manifest_contains_only_required_task_assets_and_wheels(self):
        manifest = json.loads((ROOT / "evaluation/colab-inputs.json").read_text())
        paths = {entry["path"] for entry in manifest["files"]}
        self.assertEqual(len(paths), len(manifest["files"]))
        self.assertIn("snapshots/fastapi_14786.tgz", paths)
        self.assertTrue(all(
            name in {
                "tasks.jsonl", "snapshots/fastapi_14786.tgz", "sandbox/setup.py",
                f"graphs/fastapi_{manifest['task']['base_commit']}.json",
                f"embeddings/fastapi_{manifest['task']['base_commit']}.npz",
            } or (name.startswith("wheels/") and name.endswith(".whl"))
            for name in paths
        ))


if __name__ == "__main__":
    unittest.main()
