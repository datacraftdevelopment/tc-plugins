---
name: implement-spec
description: "Build a whole spec's tickets in one go: background implementer subagents take every ready ticket at once, each in its own worktree, a merger folds each into one integration branch, newly ready tickets start, and the finished branch goes through finish (two fresh reviews, then the repo's merge policy). When the spec has a POC, the first slice is built and shown to the person before the rest start. Use when the person picks 'all at once' as they approve the tickets, or says 'implement spec', 'implement the spec', 'build the whole thing' (or types /tc-workflow:implement-spec). Never start it on your own because a spec is ready or tickets are filed: it needs the person's choice."
---

# Implement a spec

Adapted from Matt Pocock's `implement-spec` (mattpocock/skills, MIT; see
`VENDOR.md`). What changed: tickets come from this repo's tracker, builders
use this plugin's `test-driven-development`, a first slice is shown to the
person before the rest is built, the end is `finish` (the two fresh
reviewers, then the repo's merge policy), and nothing reaches the default
branch outside that policy.

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
  chose this, so that is the go to build; it is not a go to merge.
- Read the spec's `POC:` line. With a POC, every implementer is pointed at
  `docs/poc/<topic>/`: the screens it builds, and `data/*.json` for its test
  fixtures.
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

4. **The first slice, alone.** When a ticket is marked `First slice`, it is
   the whole frontier: build it by itself (as below), merge it into the
   integration branch, then **show it to the person running**: how to start
   it from the integration branch, the screens to walk, and screenshots beside
   the POC's where a browser can be driven. Ask: "Is this the thing? The
   other N tickets build on it." and **stop**. What they change is fixed here,
   on this ticket, before anything else starts; a change that contradicts the
   approved POC goes back to `poc` first. Their yes releases the rest, and
   from here you run to the end without asking. No first-slice ticket: skip
   this step.

   Then start an **implementer subagent** (`sonnet`, in the background) for each
   frontier ticket, each in its own worktree on its own branch
   (`git worktree add .worktrees/t-<n> -b t-<n>-<slug> spec/<slug>`). Each
   implementer:
   - confirms its worktree is based on the integration branch, and resets onto
     it if not;
   - loads `tc-workflow:test-driven-development` and builds the ticket
     test-first, committing at green points;
   - runs the repo's check and every Acceptance line it can verify;
   - makes no choice that would show: anything that would make a screen or a
     behaviour differ from the approved POC or the spec, it reports as a
     question instead of deciding, and you take it to the person;
   - merges the integration branch tip into its own branch, re-runs the
     check, and reports done with its branch, head commit and the check
     output. It never pushes, never touches the default branch, never edits
     the tracker.

5. When an implementer reports done, a **merger subagent** (`sonnet`) merges
   its branch into the integration branch, resolves any conflict test-first,
   runs the check on the result, and walks that ticket's own Acceptance lines
   on the merged result. Red, or a failing line, stays until fixed: the merger
   fixes it or reports it, and nothing new merges on top. This is a cheap
   early check, not the review: the two fresh reviewers still see the whole
   branch at the end.

6. If that merge opens new tickets on the frontier, start their implementers.
   Repeat until every ticket is merged into the integration branch. Keep a
   short running note of what merged and any ruling made, for the report at
   the end; don't message the person for progress.

7. Tickets with `You check` lines: ask the person to check them now, on the
   integration branch, and note what they saw.

8. Go to `finish` with the integration branch. Its review is the whole-branch
   review: both fresh reviewers on its head commit, against all the spec's
   Acceptance lines and every ticket's. Findings get one fix pass by a single
   implementer subagent, then one re-review. Then the merge, by the repo's
   merge policy: on its own under `on-pass` when everything passed, otherwise
   one go from the person for the whole spec.

9. On merge, every ticket of the spec moves to `done`. Remove every
   implementer worktree and branch (`git worktree remove`, which refuses on
   uncommitted work: read why). Offer `ship-acceptance`.

## When something goes wrong

- An implementer stuck or failing twice on its ticket: stop it, mark the
  ticket `blocked` with `Waiting on:` and why, and carry on with the rest of
  the frontier. Tell the person once, at the end or when nothing else can move.
- A ticket that turns out wrong (the spec didn't foresee it): stop that
  ticket, ask the person, don't redesign it yourself.
- Never merge to the default branch outside `finish` and the merge policy,
  never push over it, never deploy.
