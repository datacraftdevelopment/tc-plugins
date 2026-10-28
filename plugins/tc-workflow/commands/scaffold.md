---
description: Scaffold a project from the tc-workflow starter — a new project folder, or in-place for an existing repo — choose where tickets live (docs/TASKS.md or GitHub Issues), and run the skeleton interview.
argument-hint: <ProjectName> | here
---

# /tc-workflow:scaffold

Stand up a project from the bundled starter. The starter is **deliberately
minimal** — only day-one files; every other folder is created on first write
(the taxonomy in the stamped `CLAUDE.md` is the map). Moves, in order:
**copy → rename → git → orient**. Don't skip the interview.

The argument is: **$ARGUMENTS**

## 1. Resolve the mode and name

Two modes — read the argument (and the user's phrasing) to pick one:

| Mode | Trigger | Target |
|---|---|---|
| **New** (default) | A name: `OrderPortal` | `<ProjectName>/` in the current directory |
| **In-place** | `here`, `.`, "this folder", "this repo" | `_pm/` + `docs/` wiring added to the current directory |

- If `$ARGUMENTS` is empty, ask ONE question: *"What are we standing up? A project name for a new folder, or `here` to set up this folder."*
- Normalise the name to a folder-safe token (strip spaces/punctuation, keep it readable — "Order Portal" → `OrderPortal`).
- New mode creates the target **in the current working directory**. If the target folder already exists, stop and tell the user — don't overwrite.
- In-place mode: if `./_pm/` already exists, stop — this folder is already scaffolded.

## 2. Copy the template

The starter lives inside this plugin.

**New** — copy it wholesale (it's minimal now — this creates no ballast):

```bash
cp -R "${CLAUDE_PLUGIN_ROOT}/template/." "./<TargetFolder>/"
find "./<TargetFolder>" -name .DS_Store -delete
```

**In-place** — copy ONLY `_pm/`; the copy step touches nothing else that
already exists (step 5 makes small, additive edits — that's its contract,
not this step's):

```bash
cp -R "${CLAUDE_PLUGIN_ROOT}/template/_pm" "./_pm"
find "./_pm" -name .DS_Store -delete
```

The session skills (`whats-next`, `stepping-away`, `checkpoint`, …) ship
globally with this plugin — never copy them into the project.

**Never pre-create taxonomy folders** (`_pm/transcripts/`, `resources/`,
`knowledge/`, …). They're documented in the stamped `CLAUDE.md` and get
created the first time something is written into them.

## 3. Rename the placeholder

*(Skip for in-place.)* In the **copied** files:

- `CLAUDE.md`: replace the "This is a STARTER" banner block with a one-line
  project header naming the project and today's date.
- `README.md`: set the title to the project name.

## 4. Git

First check `python3 --version` reports 3.9 or newer. The credential guard
and the session helpers need it; if it's missing or older, say so and stop
before any git or session step.

The workflow's first artifacts (specs in `docs/specs/` from `spec`, plans
in `docs/plans/`) are *committed* files, so the project must be
a repository.

- **New mode:** if the target is not already inside a git worktree,
  `git init` it and make one baseline commit of the scaffold
  (`chore: scaffold from tc-workflow starter`). If it IS inside an existing worktree
  (e.g. a monorepo), say so and skip the init.
- **In-place mode:** don't init anything — but if the folder isn't a git
  repo, tell the user plainly that the specs, the plans and the
  credential-guard hook all assume one, and ask whether to `git init`.

## 5. Choose the tracker, and wire the shared record

- **The tracker: one question.** *"Where should tickets live: in
  `docs/TASKS.md` in this repo, or in GitHub Issues?"* Suggest TASKS.md for a
  repo one person works in, GitHub Issues when several people share it or the
  repo is already on GitHub. Then:
  - **TASKS.md:** copy `${CLAUDE_PLUGIN_ROOT}/templates/tracker/tasks.md` to
    `docs/agents/issue-tracker.md` and `${CLAUDE_PLUGIN_ROOT}/templates/TASKS.md`
    to `docs/TASKS.md`.
  - **GitHub Issues:** check `gh auth status` and that `gh repo view` finds
    this repo; if either fails, say what's missing (sign in, or create and
    push the GitHub repo first) and offer TASKS.md for now. Then copy
    `${CLAUDE_PLUGIN_ROOT}/templates/tracker/github.md` to
    `docs/agents/issue-tracker.md` and create the three status labels it
    lists. No `docs/TASKS.md`.

  In-place mode: an existing `docs/agents/issue-tracker.md` is that repo's
  decision. Don't ask and never overwrite it; if it has no `Tracker:` line,
  tell the user the skills need one and offer to add it.
- **No empty folders.** `docs/specs/`, `docs/plans/`, `docs/maps/`,
  `docs/shipped/` and `docs/adr/` are created the first time something is
  written into them.
- **The inbox.** `docs/inbox.md` ships in the template (loose ideas, one
  line each, no status). In-place mode: copy it if absent.
- **`.gitignore`** — the template's covers new mode. In-place mode: ensure
  `.env`, `account.md`, `_pm/transcripts/`, `.worktrees/` and `.workflow/`
  (plan ledgers and review packages) are ignored (append additively; the
  `credential-guard` hook blocks staging credentials, but the ignore is the
  belt to that brace).
- **Verification block** — the template `CLAUDE.md` already carries
  `## Verifying your work`. In-place mode: if `CLAUDE.md` exists without
  that section, or without `## How we work`, append those sections from
  `${CLAUDE_PLUGIN_ROOT}/template/CLAUDE.md`; if there is no `CLAUDE.md` at
  all, create a minimal one (project one-liner + those sections) and say
  you did. Ask for the repo's check command (tests, build, lint) and write it
  under `## Verifying your work`: the reviewers run it.

**In-place mutation contract:** the additive edits above (`.gitignore`
lines, `CLAUDE.md` section, `docs/` stubs and the tracker files) are the ONLY
changes allowed
outside `_pm/`; never rewrite or reorganize existing content, and name every
touched file in the sign-off.

## 6. Run the skeleton interview

`_pm/skeleton.md` is the default planning artifact (Wei Hao's 5-step) —
every mode gets one. Don't leave it as a placeholder — interview the user,
briefly. Ask these one at a time, conversationally, and keep it short (a
change-request job only needs a paragraph):

1. **Outcome sentence** — when this project is done, what's true that wasn't before?
2. **Critical user journey** — the one path through the deliverable that has to work.
3. **Minimum capabilities** — the few things that path requires. (Only what would *break the journey* if removed.)
4. **Fundamental enablers** — what has to exist underneath (data, access, integrations)?
5. **Non-negotiables** — hard constraints (deadline, budget, tech, compliance).

Write the answers into `_pm/skeleton.md` in that 5-step structure. If the
user says it's a small job, collapse it to a single tight paragraph — the
artifact scales with content.

## 7. Sign off

Confirm what you did in 3–4 lines: what was created (new folder or in-place
`_pm/`), git state (initialized / existing / declined), renames done,
skeleton captured, the tracker chosen, the check command, and — in-place —
every file touched. Then point at the next step: *"Shape the first piece of
work: `grill`, then `spec`, which writes `docs/specs/` with its Acceptance
checks. Then `whats-next` when you start a working session."*

Don't start doing project work — scaffolding ends here.
