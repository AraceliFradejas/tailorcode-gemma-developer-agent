"""Run the repository's two known examples and their acceptance tests."""
from pathlib import Path
import difflib
import runpy
import tempfile

from demo.verified_price import effective_price
from scripts.repair_lab import check, prepare

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_PATH = ROOT / 'examples/repair-lab/zero-price/repair_target.py'
CORRECTED_PATH = ROOT / 'demo/verified_price.py'
CASES = {
    'zero-price': (ORIGINAL_PATH, CORRECTED_PATH),
    'independent-lists': (ROOT / 'examples/repair-lab/independent-lists/repair_target.py',
                          ROOT / 'demo/verified_labels.py'),
}


def sources(case='zero-price'):
    original, corrected = CASES[case]
    return original.read_text(), corrected.read_text()


def compare(price, fallback):
    original = runpy.run_path(str(ORIGINAL_PATH))['effective_price']
    return original(price, fallback), effective_price(price, fallback)


def patch(case='zero-price'):
    before, after = sources(case)
    return ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                      fromfile='a/repair_target.py', tofile='b/repair_target.py'))


def run_checks(case='zero-price'):
    with tempfile.TemporaryDirectory(prefix='tailorcode-demo-') as directory:
        workspace = Path(directory) / 'case'
        prepare(case, workspace)
        before = check(case, workspace)
        (workspace / 'repair_target.py').write_text(CASES[case][1].read_text())
        after = check(case, workspace)
    return {'before': {'exit_code': before.returncode, 'output': before.stdout + before.stderr},
            'after': {'exit_code': after.returncode, 'output': after.stdout + after.stderr}}


def basket_trace(first_item, second_item):
    """Fresh function definitions per simulation prevent cross-visitor list sharing."""
    traces = {}
    for version, path in zip(('before', 'after'), CASES['independent-lists']):
        add = runpy.run_path(str(path))['add_label']
        first = add(first_item)
        first_snapshot = list(first)
        second = add(second_item)
        traces[version] = {'first_after_own_purchase': first_snapshot,
                           'first_final': list(first), 'second_final': list(second),
                           'same_basket': first is second}
    return traces
