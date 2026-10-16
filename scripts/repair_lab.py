"""Prepare and check trusted educational fixtures, without a model or network."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CASES = Path(__file__).resolve().parents[1] / 'examples' / 'repair-lab'
CASE_NAMES = ('independent-lists', 'zero-price', 'inclusive-range')


def prepare(case: str, workspace: Path) -> None:
    if workspace.exists() or workspace.is_symlink():
        raise FileExistsError(f'Workspace already exists; preserving it: {workspace}')
    shutil.copytree(CASES / case, workspace)


def check(case: str, workspace: Path) -> subprocess.CompletedProcess:
    workspace = workspace.resolve()
    if not workspace.is_dir():
        raise ValueError(f'Workspace does not exist: {workspace}')
    expected = CASES / case / 'test_repair_target.py'
    actual = workspace / expected.name
    if not actual.is_file() or actual.read_bytes() != expected.read_bytes():
        raise ValueError('Acceptance tests changed or missing; restore the original tests.')
    # Run the known test file, not arbitrary test-discovery patterns. This executes
    # local Python, including the candidate module; it is NOT an isolation sandbox.
    return subprocess.run(
        [sys.executable, '-I', '-B', '-c',
         "import runpy, sys; from pathlib import Path; "
         "test = sys.argv.pop(1); sys.path.insert(0, str(Path(test).parent)); "
         "runpy.run_path(test, run_name='__main__')", str(actual), '-v'],
        cwd=workspace, capture_output=True, text=True, timeout=30,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'check'))
    parser.add_argument('--case', choices=CASE_NAMES, required=True)
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == 'prepare':
            prepare(args.case, args.workspace)
            print(f'Prepared {args.case}: {args.workspace.resolve()}')
        else:
            result = check(args.case, args.workspace)
            print(result.stdout, end='')
            print(result.stderr, end='', file=sys.stderr)
            raise SystemExit(result.returncode)
    except (ValueError, FileExistsError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
