"""Run with: python3 -m unittest discover tests  (needs a checkout of the source, see build/sources.json)."""
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

    def test_reviews_a_merge_rests_on_run_on_fable(self):
        """The two reviewers carry the model themselves, and the review skill names it when it dispatches."""
        for agent in ('code-reviewer', 'function-reviewer'):
            front = (PLUGIN / 'agents' / f'{agent}.md').read_text().split('---')[1]
            self.assertIn('\nmodel: fable\n', front, agent)
        self.assertIn('both on `fable`', (PLUGIN / 'skills' / 'review' / 'SKILL.md').read_text())
        rule = (PLUGIN / 'WORKFLOW.md').read_text().split('## Model rule')[1].split('\n## ')[0]
        self.assertIn('`fable` for the reviews a merge rests on', rule)

    def test_review_adds_the_other_vendor_only_where_it_is_installed(self):
        review = (PLUGIN / 'skills' / 'review' / 'SKILL.md').read_text()
        self.assertIn('only where the machine has one', review)
        self.assertIn('never blocks a merge by being absent', review.replace('\n  ', ' '))
        cross = (PLUGIN / 'skills' / 'cross-review' / 'SKILL.md').read_text()
        self.assertIn("command -v codex", cross)

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
