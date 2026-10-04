import sys
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_smoke_environment import compatibility_issues


class SmokeEnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.packages = {'swegemma': '0.2.7', 'adk-submission': '0.2.11',
                         'adk-eval-core': '0.1.0', 'google-adk': '1.36.1', 'vllm': '0.19.1'}

    def test_python_313_is_blocked_even_with_gpu(self):
        errors = compatibility_issues('Linux', 'x86_64', (3, 13), self.packages, True)
        self.assertTrue(any('Python 3.12' in error for error in errors))

    def test_new_adk_major_is_blocked(self):
        self.packages['google-adk'] = '2.7.1'
        self.assertTrue(compatibility_issues('Linux', 'x86_64', (3, 12), self.packages, True))

    def test_matching_basic_environment_does_not_require_docker(self):
        self.assertEqual(compatibility_issues('Linux', 'x86_64', (3, 12), self.packages, True), [])

    def test_mac_cpu_is_not_mistaken_for_gpu_host(self):
        errors = compatibility_issues('Darwin', 'arm64', (3, 12), {}, False)
        self.assertTrue(any('Linux' in error for error in errors))
        self.assertTrue(any('GPU' in error for error in errors))

    def test_runner_does_nothing_without_explicit_opt_in(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            result = subprocess.run([
                sys.executable, str(root / 'scripts/run_public_smoke.py'),
                '--data-root', directory, '--model-path', directory, '--output', str(output),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('requires --run-agent', result.stderr)
            self.assertFalse(output.exists())

    def test_notebook_is_valid_python_and_stops_before_setup(self):
        root = Path(__file__).resolve().parents[1]
        notebook = json.loads((root / 'notebooks/tailorcode-public-smoke.ipynb').read_text())
        cells = [''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type'] == 'code']
        for cell in cells:
            compile(cell, '<smoke-notebook>', 'exec')
        with self.assertRaisesRegex(RuntimeError, 'approve runtime'):
            exec(cells[0], {})

    def test_guided_notebook_requires_approval_before_each_step(self):
        root = Path(__file__).resolve().parents[1]
        notebook = json.loads((root / 'notebooks/tailorcode-public-smoke.ipynb').read_text())
        ids = [cell['id'] for cell in notebook['cells']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertLess(ids.index('project-setup'), ids.index('install-environment'))
        self.assertLess(ids.index('a58JyR6YS5sU'), ids.index('Vv3-uZkxRhom'))
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                with self.subTest(cell=cell['id']):
                    self.assertEqual(cell['outputs'], [])
                    with self.assertRaises(RuntimeError):
                        exec(''.join(cell['source']), {})

    def test_evaluation_uses_isolated_interpreter(self):
        root = Path(__file__).resolve().parents[1]
        notebook = json.loads((root / 'notebooks/tailorcode-public-smoke.ipynb').read_text())
        cells = {cell['id']: ''.join(cell['source']) for cell in notebook['cells']}
        for cell_id in ('tailorcode-smoke-06', 'tailorcode-smoke-08'):
            self.assertIn('str(PYTHON)', cells[cell_id])
            self.assertNotIn('sys.executable', cells[cell_id])
        self.assertIn('RUN_AGENT = False', cells['tailorcode-smoke-08'])
        self.assertIn('INSTALL_APPROVED = False', cells['install-environment'])


if __name__ == '__main__':
    unittest.main()
