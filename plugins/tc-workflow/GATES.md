# Gates and review policy

Repo-level enforcement kits. The workflow skills run the session: shaping,
tickets, verification, delivery. This half holds what the session leaves to
deterministic tools: gates a session cannot talk its way past, and a written
review policy read by a reviewer that did not write the change.

It uses Claude Code features only, so the same kit works in a repo that uses
none of the other skills.

```
skills, CLAUDE.md      advise      nothing makes a session comply
       │
gate-hooks             enforce     one script and one config, in the repo
review-policy          re-check    REVIEW.md, read by a fresh reviewer
       │
managed settings       lock        the admin's layer; mapped here, not deployed
```

## What is in it

| Piece | What it does |
|---|---|
| hook `credential-guard` (`hooks/`, `scripts/credential_guard.py`, `scripts/credential-policy.json`) and skill `credential-guard` | Machine-wide, no per-repo setup: a PreToolUse hook on Bash that blocks `git add`, `git stage` and `git commit` when a credential-shaped file would be staged or committed. Test: `bash hooks/test-credential-guard.sh` from the plugin folder. |
| skill `gate-hooks` | Installs the gate kit into a repo and writes its rules with the user. |
| `kit/sdlc_gate.py` | The gate. A PreToolUse and Stop hook: production commands, protected paths, a test lock for fix tasks, a commit backstop, and protection for its own files. It also provides the `lock`, `unlock`, `status` and `check` commands. The lock and the decision log are kept in `.git/sdlc-gate/`, where `git clean` cannot remove them. |
| `scripts/install_gates.py` | Copies the kit into `<repo>/.claude/`, merges the hook entries into `settings.json`, backs up what it replaces. Safe to repeat. |
| skill `review-policy` | Sets up and tunes `REVIEW.md`; runs a policy review of a diff. |
| agent `policy-reviewer` | Fresh context, read-only (`Read, Grep, Glob`). Reports findings against `REVIEW.md` and the intent, spec or plan. Never edits. |
| `templates/REVIEW.md` | The policy template: passes, severity, nit cap, do-not-report, evidence rule, tuning log. |

## Where it came from

Anthropic's *AI-native SDLC playbook* course (14 lessons,
<https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction>). The
workflow skills cover intent, spec, plan, CLAUDE.md, parallel sessions,
self-checks and ship. These kits cover the enforcement side: hooks that block
during the build and hooks that ask for approval (lessons 6, 8, 11) are
`gate-hooks`; the review policy file and its reviewer (lesson 10) are
`review-policy`.

## Install

```
/plugin marketplace update tc-plugins
/plugin install tc-workflow@tc-plugins
```

Then, in a repo, ask for a gate or a review policy and the skills take it from
there. By hand, with the absolute path of the folder sessions start in:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/install_gates.py" --repo /absolute/path/to/repo --dry-run
```

## What has been proven

Run the suite from the repo root:

```bash
python3 -m pytest tests/test_sdlc_plugin.py -q
```

It drives the gate through the exact command string the installer writes into
`settings.json`, in a repo whose path has a space in it.

Live, on Claude Code 2.1.285 (2026-10-03), in a scratch repo with headless
sessions that loaded only the settings of that repo:

| Case | Result |
|---|---|
| Unmatched command | ran |
| Production `deny` | refused; the reason and approval route reached the session word for word |
| Production `ask` with nobody to answer | refused, even with Bash pre-allowed |
| Write to a protected path | refused; no file created |
| `sed -i` on a protected path, through the shell | refused at the call; file unchanged |
| `echo … >>` onto a locked test, through the shell | refused at the call; file unchanged |
| A script file changes a locked test, then the session ends | the Stop hook sent the session back once. In one run the session then restored the file. In another it ended with the lock still violated, which the commit gate keeps refusing. |
| `git commit` with a protected path changed | refused; HEAD unchanged |
| Session started in a subfolder of the repo | gates not loaded; the matching command ran |

A fresh session given only the `gate-hooks` skill and a plain request set up
four rules that gave the intended decision on 17 of 17 probes. Its report also
found the gaps that are now warnings in the installation steps and three of the
limits below.

The same request went to a fresh session with no skill. It hand-built a working
gate of about 240 lines: 15 of the 17 probes as intended, the other two stricter
than asked. It also refused shell writes to protected paths, which this kit did
not do at the time. That check was added here because of it. So the kit does not
give a session an ability it lacks. It gives one tested implementation, the
commit and Stop backstops, the test lock, and limits that are written down. A fresh reviewer given `REVIEW.md` and a diff with five planted defects
reported all five, kept to the nit cap and left the excluded generated file
alone.

The same reviewer instructions, run on this plugin's own code, found six
Important defects. Each is fixed and has a test: a Python that fails before the
gate starts now blocks; the lock moved into the git directory, so `git clean`
cannot drop it; a command continued over lines is matched; a config that leaves
out a section no longer crashes; the docs no longer claim the Stop hook catches
protected paths; and the managed-settings page no longer suggests a deployment
the script cannot do.

The shell-write check was added after that review, and two more reviews of it
alone found seventeen problems between them: ordinary commands wrongly refused
(`chmod +x *.sh`, `cp logo.png .`, a comment with an apostrophe in it), writes
that got through, and three crash paths. Fixing them one at a time was not
converging, so the check was cut down. It now refuses only what it can read with
certainty, and it lets a command through when it cannot parse it or hits a fault
of its own. The rest of the gate still blocks on anything it cannot read.

The cut-down check was then run, in a fixture repo with a lock set, against 76
shell lines that look like writes and are not (arithmetic, `[[ a > b ]]`,
process substitution, quoted `>`, comments, here-documents) and 13 that really
write a protected or locked path. All 76 were allowed and all 13 refused, with
no fault inside the check. A further 142 ordinary and odd commands produced only
two refusals, both correct. A fourth independent review of this version was
started and did not finish, so no fresh reader has been over the final code. It
is the newest and least proven part of the gate.

Not proven:

- **The interactive approval prompt.** Every `ask` in the table ran headless,
  where it refuses. Nobody has seen the prompt in a session in default
  permission mode yet.
- **`ask` in auto mode does not reach the user.** Seen once, on 2.1.286 in the
  desktop app (2026-10-04): the hook returned `ask` twice in a session in auto
  mode, no prompt appeared, and each command ran, 18 and 67 seconds later. The
  transcript carries auto mode's classifier records on both calls and no
  record of a person's answer. So in auto mode an `ask` rule is answered by
  the classifier, and only `deny` stops the call. This contradicts the docs,
  which say a hook's `ask` still prompts in auto mode, and it contradicts the
  no-skill baseline session's report that its own gate's `ask` held in auto
  mode on 2.1.285.
- **`ask` in bypass-permissions mode.** Not documented and not tested here.
  `deny` blocks in every mode.
- **The decision log in a worktree session.** In that same session neither
  `ask` was written to the log, although the gate logs before it answers. The
  same event fed to the same script from a terminal was logged. Cause not
  found; a write the session was not allowed to make under the main repo's
  `.git/` is the guess.
- **Managed settings.** `skills/gate-hooks/managed-settings.md` is checked
  against the docs and deployed nowhere.
- **The review skill on a real change.** The reviewer's read-only tool list is
  asserted by a test; its findings have not been judged on real work.
- **Windows.** The hook command is POSIX shell.

## Limits worth knowing

- A gate reads five tools: Bash, Monitor, Edit, Write and NotebookEdit. An MCP
  tool that reaches the same database or host goes round it. Cover those with
  permission rules in `.claude/settings.json`.
- It is not a sandbox. It refuses a shell write only when it can read it with
  certainty: a redirect, or `rm`, `mv`, `cp`, `tee` or `sed -i` naming the path.
  Everything else in a shell line gets through: git, `find`, a formatter, a
  generator, a script, inline code. A protected file changed that way is caught
  when a commit is attempted through Claude. A locked file is also caught at
  Stop. When the check cannot parse a command, it lets it through.
- The Stop hook pushes back once. If the session still ends with a locked file
  changed, the user gets a warning and the commit gate keeps refusing.
- The hooks load only in a session started in the folder that holds `.claude/`.
  A session started in a subfolder runs with no gates, and so does a nested
  `claude` run that is told to skip project settings.
- The gates bind Claude Code only. Other agents working in the same repo do
  not read these hooks.
- Production rules match text. The real production boundary is credentials the
  session does not hold.
- A Claude Code mod installed on the machine can approve a call the gate
  refused. Only a hook in managed settings is final. See
  `skills/gate-hooks/managed-settings.md`.

## Layout

```
tc-workflow/   (only the gate and review parts)
├── agents/policy-reviewer.md
├── hooks/                      ← credential-guard hook, hooks.json
├── kit/
│   ├── sdlc_gate.py           ← copied to <repo>/.claude/hooks/
│   └── gates.starter.json     ← becomes <repo>/.claude/sdlc/gates.json
├── scripts/
│   ├── install_gates.py
│   └── credential_guard.py, credential_policy.py, credential-policy.json
├── skills/
│   ├── credential-guard/
│   ├── gate-hooks/            ← SKILL.md, managed-settings.md
│   └── review-policy/         ← SKILL.md
└── templates/REVIEW.md
```

The `.claude/sdlc/` config folder, the `sdlc_gate.py` file name and the
`.git/sdlc-gate/` lock folder keep their names, so repos that already installed
the gate keep working.

