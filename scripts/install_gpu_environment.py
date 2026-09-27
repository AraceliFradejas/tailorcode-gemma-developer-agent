"""Install a candidate GPU stack in a NEW, isolated Linux Python 3.12 venv.

Run only on an already approved runtime. Does not start a model or cloud VM.
PyPI dependency downloads may be several GB; environment compatibility remains
unverified until resolution, pip check, imports and a real GPU run succeed.
"""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verified_wheels(directory):
    manifest = json.loads((ROOT / 'evaluation/official-harness-wheels.json').read_text())
    paths = []
    for entry in manifest['files']:
        path = directory / entry['name']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f'Missing or changed official wheel: {path.name}')
        paths.append(str(path.resolve()))
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheelhouse', type=Path, required=True)
    parser.add_argument('--venv', type=Path, required=True)
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    if not args.install:
        parser.exit(2, 'Installation disabled; review runtime consumption before using --install.\n')
    if (platform.system(), platform.machine(), sys.version_info[:2]) != ('Linux', 'x86_64', (3, 12)):
        parser.exit(1, 'Use an approved Linux x86_64 Python 3.12 runtime. No installation started.\n')
    wheels = verified_wheels(args.wheelhouse)
    if args.venv.exists():
        parser.exit(1, 'Choose a new venv path; existing environments are not overwritten.\n')
    subprocess.run([sys.executable, '-m', 'venv', str(args.venv)], check=True)
    python = str(args.venv.resolve() / 'bin/python')
    subprocess.run([python, '-m', 'pip', 'install', '--disable-pip-version-check',
                    '-r', str(ROOT / 'requirements-gpu.txt'), *wheels], check=True)
    subprocess.run([python, '-m', 'pip', 'check'], check=True)
    subprocess.run([python, '-c', 'import torch, vllm, swegemma, adk_submission; '
                    'print("Imports passed; CUDA available:", torch.cuda.is_available())'], check=True)
    frozen = subprocess.check_output([python, '-m', 'pip', 'freeze'], text=True)
    (args.venv / 'installed-packages.txt').write_text(frozen)
    print('Environment prepared:', python)
    print('No model started. Run the input/GPU preflight separately.')


if __name__ == '__main__':
    main()
