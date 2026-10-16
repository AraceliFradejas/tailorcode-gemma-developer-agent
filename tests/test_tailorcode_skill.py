"""Verify fixture behavior and installation, not claims about agent quality."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install_tailorcode_skill import install
from repair_lab import CASE_NAMES, check, prepare

# Hand-written reference corrections for validating the exercise harness only.
# These are never passed to a model in the comparison protocol.
FIXES = {
    'independent-lists': 'def add_label(label, labels=None):\n    if labels is None:\n        labels = []\n    labels.append(label)\n    return labels\n',
    'zero-price': 'def effective_price(price, fallback):\n    return fallback if price is None else price\n',
    'inclusive-range': 'def even_numbers(start, end):\n    return [number for number in range(start, end + 1) if number % 2 == 0]\n',
}


class SkillLabTests(unittest.TestCase):
    def test_each_original_fails_assertions_and_reference_correction_passes(self):
        for case in CASE_NAMES:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / 'case'
                prepare(case, workspace)
                before = check(case, workspace)
                self.assertNotEqual(before.returncode, 0)
                self.assertIn('AssertionError', before.stderr)
                self.assertNotIn('ImportError', before.stderr)
                (workspace / 'repair_target.py').write_text(FIXES[case])
                after = check(case, workspace)
                self.assertEqual(after.returncode, 0, after.stderr)
                self.assertIn('OK', after.stderr)

    def test_changed_acceptance_tests_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / 'case'
            prepare(CASE_NAMES[0], workspace)
            (workspace / 'test_repair_target.py').write_text('print("OK")\n')
            with self.assertRaisesRegex(ValueError, 'Acceptance tests'):
                check(CASE_NAMES[0], workspace)

    def test_existing_workspace_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / 'keep.txt').write_text('user work')
            with self.assertRaises(FileExistsError):
                prepare(CASE_NAMES[0], workspace)
            self.assertEqual((workspace / 'keep.txt').read_text(), 'user work')

    def test_installs_portable_instructions_for_both_targets_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for target in ('codex', 'claude'):
                destination = install(project, target)
                self.assertEqual((destination / 'SKILL.md').read_bytes(),
                                 (ROOT / 'skills/tailorcode/SKILL.md').read_bytes())
                self.assertTrue((destination / 'references/explanation.md').is_file())
                self.assertEqual((destination / 'agents/openai.yaml').exists(), target == 'codex')
                (destination / 'SKILL.md').write_text('user version')
                with self.assertRaises(FileExistsError):
                    install(project, target)
                self.assertEqual((destination / 'SKILL.md').read_text(), 'user version')



if __name__ == '__main__':
    unittest.main()
