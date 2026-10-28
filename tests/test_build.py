"""Run with: python3 -m unittest discover tests  (needs checkouts of the two sources, see build/sources.json)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / 'plugins' / 'tc-workflow'


class BuildTest(unittest.TestCase):
    def test_committed_plugin_matches_a_fresh_build(self):
        r = subprocess.run([sys.executable, str(ROOT / 'build' / 'build.py'), '--check'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_marketplace_points_at_the_plugin(self):
        m = json.loads((ROOT / '.claude-plugin' / 'marketplace.json').read_text())
        self.assertEqual([p['source'] for p in m['plugins']], ['./plugins/tc-workflow'])
        self.assertEqual(json.loads((PLUGIN / '.claude-plugin' / 'plugin.json').read_text())['name'], 'tc-workflow')

    def test_no_links_ship(self):
        self.assertEqual([p for p in PLUGIN.rglob('*') if p.is_symlink()], [])

    def test_credential_guard_suite(self):
        r = subprocess.run(['bash', str(PLUGIN / 'hooks' / 'test-credential-guard.sh')], capture_output=True, text=True,
                           cwd=PLUGIN)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])

    def test_clean_check_catches_a_leak(self):
        sys.path.insert(0, str(ROOT / 'build'))
        import build
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / 'skills' / 'x').mkdir(parents=True)
            (out / 'skills' / 'x' / 'SKILL.md').write_text('Send it to Ringer on the Runway app.\n')
            with self.assertRaises(SystemExit):
                build.clean_check(out)


if __name__ == '__main__':
    unittest.main()
