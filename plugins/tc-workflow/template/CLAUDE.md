# CLAUDE.md

This file orients Claude Code when working in this repository.

> **This is a STARTER, not a live project.** `/tc-workflow:scaffold` stamps it
> and replaces this banner with the project header. The workflow it serves is
> the tc-workflow plugin's `WORKFLOW.md`.

## What this is

The project-management layer around this project, kept light: the scaffold
holds only what every project uses from day one. Everything else is known but
not built (the taxonomy below).

## Day-one layout

```
<project>/
├── CLAUDE.md            ← you are here
├── README.md
├── .gitignore
├── docs/                ← SHARED record: collaborators and clients read it
│   ├── inbox.md         ← loose ideas, one line each, no status
│   ├── TASKS.md         ← the tickets, when the tracker is tasks
│   ├── agents/
│   │   └── issue-tracker.md ← where tickets live (tasks or github) and their format
│   └── quirks.md        ← technical gotchas, fast capture
└── _pm/                 ← PERSONAL log: per person, append-only, never authoritative
    ├── README.md
    ├── skeleton.md      ← the macro why. Always populated.
    └── sessions/        ← one file per session: YYYY-MM-DD-<name>[-N].md
```

**The one rule:** `docs/` is authoritative; `_pm/` records what I did and
what I'm doing, never what is true.

## How we work

The tc-workflow plugin's skills, start to finish. Its `WORKFLOW.md` is the
one-page version.

- **Open with `whats-next`, close with `stepping-away`.** Several sessions a
  day is normal.
- **New work is shaped first:** `grill` talks it through, `prototype` shows it
  when seeing beats reading, and `spec` writes it up. Foggy work with several
  unknowns that depend on each other: suggest `map`, never start it unasked. A
  quick, fully specified task skips shaping.
- **Screens come first.** Work with screens goes data sample, then screens in
  Claude Design (`design-handoff`), approved, then the spec.
- **Specs go in `docs/specs/YYYY-MM-DD-<topic>.md`, plans in
  `docs/plans/YYYY-MM-DD-<feature>.md`.** Both are committed.
- **Every spec has `## Acceptance`:** three to six observable checks as
  `- [ ] A1: …` lines, each saying how to verify it. The function reviewer
  walks them on every branch; `ship-acceptance` runs them again against the
  real candidate and production.
- **An approved spec is not a go to build or to file.** Ask; the user may
  want to sit on it.
- **Tickets** live where `docs/agents/issue-tracker.md` says
  (`docs/TASKS.md` or GitHub Issues). `file-tickets` files them only on the
  user's typed go.
- **Building:** `work-ticket` takes one ticket into its own worktree, plans it
  (`writing-plans`) when it is more than a step or two, and builds it with
  `subagent-driven-development` or `executing-plans`, test-first. A whole spec
  in one go is `implement-spec`, only when the user says "implement spec".
  Nested sessions only when the user asks for them by name. Decisions the
  plan didn't settle are made and written in the ledger as rulings; only
  irreversible, security, outside-the-worktree or hopelessly broken steps stop
  to ask.
- **Every branch ends in `finish`:** the check, then `review` (two fresh
  reviewers on the exact commit: code and function; both must pass), one fix
  pass at most, then **the user merges**, on their typed go. Sensitive work
  (auth, payments, data, migrations, CI, secrets) gets the user's own read of
  the diff too.
- **Bugs:** `systematic-debugging`. Reproduce before fixing.
- **Model economy.** Subagents always name their model: `sonnet` to build,
  `opus` for judgment and every review, whatever the main session runs on.

## The taxonomy: known folders, created on first write

**Never pre-create a folder.** Each exists the moment something is first
written into it (`mkdir -p`, then write): presence means it was needed.

| Folder | Purpose | Sprout when |
|---|---|---|
| `docs/specs/` | Specs from `spec`, with Acceptance | the first spec is written |
| `docs/plans/` | Plans, from writing-plans | the first plan is written |
| `docs/shipped/` | Delivery records from ship-acceptance | the first acceptance run |
| `docs/notes/` | Scratch, meeting notes, ad-hoc analysis | first ad-hoc doc that isn't workflow |
| `knowledge/` | Curated project knowledge, always an OKF bundle (`okf` skill) | facts turn entity-shaped, or a second consumer needs them |
| `resources/` | Material **you bring in** from outside (`design-handoff/`, `research/`, `history/` as needed) | first external file arrives |
| `docs/adr/` | Durable decisions, in domain-modeling's format | the first ADR |
| `docs/maps/<effort>/` | A map, its decisions and research notes (`docs/agents/issue-tracker.md`) | `map` charts its first map |
| `.workflow/` | Gitignored working state: plan ledgers and review packages | the first plan run |
| `.worktrees/` | Gitignored: one worktree per ticket being built | the first ticket worked |
| `docs/agents/client-face.md` | Optional: names an outside tracker the team reports to and its close-out steps; `stepping-away` follows it | when such a tracker is set up |
| `_pm/transcripts/` | Meeting transcripts, **gitignored** | first transcript kept |
| `_pm/artifacts/` | Other raw inputs: customer docs, exports, recordings | first raw input that isn't a transcript |
| `_pm/deliverables/` | What you hand over: reports, dashboards | first deliverable produced |
| `_app/` · `_ws/` · … | Code surfaces, **one underscore container per surface** | the surface becomes real |

Claude-generated docs go in `docs/`; external material goes in `resources/`.
Provenance decides, not file type.

## The skeleton

`_pm/skeleton.md`: outcome sentence, critical user journey, minimum
capabilities, fundamental enablers, non-negotiables. A paragraph for a
change-request job, a longer doc for a six-month project.

## Sessions and the Intent block

One file per session, per person, append-only. `whats-next` writes a two or
three sentence Intent at the open (push, why, done-for-this-session, not in
scope) when the work is clear; a fuzzy start leaves it unset and the first
re-aim sets it; `stepping-away` closes with Shipped / Tried-Learned-Decided /
Intent-vs-outcome and a resumable line per plan in flight. Keep the session's
exact path and ID in the conversation; close by that binding. `checkpoint`
appends a dated re-aim only when the session can't be broken.

## Verifying your work

Before reporting any task done, fixed or passing:

- **Run the check fresh**, after the last edit, and **show its output**:
  tests, build, lint, a real request, a screenshot, whichever would catch the
  failure you'd most plausibly have caused.
- The claim is exactly what the output supports. Red: report it verbatim.
  Partial: say which parts. Nothing runnable: say what *would* verify it.
- Fix the code, not the test. Never skip or delete a failing test, add a
  suppression or loosen a threshold to get green.

The check command for this repo: `<fill in at scaffold: tests, build, lint>`.

(The full rule: the `verification-before-completion` skill.)

## Delivery acceptance

When a spec's tickets have all merged, `ship-acceptance` runs its Acceptance
checks against the actual candidate, records the result in `docs/shipped/`,
and repeats them against production after a person deploys. Merged tickets
are not a delivered spec.
