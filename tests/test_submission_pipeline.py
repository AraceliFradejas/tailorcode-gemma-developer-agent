"""Regression checks for packaging mistakes that can waste Kaggle submissions."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_submission import load_files, render_notebook, validate
from prepare_evaluation import select_tasks


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.files = load_files(ROOT / "agents/baseline")

    def test_baseline_and_saved_notebook_match(self):
        validate(self.files)
        self.assertEqual(render_notebook(self.files),
                         (ROOT / "deliverables/tailorcode-submit-ready.ipynb").read_text())

    def test_rejects_common_submission_failures(self):
        cases = []
        missing = self.files.copy()
        del missing["agent.yaml"]
        cases.append(missing)
        for old, new in [
            ("gemma-4-31b-it-qat-w4a16-ct", "wrong-model"),
            ("  - submit_patch", "  - unknown_tool"),
            ("sub_agents/code_analyzer.yaml", "../outside.yaml"),
            ("max_output_tokens: 16384", "max_output_tokens: 999999"),
        ]:
            broken = self.files.copy()
            broken["agent.yaml"] = broken["agent.yaml"].replace(old, new)
            cases.append(broken)
        duplicate = self.files.copy()
        duplicate["agent.yaml"] += "name: overwritten\n"
        cases.append(duplicate)
        mutable = self.files.copy()
        mutable["sub_agents/code_analyzer.yaml"] = mutable["sub_agents/code_analyzer.yaml"].replace("  - read_file", "  - write_file")
        cases.append(mutable)
        for i, files in enumerate(cases):
            with self.subTest(case=i), self.assertRaises(ValueError):
                validate(files)

    def test_zip_is_reproducible_and_matches_sources(self):
        notebook = json.loads(render_notebook(self.files))
        code = "\n".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code")
        archives = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as directory:
                subprocess.run([sys.executable, "-I", "-c", code], cwd=directory,
                               check=True, timeout=30, capture_output=True)
                path = Path("/kaggle/working/submission.zip") if Path("/kaggle").is_dir() else Path(directory) / "submission.zip"
                archives.append(path.read_bytes())
                with zipfile.ZipFile(path) as archive:
                    self.assertEqual(set(archive.namelist()), set(self.files))
                    for name, content in self.files.items():
                        self.assertEqual(archive.read(name).decode(), content)
        self.assertEqual(*archives)

    def test_task_selection_preserves_order_and_detects_wrong_dataset(self):
        suite = {"tasks": [{"instance_id": "a", "repo": "one", "base_commit": "abc"},
                           {"instance_id": "b", "repo": "two", "base_commit": "def"}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.jsonl"
            path.write_text("\n".join(json.dumps(t) for t in reversed(suite["tasks"])))
            self.assertEqual(select_tasks(path, suite), suite["tasks"])
            wrong = copy.deepcopy(suite)
            wrong["tasks"][0]["base_commit"] = "unexpected"
            with self.assertRaisesRegex(ValueError, "Dataset mismatch"):
                select_tasks(path, wrong)
            path.write_text(json.dumps(suite["tasks"][0]) + "\n")
            with self.assertRaisesRegex(ValueError, "Missing tasks"):
                select_tasks(path, suite)


if __name__ == "__main__":
    unittest.main()
