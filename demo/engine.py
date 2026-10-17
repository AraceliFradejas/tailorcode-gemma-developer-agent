"""Run only the repository's known price example and its acceptance tests."""
from pathlib import Path
import difflib
import runpy
import tempfile

from demo.verified_price import effective_price
from scripts.repair_lab import check, prepare

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_PATH = ROOT / 'examples/repair-lab/zero-price/repair_target.py'
CORRECTED_PATH = ROOT / 'demo/verified_price.py'


def sources():
    return ORIGINAL_PATH.read_text(), CORRECTED_PATH.read_text()


def compare(price, fallback):
    original = runpy.run_path(str(ORIGINAL_PATH))['effective_price']
    return original(price, fallback), effective_price(price, fallback)


def patch():
    before, after = sources()
    return ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                      fromfile='a/repair_target.py', tofile='b/repair_target.py'))


def run_checks():
    with tempfile.TemporaryDirectory(prefix='tailorcode-demo-') as directory:
        workspace = Path(directory) / 'case'
        prepare('zero-price', workspace)
        before = check('zero-price', workspace)
        (workspace / 'repair_target.py').write_text(CORRECTED_PATH.read_text())
        after = check('zero-price', workspace)
    return {'before': {'exit_code': before.returncode, 'output': before.stdout + before.stderr},
            'after': {'exit_code': after.returncode, 'output': after.stdout + after.stderr}}
