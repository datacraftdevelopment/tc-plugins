---
name: implement-spec
description: "Build a whole spec's tickets in one go: background implementer subagents take every ready ticket at once, each in its own worktree, a merger folds each into one integration branch, newly ready tickets start, and the finished branch goes through finish (two fresh reviews, the person's go to merge). Use ONLY when the person explicitly says 'implement spec' or 'implement the spec' (or types /tc-workflow:implement-spec). Never start it on your own, and never because a spec is ready or tickets are filed; offer it instead."
---

# Implement a spec

Adapted from Matt Pocock's `implement-spec` (mattpocock/skills, MIT; see
`VENDOR.md`). What changed: tickets come from this repo's tracker, builders
use this plugin's `test-driven-development`, the end is `finish` (the two
fresh reviewers, then the person merges), and nothing reaches the default
branch without the person's go.

You have been given a spec (`docs/specs/...`) and its tickets, filed with
`file-tickets`. `docs/agents/issue-tracker.md` says where they live. No
tickets yet: stop and offer `file-tickets` first.

The goal is the whole spec built on one **integration branch**, every ticket
merged into it, then reviewed and merged by the person.

The tickets are not a list of steps. They are a **task graph**: `Blocked by:`
lines link them. At any moment there is a **frontier** of ready tickets
(open, and everything they're blocked by merged into the integration branch).

Keep messages to and from subagents short. Point at things, the spec, the
ticket, notes, earlier commits, instead of copying them.

## Before you start

- Say how many tickets, how many are ready now, and which wait. The person
  asked for it by name, so that is the go to build; it is not a go to merge.
- Check the machine has room: each implementer is a full build. Three at once
  is the ceiling unless the person says otherwise.
- Any ticket with `You check` lines: those lines need the person at the end,
  before the review. Say so now.
- Background subagents can't ask for permission: a command that isn't
  already allowed is simply denied. Check that `git` and the repo's check
  command are in `.claude/settings.json` under `permissions.allow` (for
  example `"Bash(git:*)"`, `"Bash(npm test:*)"`). If they aren't, offer to add
  them; without them, run the implementers in the foreground instead.

## Steps

1. Read the spec and the tickets, and work out the graph and the frontier.

2. (Optional) One **exploration subagent** (`sonnet`) for what several tickets
   need to know: the relevant code, external docs. It saves its notes as
   Markdown in a folder outside the repo (`${TMPDIR:-/tmp}/implement-<spec>/`)
   that every later subagent can read, so implementers build rather than
   explore.

3. Create the integration branch from the up-to-date default branch:
   `spec/<slug>`. Mark the spec's tickets as yours to build: each one moves to
   `in progress` when its implementer starts (tasks: `Status:` lines committed
   on the default branch in the main checkout; github: the label).

4. Start an **implementer subagent** (`sonnet`, in the background) for each
   frontier ticket, each in its own worktree on its own branch
   (`git worktree add .worktrees/t-<n> -b t-<n>-<slug> spec/<slug>`). Each
   implementer:
   - confirms its worktree is based on the integration branch, and resets onto
     it if not;
   - loads `tc-workflow:test-driven-development` and builds the ticket
     test-first, committing at green points;
   - runs the repo's check and every Acceptance line it can verify;
   - merges the integration branch tip into its own branch, re-runs the
     check, and reports done with its branch, head commit and the check
     output. It never pushes, never touches the default branch, never edits
     the tracker.

5. When an implementer reports done, a **merger subagent** (`sonnet`) merges
   its branch into the integration branch, resolves any conflict test-first,
   and runs the check on the result. Red stays red until fixed: the merger
   fixes it or reports it, and nothing new merges on top of red.

6. If that merge opens new tickets on the frontier, start their implementers.
   Repeat until every ticket is merged into the integration branch.

7. Tickets with `You check` lines: ask the person to check them now, on the
   integration branch, and note what they saw.

8. Go to `finish` with the integration branch. Its review is the whole-branch
   review: both fresh reviewers on its head commit, against all the spec's
   Acceptance lines and every ticket's. Findings get one fix pass by a single
   implementer subagent, then one re-review. Then the person's go to merge.

9. On merge, every ticket of the spec moves to `done`. Remove every
   implementer worktree and branch (`git worktree remove`, which refuses on
   uncommitted work: read why). Offer `ship-acceptance`.

## When something goes wrong

- An implementer stuck or failing twice on its ticket: stop it, mark the
  ticket `blocked` with `Waiting on:` and why, and carry on with the rest of
  the frontier. Tell the person once, at the end or when nothing else can move.
- A ticket that turns out wrong (the spec didn't foresee it): stop that
  ticket, ask the person, don't redesign it yourself.
- Never merge to the default branch, push it, or deploy. The person merges.
