import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install_gpu_environment import create_environment


class EnvironmentCreationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.target = Path(self.directory.name) / 'environment'

    @patch('install_gpu_environment.subprocess.run')
    @patch('install_gpu_environment.importlib.util.find_spec', return_value=object())
    def test_standard_venv_when_ensurepip_exists(self, find_spec, run):
        create_environment(self.target)
        find_spec.assert_called_once_with('ensurepip')
        run.assert_called_once_with(
            [sys.executable, '-m', 'venv', str(self.target)], check=True)

    @patch('install_gpu_environment.subprocess.run')
    @patch('install_gpu_environment.importlib.util.find_spec',
           side_effect=[None, object()])
    def test_virtualenv_without_ensurepip(self, find_spec, run):
        create_environment(self.target)
        run.assert_called_once_with(
            [sys.executable, '-m', 'virtualenv', '--python', sys.executable,
             str(self.target)], check=True)

    @patch('install_gpu_environment.subprocess.run')
    @patch('install_gpu_environment.importlib.util.find_spec', return_value=None)
    def test_missing_creator_stops_before_creating_directory(self, find_spec, run):
        with self.assertRaisesRegex(RuntimeError, 'requirements-setup.txt'):
            create_environment(self.target)
        run.assert_not_called()
        self.assertFalse(self.target.exists())

    @patch('install_gpu_environment.subprocess.run')
    def test_existing_directory_is_preserved(self, run):
        self.target.mkdir()
        marker = self.target / 'marker'
        marker.write_text('preserve')
        with self.assertRaisesRegex(ValueError, 'not overwritten'):
            create_environment(self.target)
        run.assert_not_called()
        self.assertEqual(marker.read_text(), 'preserve')

    @patch('install_gpu_environment.subprocess.run',
           side_effect=subprocess.CalledProcessError(1, ['creator']))
    @patch('install_gpu_environment.importlib.util.find_spec', return_value=object())
    def test_creator_failure_is_propagated(self, find_spec, run):
        with self.assertRaises(subprocess.CalledProcessError):
            create_environment(self.target)


if __name__ == '__main__':
    unittest.main()
