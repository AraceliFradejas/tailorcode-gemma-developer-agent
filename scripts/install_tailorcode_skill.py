"""Install the repository skill into a chosen project; never overwrite a skill."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'skills' / 'tailorcode'
LOCATIONS = {'codex': '.agents', 'claude': '.claude'}


def install(project: Path, target: str) -> Path:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f'Project directory does not exist: {project}')
    destination = project / LOCATIONS[target] / 'skills' / 'tailorcode'
    # A broken symlink is also an existing installation; do not follow it.
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Preserving existing installation: {destination}')
    # Copy only portable resources for Claude, plus Codex UI metadata for Codex.
    shutil.copytree(SOURCE, destination,
                    ignore=shutil.ignore_patterns('agents') if target == 'claude' else None)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=LOCATIONS, required=True)
    parser.add_argument('--project', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(install(args.project, args.target))
    except (ValueError, FileExistsError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
