# tc-plugins

A complete way of building software with **Claude Code**, packaged as one
plugin: `tc-workflow`.

You shape an idea until it is clear, write it up as a spec with checks anyone
can run, cut it into small tickets, and let Claude build each one test-first.
Every finished branch is checked by two fresh reviewers that never saw it
being built. **Nothing merges until you say so**, and nothing counts as
delivered until the spec's checks pass against the real thing.

It needs nothing but Claude Code, git and Python 3. No other AI tool, no
separate app, no server.

**Contents**

1. [Install](#1-install)
2. [Your first project, start to finish](#2-your-first-project-start-to-finish)
3. [The workflow, step by step](#3-the-workflow-step-by-step)
4. [Where tickets live: TASKS.md or GitHub Issues](#4-where-tickets-live-tasksmd-or-github-issues)
5. [Three ways to build](#5-three-ways-to-build)
6. [Review and merge](#6-review-and-merge)
7. [Shipping: merged is not delivered](#7-shipping-merged-is-not-delivered)
8. [Guards that run on their own](#8-guards-that-run-on-their-own)
9. [What a project looks like](#9-what-a-project-looks-like)
10. [Every skill, and what to say to use it](#10-every-skill-and-what-to-say-to-use-it)
11. [Rules the plugin always follows](#11-rules-the-plugin-always-follows)
12. [Troubleshooting](#12-troubleshooting)
13. [Feedback](#13-feedback)
14. [For maintainers: how the plugin is built](#14-for-maintainers-how-the-plugin-is-built)
15. [Credits and licences](#15-credits-and-licences)

---

## 1. Install

**You need:**

| What | Why | Check |
|---|---|---|
| Claude Code | runs everything | `claude --version` |
| git | every project is a git repo; tickets are built in git worktrees | `git --version` |
| Python 3.9 or newer | the credential guard and the session log | `python3 --version` |
| GitHub CLI, signed in (optional) | only if your tickets live in GitHub Issues, or to file feedback | `gh auth status` |
| Claude Code 2.1.236+ on your own computer (optional) | only for nested sessions | `claude --version` |

**Install the plugin** (once per computer), inside Claude Code:

```
/plugin marketplace add datacraftdevelopment/tc-plugins
/plugin install tc-workflow@tc-plugins
```

Then **restart Claude Code**. Skills from a newly installed plugin load in new
sessions only.

**Update** when a new version is out:

```
/plugin marketplace update tc-plugins
```

and restart Claude Code. `/plugin` shows the installed version.

**Coming from the older edition?** If you had the earlier `pm` plugin from a
local tc-plugins folder, remove it first, or the two will fight over skill
names and the credential guard will run twice:

```
/plugin uninstall pm@tc-plugins
/plugin marketplace remove tc-plugins
```

then add this marketplace as above.

**Don't install alongside it:** Superpowers, Matt Pocock's skills, or other
workflow plugins. This plugin already carries the parts of them it uses, and
two sets of the same skills compete.

---

## 2. Your first project, start to finish

A walk through one small piece of work, so you see every step once. What you
type is in quotes; you can use your own words.

**1. Set up the repo.** In the repo's folder, start Claude Code and run:

```
/tc-workflow:scaffold here
```

(or `/tc-workflow:scaffold MyProject` to create a new folder). It asks:

- **where tickets should live**: `docs/TASKS.md` in the repo, or GitHub
  Issues (see [section 4](#4-where-tickets-live-tasksmd-or-github-issues));
- **the repo's check command**: whatever runs your tests, build and lint
  (`npm test`, `python3 -m unittest`, `./gradlew check`). The reviewers run it;
- **five short questions** for `_pm/skeleton.md`: what's true when this is
  done, the one path that has to work, the minimum it needs, what has to exist
  underneath, and the hard limits. A small job gets one paragraph.

It commits the result. Nothing in your existing code is touched.

**2. Open a session.** "What's next?" runs `whats-next`: it reads the
tickets, specs, plans and your last sessions, proposes what to pick up, and
writes this session's *Intent* (two or three sentences on what this session
is for).

**3. Shape the work.** "I want users to be able to export their orders as
CSV. Grill me." The `grill` skill asks one question at a time until nothing
important is left open. Then "write the spec": `spec` writes
`docs/specs/2026-10-28-csv-export.md` with what it does, what it doesn't, and
three to six **Acceptance** lines, each with a way to verify it:

```markdown
## Acceptance
- [ ] A1: The Orders page has an Export button that downloads orders.csv. Verify: tests/test_export.py::test_download.
- [ ] A2: The file has one row per order and the columns id, date, total. Verify: same test, header and row count.
- [ ] A3: An account with no orders gets a file with only the header. Verify: tests/test_export.py::test_empty.
```

**4. Cut it into tickets.** "File tickets." `file-tickets` proposes a table:
each ticket, what it waits on, any lines only you can check, whether it's
sensitive. **It files nothing until you type go.**

**5. Build one.** "Work the next ticket." `work-ticket` gives the ticket its
own worktree and branch (`.worktrees/t-1`, branch `t-1-export-button`), marks
it in progress, writes a short plan if it needs one, and builds it
test-first: a failing test, then the code that makes it pass, then the whole
check.

**6. Finish it.** At the end, `finish` brings the branch up to date, runs the
check, opens a pull request (when the repo has a remote), and sends the exact
commit to **two fresh reviewers**: one reads the code, one runs every
Acceptance line and shows the evidence. Then it stops and asks you:

> Both reviews pass on 1c9affc. A1: test_download ok. A2: header and 3 rows.
> A3: test_empty ok. Merge it?

You say "go". It merges, marks the ticket done, removes the worktree, and
names the tickets that are now ready.

**7. Close the session.** "I'm stepping away." `stepping-away` writes what
shipped against the Intent, a line for anything still open, and loose ideas
into `docs/inbox.md`.

**8. When the spec's last ticket merges:** `ship-acceptance` runs the spec's
Acceptance lines against the real build, and again against production after
someone deploys, and records the result in `docs/shipped/`.

That's the whole loop. Everything below is detail.

---

## 3. The workflow, step by step

```
 whats-next ─► shape ─► spec ─► file-tickets ─► build ─► finish ─► you merge ─► ship-acceptance ─► stepping-away
               │                                 │        │
               ├ grill                           ├ work-ticket         review: code reviewer
               ├ prototype                       ├ implement-spec              + function reviewer
               ├ map                             └ nested sessions
               └ design-handoff
```

### Sessions

Several sessions a day is normal. Each one opens with `whats-next` and closes
with `stepping-away`.

- **`whats-next`** reads where the work stands: tickets in progress, in
  review, ready, blocked; plans and how far they got; specs waiting to be
  filed; your last one to three sessions. It recommends one thing, and lists
  what's waiting on you (a branch to merge, a line to check, a spec to
  approve). If you already named the work, it just writes the Intent and starts.
- **`stepping-away`** compares what shipped to the Intent, says whether the
  session drifted, leaves a resumable line for every plan and ticket still
  open, and offers the next session.
- **`checkpoint`** re-aims the session in the middle when the direction
  changed but you don't want to break the session.

Session notes are files in `_pm/sessions/`, one per session per person.
They're your log, not the truth: **`docs/` is the shared record**, and when
they disagree, `docs/` wins.

### Shaping

Don't start building something that isn't clear yet. Pick what fits:

- **`grill`** — an interview, one question at a time, until every open
  branch of the plan is settled. It asks, it never builds. Say "grill me" or
  "poke holes in this".
- **`prototype`** — a quick throwaway build to settle one question by seeing
  it: a screen, a flow, a state model. "Prototype this", "mock it up".
- **`map`** — for work too big or too foggy for one session. It charts the
  decisions the work needs in `docs/maps/<effort>/` and settles them one at a
  time across sessions. Its end is a list of chunks, each of which gets its
  own spec. It's suggested, never started unless you ask.
- **`design-handoff`** — for work with screens: a brief you paste into
  Claude Design, with a small sample of real data. You approve the screens
  before anything is built.

A quick, fully specified task skips all of this. It's just done, test-first.

### The spec

**`spec`** writes what was settled into `docs/specs/YYYY-MM-DD-<topic>.md`:
why, what it does, what's not in scope, decisions, where the tests go, whether
it's **sensitive** (auth, payments, data, migrations, CI, secrets, a public
interface), and the **Acceptance** lines.

Acceptance lines are the most important part. Each one is something a fresh
agent can run or look at, with how to verify it. "Works well" is not a line;
"`GET /export` returns 200 with a `text/csv` body" is. A line only a person can
check (on a real phone, how it looks or feels) is marked `(you check)`.

An approved spec is **not** a go to build: the session asks. For a spec
that's project-sized, `spec` offers a builder's read first: a fresh agent reads
only the spec and says where a builder would get stuck or guess.

---

## 4. Where tickets live: TASKS.md or GitHub Issues

Chosen once, at scaffold, and written to `docs/agents/issue-tracker.md`. Every
skill reads that file to know where tickets are.

| | `docs/TASKS.md` | GitHub Issues |
|---|---|---|
| Best for | one person's repo, or no GitHub | a repo several people share, already on GitHub |
| Needs | nothing | `gh` signed in with write access |
| Ticket id | `T-1`, `T-2`… | the issue number, `#12` |
| Status | a `Status:` line | open/closed plus labels `in progress`, `in review`, `blocked` |
| Review verdicts | a `### Review <sha>` block under the ticket | a comment on the pull request |

A ticket in `docs/TASKS.md` looks like this:

```markdown
## T-1: Export button downloads orders.csv
Status: open
Spec: docs/specs/2026-10-28-csv-export.md
Blocked by: none
You check: none
Sensitive: no
Branch:
Reviews:

Add an Export button to the Orders page that streams the current account's orders as CSV.

Acceptance:
- [ ] A1: The Orders page has an Export button that downloads orders.csv. Verify: tests/test_export.py::test_download.
```

**Status** moves `open` → `in progress` → `in review` → `done`, or `blocked`
with a `Waiting on:` line. A ticket is **ready** when it's open and everything
it's blocked by is done.

Only the main checkout edits `docs/TASKS.md`, on the default branch, in commits
of their own (`tasks: T-1 in review`), never mixed with code. Builders in
worktrees report; the main session writes.

**Switching later** is a small migration, described in
`docs/agents/issue-tracker.md`: move the open tickets across, mark the old ones
as moved, change the `Tracker:` line. Never run both at once.

Loose ideas never go in the tracker. They go in `docs/inbox.md`, one line each.

---

## 5. Three ways to build

| | `work-ticket` | `implement-spec` | nested sessions |
|---|---|---|---|
| What | one ticket, with you | every ticket of a spec, hands-off | two or three tickets at once, each its own session |
| Starts | when you or `whats-next` pick a ticket | **only when you say "implement spec"** | **only when you ask for it by name** |
| Where it runs | this session, subagents for the tasks | background subagents, one worktree each | background Claude Code sessions on your computer |
| You see | every step | the result, and anything that got stuck | one main session that relays questions |
| Ends in | `finish` | `finish` on the integration branch | `finish` per branch |

### One ticket at a time: `work-ticket`

The default. "Work the next ticket", "do T-4", "pick up #12".

1. Picks a ready ticket and reads it and its spec.
2. Makes a worktree and branch: `git worktree add .worktrees/t-4 -b t-4-<slug>`.
   Your main checkout stays on the default branch.
3. More than a step or two: a plan in `docs/plans/` (`writing-plans`), run by
   `subagent-driven-development` (a fresh subagent per task, each task
   reviewed) or `executing-plans` (inline, when you want to watch).
4. Every change test-first (`test-driven-development`). Bugs go through
   `systematic-debugging`: reproduce first, then fix.
5. The lines only you can check: it tells you exactly what to do and what to
   look for, and waits for your answer.
6. Goes to `finish`.

### A whole spec in one go: implement spec

After the tickets are filed, say **"implement spec"** (or "implement the spec
for CSV export", or type `/tc-workflow:implement-spec docs/specs/<file>.md`).
It starts only when you name it like that; it never starts on its own. The
session:

- reads the tickets as a graph (what waits on what) and finds the ones ready
  now;
- starts a background builder for each ready ticket, each in its own worktree,
  each building test-first;
- has a merger fold each finished ticket into one integration branch
  (`spec/<slug>`), and starts the tickets that just became ready;
- when all are in, asks you for any lines only you can check, then runs
  `finish` on the integration branch: one review of the whole thing.

Before the first run, **allow `git` and your check command** in the repo's
`.claude/settings.json`; background builders can't stop to ask permission, so
anything not allowed is simply refused. The skill offers to add them:

```json
{ "permissions": { "allow": ["Bash(git:*)", "Bash(npm test:*)"] } }
```

At most three builders at once unless you say otherwise. A ticket that fails
twice is marked blocked and the rest carry on.

### Nested sessions

Say "set up nested sessions for T-3 and T-4". The main session starts a
background Claude Code session per ticket (`claude --bg --model sonnet --name <ticket>`, or `opus` when the ticket needs judgment; never above Opus),
watches for their messages, answers their questions from the spec when it can,
brings you the real decisions, runs the two reviews on each finished branch,
and lands them one at a time on your go. You only talk to the main session,
though you can open any of the others.

Needs Claude Code 2.1.236+ running on your own computer, tickets that touch
different files, and room on the machine (each session is a full build). Three
at once is the ceiling. In a cloud session it falls back to sessions that
report to you directly.

---

## 6. Review and merge

Every branch ends in **`finish`**:

1. **Up to date and green.** The base branch merged in, the check run fresh,
   output shown.
2. **Pull request.** Pushed and opened as a draft when the repo has a remote;
   the body points at the spec and the ticket.
3. **`review`, on the exact head commit.** Two reviewers, each in its own
   throwaway checkout of that commit, each with none of the builder's
   reasoning, running at the same time:
   - the **code reviewer** reads the diff for bugs, edge cases, risk, missing
     tests, and anything that **lowers the bar** (a skipped or weakened test, a
     stub, a loosened check, a swallowed error). Any of those fails it;
   - the **function reviewer** runs the check and walks **every Acceptance
     line**, doing what its Verify says and recording the evidence. A line it
     can't verify is a fail, never a guess. Your `You check` lines count only
     once you've confirmed them.

   Both must pass. If either fails: **one** fix pass (every finding fixed
   test-first), then **one** re-review of the new commit. A second failure
   stops and comes to you, and the ticket is marked blocked.
4. **To you.** The verdicts, one line of evidence per Acceptance line, any
   decisions the plan made on your behalf, and, for sensitive work, "please read
   the diff before you say go." Then: "Merge it?"
5. **Merge on your typed go**, and only at the commit that was reviewed. A new
   commit means a new review.
6. **Close.** Ticket done, worktree removed, newly ready tickets named.

The reviewers also read `REVIEW.md` if the repo has one (`review-policy`
writes it), so your team's review rules apply to both.

---

## 7. Shipping: merged is not delivered

When a spec's tickets have all merged, **`ship-acceptance`**:

1. copies the spec's Acceptance lines word for word, and pins the exact
   revision;
2. checks each one against the real candidate, with a reviewer that didn't
   build it, and you for the lines only a person can check;
3. after **a person** deploys (the plugin never deploys), checks the same lines
   against what's live;
4. records it in `docs/shipped/<spec>.md`: `blocked`, `ready-for-release`,
   `shipped`, or `released-with-exceptions` (a line you chose to ship without,
   with who decided and why).

A line is never weakened to fit what was built. A missing tool is "not run",
never an assumed pass.

---

## 8. Guards that run on their own

- **Credential guard.** Always on, in every repo, no setup. It blocks
  `git add`, `git stage` and `git commit` when a credential-shaped file
  (`.env`, keys, `credentials.*`, `secrets.*`) would be staged. The scaffold's
  `.gitignore` covers the same files. If it blocks something legitimate, the
  `credential-guard` skill explains why and what to do.
- **`gate-hooks`.** Rules a session can't talk its way past, installed per
  repo: production commands that need a person, paths an agent must not edit
  (generated code, migrations, infrastructure), and a **test lock** that keeps
  the failing test untouched while a bug is fixed. Say "add a gate" or "protect
  this path". Details: [`GATES.md`](plugins/tc-workflow/GATES.md).
- **`review-policy`.** Writes and tunes `REVIEW.md`: what matters in a review,
  severity, what not to report. Read by both reviewers and the
  `policy-reviewer` agent.

---

## 9. What a project looks like

The scaffold creates only what every project uses on day one. Everything else
appears the first time something is written into it. **Never create empty
folders.**

```
<project>/
├── CLAUDE.md              how Claude works in this repo, and the check command
├── README.md
├── .gitignore             credentials, .worktrees/, .workflow/, transcripts
├── docs/                  THE SHARED RECORD
│   ├── TASKS.md           tickets (when the tracker is tasks)
│   ├── agents/
│   │   └── issue-tracker.md   where tickets live, and their format
│   ├── inbox.md           loose ideas, one line each
│   ├── quirks.md          technical gotchas
│   ├── specs/             (first spec)        what to build, with Acceptance
│   ├── plans/             (first plan)        how, task by task
│   ├── maps/              (first map)         decisions for foggy work
│   ├── shipped/           (first ship check)  delivery records
│   └── adr/               (first decision)    durable decisions
├── _pm/                   YOUR PERSONAL LOG, never the truth
│   ├── skeleton.md        the project's why, from the scaffold interview
│   └── sessions/          one file per session
├── .worktrees/            (gitignored) one worktree per ticket being built
└── .workflow/             (gitignored) plan ledgers and review packages
```

---

## 10. Every skill, and what to say to use it

You can name a skill, or just say what you want; the phrases below are the
kind that pick it up.

| Skill | What it does | Say |
|---|---|---|
| `/tc-workflow:scaffold` | Sets up a repo: tracker, check command, skeleton | "/tc-workflow:scaffold here" |
| `whats-next` | Opens a session: where things stand, what to pick up, the Intent | "what's next?", "where did we leave off?" |
| `stepping-away` | Closes a session: shipped vs Intent, open threads, inbox | "I'm stepping away", "let's wrap up" |
| `checkpoint` | Re-aims mid-session | "checkpoint", "re-aim" |
| `grill` | One question at a time until the plan is settled | "grill me", "poke holes in it" |
| `prototype` | Throwaway build to settle one question | "prototype this", "show me" |
| `map` | Decisions map for big, foggy work | "map this", "work the map" |
| `design-handoff` | Brief for Claude Design, data sample first | "design handoff" |
| `spec` | Writes the spec with Acceptance lines | "write the spec", "spec this" |
| `file-tickets` | Cuts a spec into tickets, files on your go | "file tickets", "break this up" |
| `work-ticket` | Builds one ticket in its own worktree | "work the next ticket", "do T-4" |
| `implement-spec` | Builds every ticket of a spec with background builders | "implement spec" (only when you say it) |
| `nested-sessions` | Two or three tickets in parallel sessions | "set up nested sessions" |
| `writing-plans` | A task-by-task plan in `docs/plans/` | "write a plan" |
| `subagent-driven-development` | Runs a plan, a fresh subagent per task, each reviewed | (used by work-ticket) |
| `executing-plans` | Runs a plan inline | "do it inline" |
| `test-driven-development` | Red, green, refactor, for every change | (always on while building) |
| `systematic-debugging` | Reproduce, find the root cause, then fix | "this is broken", a failing test |
| `verification-before-completion` | No "done" without fresh output | (always on) |
| `review` | Two fresh reviewers on one commit | "review this branch" |
| `finish` | Up to date, PR, review, your go, merge, close | "finish this", "get it merged" |
| `ship-acceptance` | Acceptance against the candidate and production | "ship acceptance", "is this delivered?" |
| `credential-guard` | Explains the guard when it blocks | (when a commit is blocked) |
| `gate-hooks` | Repo gates that can't be talked past | "add a gate", "lock the tests" |
| `review-policy` | Writes `REVIEW.md` | "set up a review policy" |
| `domain-modeling` | Glossary and decision records | "add to the glossary", "write an ADR" |
| `codebase-design` | Designing deep modules and seams | "how should this module look?" |
| `okf` | Conventions for a `knowledge/` folder | "knowledge bundle" |
| `research` | Background research into a Markdown file | "research this" |
| `pr` | Writes a pull request body | "write the PR" |
| `cross-review` | Optional, only if you have Ringer installed: another AI vendor reads a spec or branch, next to a fresh Claude. Does nothing without Ringer | "Ringer cross-review" |
| `feedback` | Reports a problem with this plugin | "send feedback", "/tc-workflow:feedback" |

Agents (started by the skills, not by you): `code-reviewer`,
`function-reviewer`, `policy-reviewer`.

**Model rule.** Every subagent and nested session names its model and never
inherits yours. The lowest model that fits the work: `sonnet` builds,
explores, researches and merges; `opus` judges (design, hard bugs) and
reviews. **Opus is the ceiling**: even when your session runs on Fable,
nothing it starts runs above Opus. Never Haiku.

---

## 11. Rules the plugin always follows

- **Your typed go** is needed to file tickets, to merge, and to file feedback.
  A passing review is not a go.
- **A review is for one commit.** New commits, a rebase or a conflict fix
  mean a new review.
- **Never lower the bar** to get green: no skipped or deleted tests, no
  loosened checks, no weakened Acceptance lines.
- **No "done" without output**: the command, what it printed, then the claim.
- **Never deploys** and never sends anything outside the repo without your say.
- **Work happens in worktrees**, never on the default branch.
- **Decisions a plan didn't settle** are made, written down as rulings, and
  shown to you at the end. Only irreversible, security or outside-the-repo
  questions stop the work to ask.

---

## 12. Troubleshooting

**The skills don't show up.** Restart Claude Code after installing or
updating. `/plugin` should list `tc-workflow@tc-plugins` as enabled.

**"credential-guard: BLOCKED".** A file that looks like a credential would
have been committed, or the git command was written in a way the guard can't
check (variables in paths, chained commands). Run the git command on its own
with a plain path. Ask "why did the credential guard block that?" for details.

**implement-spec builders fail with "permission denied".** Background
builders can't ask for permission. Allow `git` and your check command in
`.claude/settings.json` (see [section 5](#5-three-ways-to-build)), or use
`work-ticket`.

**A worktree is missing files.** Worktrees have only committed files. Your
`.env`, installed dependencies and local databases aren't there: the skills
set them up from `.env.example` and the install command, and say what they did.
Commit anything else the build needs.

**`git worktree remove` refuses.** The worktree has uncommitted work or
unpushed commits. The skills never force it; look at what's there first.

**Nested sessions don't report back.** Check `claude --version` (2.1.236+)
and that you're on your own computer, not a cloud session. `claude agents`
lists background sessions and their state.

**GitHub Issues tracker can't create labels or issues.** `gh auth status`
must show an account with write access to the repo.

**The reviewers fail a line only I can check.** Confirm it in the session
first ("I checked A2 on my phone: it fills the frame"), then run the review
again.

---

## 13. Feedback

Something broken, confusing or missing in the plugin? In any Claude Code
session:

```
/tc-workflow:feedback the review skill didn't wait for me to confirm A2
```

It drafts an issue for this repo with the plugin and Claude Code versions,
**removes anything from your project** (names, paths, code, company details),
shows you the whole draft, and files it only when you say go. Without `gh`, it
opens a prefilled issue page for you to submit.

Or open one directly:
<https://github.com/datacraftdevelopment/tc-plugins/issues/new/choose>.
**This repo is public**: leave out secrets, company or client names, internal
hosts and anyone's code.

---

## 14. For maintainers: how the plugin is built

`plugins/tc-workflow/` is **generated. Never edit it by hand.** It is cut
from two public upstream plugins at pinned commits, plus the files this
edition owns.

```
.claude-plugin/marketplace.json   the marketplace: one plugin, ./plugins/tc-workflow
build/sources.json   the two upstreams and the exact commits used
build/files.json     the allowlist: the only upstream files that ship
build/phrases.json   word-for-word edits to upstream files, then token swaps
build/banned.json    the clean check: words that must never ship
build/build.py       runs all of it; any miss fails the build
overlay/             files this edition owns outright, laid on top
plugins/tc-workflow/ the output, with BUILD-INFO.json (inputs and a digest)
tests/               reproducible build, clean check works, guard suite passes
.github/             issue forms for bugs and ideas
```

**Build steps**, each fatal on failure:

1. Export each upstream at its pinned commit with `git archive`: tracked files
   only, links refused.
2. Copy only what `build/files.json` allows.
3. Apply `build/phrases.json`: per-file edits (each must match exactly), then
   token swaps across all files (each must match somewhere).
4. Lay `overlay/` on top.
5. Clean check: no output line may match `build/banned.json`, except the
   credits files it allows.
6. Validate JSON and every skill's front matter, check every
   `tc-workflow:<name>` reference resolves, write `BUILD-INFO.json`.

**Rebuild** with public checkouts of
[dc-dev-plugins](https://github.com/datacraftdevelopment/dc-dev-plugins) and
[agent-runway](https://github.com/datacraftdevelopment/agent-runway) next to
this repo (or pass `--pm-sp-src` and `--agent-runway-src`):

```bash
python3 build/build.py                      # writes plugins/tc-workflow/
python3 build/build.py --check              # fails if plugins/ isn't a fresh build
python3 -m unittest discover tests
```

**Change something:** edit `overlay/` (or the maps in `build/`), bump
`version` in `overlay/.claude-plugin/plugin.json`, rebuild, run the tests,
read the diff of `plugins/`, commit and push. Users get it with
`/plugin marketplace update tc-plugins`.

**Take a newer upstream:** set the new commit in `build/sources.json` and
rebuild. A phrase that no longer matches, a moved file or a banned word stops
the build and names the file and line. Fix the map, or copy the file into
`overlay/` and own it.

**Rules for this repo:** it's public, so no company or client names,
internal hosts, credentials or anything under NDA, in the plugin, the build
files or the issues. The plugin is a way of working, not project knowledge. A
generic improvement found here goes upstream as its own change, written there.

---

## 15. Credits and licences

Built by **Joe DaSilva**. The plugin is assembled from:

- six skills from Jesse Vincent's **Superpowers** (MIT):
  `writing-plans`, `subagent-driven-development`, `executing-plans`,
  `test-driven-development`, `systematic-debugging`,
  `verification-before-completion`;
- skills from **Matt Pocock** (MIT): `domain-modeling`, `codebase-design`,
  `research`, `pr`, and `implement-spec`, adapted;
- **Agent Runway** (PolyForm Shield 1.0.0; Required Notice: Copyright 2026
  DataCraft Development): `map`, `grill`, `prototype`, and the base of
  `spec`, `file-tickets`, `work-ticket`, `review`, `finish` and the two
  reviewer agents;
- Joe DaSilva's own session skills, scaffold, guards and kits.

Each part keeps its licence. The full list, with what the build changes in
upstream files: [`VENDOR.md`](plugins/tc-workflow/VENDOR.md).
