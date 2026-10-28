#!/usr/bin/env python3
"""Build the tc-workflow plugin from pinned public sources plus the TC-owned overlay.

    python3 build/build.py                     # write plugins/tc-workflow/
    python3 build/build.py --check             # build to a temp dir, fail if plugins/ differs
    python3 build/build.py --pm-sp-src PATH --agent-runway-src PATH

Steps, in order, every one fatal on failure:
1. Export each source at its pinned commit with `git archive` (tracked files only; symlinks refused).
2. Copy only the files build/files.json allows.
3. Apply build/phrases.json: per-file edits first (each must match), then global token swaps (each must match
   somewhere). A miss means upstream moved: read it, then fix the map or own the file in overlay/.
4. Copy overlay/ on top (files the TC edition owns outright).
5. Clean check: no output file may match build/banned.json, except where that file allows it.
6. Validate JSON and skill front matter, then write BUILD-INFO.json (inputs and an output digest).

The output is never edited by hand. Change the map, the overlay or a pinned commit, then rebuild.
"""
import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'build'
OVERLAY = ROOT / 'overlay'
OUT = ROOT / 'plugins' / 'tc-workflow'


def fail(msg):
    print(f'build: FAIL: {msg}', file=sys.stderr)
    sys.exit(1)


def load(name):
    return json.loads((BUILD / name).read_text())


def export(src, commit, subdir, dest):
    """Tracked files of src/subdir at commit into dest. Refuses links and anything outside subdir."""
    try:
        data = subprocess.run(['git', '-C', str(src), 'archive', '--format=tar', commit, subdir],
                              check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as e:
        fail(f'git archive {commit} {subdir} in {src}: {e.stderr.decode().strip()}')
    prefix = subdir.rstrip('/') + '/'
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for m in tar.getmembers():
            if m.issym() or m.islnk():
                fail(f'{src}:{m.name} is a link; links never ship')
            if m.isdir():
                continue
            if not m.name.startswith(prefix) or '..' in Path(m.name).parts:
                fail(f'{src}:{m.name} is outside {subdir}')
            target = dest / m.name[len(prefix):]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(tar.extractfile(m).read())
            target.chmod(0o755 if m.mode & 0o111 else 0o644)


def take(exports, out):
    for entry in load('files.json')['take']:
        source, path = entry['from'].split(':', 1)
        base = exports[source]
        if path.endswith('/'):
            files = sorted(p for p in (base / path).rglob('*') if p.is_file()) if (base / path).is_dir() else []
            if not files:
                fail(f'{entry["from"]} matched nothing')
            for f in files:
                dst = out / entry['to'] / f.relative_to(base / path)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
        else:
            if not (base / path).is_file():
                fail(f'{entry["from"]} is missing')
            dst = out / entry['to']
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(base / path, dst)


def text_files(out):
    for p in sorted(out.rglob('*')):
        if p.is_file():
            try:
                yield p, p.read_text()
            except UnicodeDecodeError:
                continue


def apply_phrases(out):
    phrases = load('phrases.json')
    for e in phrases['edits']:
        p = out / e['file']
        if not p.is_file():
            fail(f'phrase map names {e["file"]}, which is not in the build')
        text = p.read_text()
        if e['old'] not in text:
            fail(f'phrase not found in {e["file"]}: {e["old"][:80]!r}')
        p.write_text(text.replace(e['old'], e['new']))
    hits = {t['old']: 0 for t in phrases['tokens']}
    for p, text in text_files(out):
        new = text
        for t in phrases['tokens']:
            n = new.count(t['old'])
            if n:
                hits[t['old']] += n
                new = new.replace(t['old'], t['new'])
        if new != text:
            p.write_text(new)
    missed = [k for k, v in hits.items() if not v]
    if missed:
        fail(f'global tokens matched nothing: {missed}')


def overlay(out):
    for f in sorted(OVERLAY.rglob('*')):
        if f.is_symlink():
            fail(f'overlay/{f.relative_to(OVERLAY)} is a link')
        if f.is_file() and f.name != '.DS_Store':
            dst = out / f.relative_to(OVERLAY)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)


def clean_check(out):
    banned = load('banned.json')
    problems = []
    for p, text in text_files(out):
        rel = str(p.relative_to(out))
        for rule in banned['rules']:
            if any(re.fullmatch(a, rel) for a in rule.get('allow_in', [])):
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if re.search(rule['pattern'], line, re.I):
                    problems.append(f'{rel}:{i}: [{rule["why"]}] {line.strip()[:120]}')
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        fail(f'clean check: {len(problems)} line(s) above must not ship')


def validate(out):
    for p in out.rglob('*.json'):
        try:
            json.loads(p.read_text())
        except ValueError as e:
            fail(f'{p.relative_to(out)} is not valid JSON: {e}')
    names = set()
    for skill in sorted((out / 'skills').glob('*/SKILL.md')):
        head = skill.read_text().split('---')
        m = re.search(r'^name:\s*(\S+)', head[1] if len(head) > 2 else '', re.M)
        if not m or m.group(1) != skill.parent.name:
            fail(f'{skill.relative_to(out)}: front matter name must be {skill.parent.name}')
        if not re.search(r'^description:', head[1], re.M):
            fail(f'{skill.relative_to(out)}: no description')
        names.add(m.group(1))
    for ref in sorted({r for _, t in text_files(out) for r in re.findall(r'tc-workflow:([a-z0-9-]+)', t)}):
        if ref not in names and not any((out / d / f'{ref}.md').is_file() for d in ('agents', 'commands')):
            fail(f'tc-workflow:{ref} is referenced but no such skill or agent ships')


def digest(out):
    h = hashlib.sha256()
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name != 'BUILD-INFO.json':
            h.update(str(p.relative_to(out)).encode() + b'\0' + p.read_bytes() + b'\0')
    return h.hexdigest()


def build(dest, srcs):
    sources = {k: v for k, v in load('sources.json').items() if not k.startswith('_')}
    with tempfile.TemporaryDirectory() as tmp:
        exports = {}
        for name, s in sources.items():
            exports[name] = Path(tmp) / name
            export(srcs[name], s['commit'], s['subdir'], exports[name])
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        take(exports, dest)
    apply_phrases(dest)
    overlay(dest)
    clean_check(dest)
    validate(dest)
    info = {'sources': {k: {'url': v['url'], 'commit': v['commit'], 'subdir': v['subdir']} for k, v in sources.items()},
            'output_sha256': digest(dest)}
    (dest / 'BUILD-INFO.json').write_text(json.dumps(info, indent=2) + '\n')
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='fail if plugins/tc-workflow differs from a fresh build')
    sources = {k: v for k, v in load('sources.json').items() if not k.startswith('_')}
    for name in sources:
        ap.add_argument(f'--{name}-src', help=f'checkout of {sources[name]["url"]}')
    args = ap.parse_args()
    srcs = {}
    for name, s in sources.items():
        given = getattr(args, f'{name.replace("-", "_")}_src')
        srcs[name] = Path(given) if given else (ROOT / s['default_checkout']).resolve()
        if not (srcs[name] / '.git').exists():
            fail(f'no git checkout of {s["url"]} at {srcs[name]} (pass --{name}-src)')
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            info = build(Path(tmp) / 'tc-workflow', srcs)
            if not (OUT / 'BUILD-INFO.json').is_file():
                fail('plugins/tc-workflow has never been built')
            have = digest(OUT)
            if have != info['output_sha256']:
                fail('plugins/tc-workflow differs from a fresh build: rebuild, never edit it by hand')
        print(f'build: check OK ({info["output_sha256"][:12]})')
        return
    info = build(OUT, srcs)
    print(f'build: OK, plugins/tc-workflow ({info["output_sha256"][:12]})')


if __name__ == '__main__':
    main()
