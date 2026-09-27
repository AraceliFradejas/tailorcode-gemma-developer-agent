"""Run the trusted project packaging notebook in a temporary directory.

This verifies notebook execution and archive contents, not agent compilation or
benchmark performance. Requires only the Python standard library.
"""
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "deliverables" / "tailorcode-submit-ready.ipynb"


def main():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    source = "\n\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )
    with tempfile.TemporaryDirectory(prefix="tailorcode-check-") as directory:
        for _ in range(2):
            subprocess.run(
                [sys.executable, "-I", "-c", source],
                cwd=directory, check=True, timeout=60, capture_output=True, text=True,
            )
            archive_path = Path(directory) / "submission.zip"
            if Path("/kaggle").is_dir():
                archive_path = Path("/kaggle/working/submission.zip")
            with zipfile.ZipFile(archive_path) as archive:
                expected = {"agent.yaml", "eval_config.yaml", "sub_agents/code_analyzer.yaml"}
                assert set(archive.namelist()) == expected
                assert archive.testzip() is None
                for name in ("agent.yaml", "sub_agents/code_analyzer.yaml"):
                    config = archive.read(name).decode("utf-8")
                    assert "model: gemma-4-31b-it-qat-w4a16-ct" in config
                    assert "!include" not in config
    print("PASS: complete notebook execution twice; archive contents verified.")
    print("Agent compilation and benchmark evaluation were not run.")


if __name__ == "__main__":
    main()
