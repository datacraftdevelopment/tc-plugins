---
name: work-ticket
description: "Build one ticket in this session with the person: pick a ready ticket, give it its own worktree and branch, plan it when it is more than a step or two, build it test-first, have the person check the lines only they can, then finish it (two fresh reviews, their go to merge). Also builds a small spec with no tickets. Use when the person says 'work the next ticket', 'do T-4', 'pick up #12', 'build it here', or whats-next recommends a ticket."
---

# Work one ticket

One ticket, one worktree, one branch, start to merge, with the person in the
loop. Read `docs/agents/issue-tracker.md` first: it says where tickets live
(`Tracker: tasks` is `docs/TASKS.md`, `Tracker: github` is GitHub Issues) and
their format.

## 1. Pick it

The person named one: take that. Otherwise list the ready ones (open, no
status, everything they're blocked by done) and agree which. Ones that other
tickets wait on come first.

Read the ticket, its Acceptance lines, its `You check` lines and the spec it
points at, before changing anything. If something in it is unclear enough to
change what gets built, ask that one question now.

## 2. Take it

From the main checkout, on the up-to-date default branch:

```bash
git worktree add .worktrees/t-<n> -b t-<n>-<slug>
```

(`.worktrees/` is gitignored by the scaffold; check it is, before the first
one.) A fresh worktree lacks ignored files: set up what the check needs
(dependencies, an env file from `.env.example`) and say what you did.

Mark the ticket `in progress` and note the branch (tasks: `Status:` and
`Branch:` lines, committed on the default branch on their own; github: the
`in progress` label). Work only in the worktree from here on.

## 3. Build it

- **More than a step or two:** a short plan with `writing-plans` in
  `docs/plans/`, pointing at the spec and ticket rather than restating them.
  Run it with `subagent-driven-development` (the default: a fresh `sonnet`
  subagent per task, each reviewed), or `executing-plans` when subagents
  aren't available or the person wants it inline.
- **Every change test-first:** `test-driven-development`. A bug:
  `systematic-debugging`, reproduce before fixing.
- Commit in the worktree as you go, at green points.
- Decisions the plan didn't settle: make them, write them down as rulings,
  and keep going. Stop to ask only for something irreversible, a security
  question, anything outside the worktree, a ticket that turns out wrong, or
  **a choice that would show**: anything that makes a screen or a behaviour
  differ from the approved POC or the spec. That one is the person's, however
  small it looks.
- With a POC (`POC:` line in the spec): build the screens to match
  `docs/poc/<topic>/`, and take test fixtures from its `data/*.json`. The POC
  is the picture, not source to paste.
- A ticket marked `First slice`: when it runs, show it to the person running
  (how to start it, the screens to walk) before going to `finish`. The other
  tickets build on it.

## 4. The lines only the person can check

For each `You check` line, tell the person exactly what to do and what to look
for ("open the app on the phone, add a set: the timer starts at 0:00"), and
wait for their answer. Note what they saw and when: `review` needs it.

Run the check and every line you can verify yourself, with
`verification-before-completion`: the command, its output, then the claim.
Never mark a line the person didn't confirm. A line that fails is fixed and
asked again.

## 5. Finish

Go to `finish`: up to date, checks, pull request, the two fresh reviews, and
the merge by this repo's merge policy (`docs/agents/merge-policy.md`: the
person's go, or on its own under `on-pass` when everything passed). The ticket
is done only when it has merged. Under `ask`, when more ready tickets remain,
carry on with the next one while this one waits, and bring the finished
branches to the person together: one go can merge several.

## No tickets: a small spec built here

A spec that is one piece needs no tickets. Do the same with the spec as the
work: a worktree and branch named for the spec, steps 3 to 5, and the
Acceptance lines of the spec in place of the ticket's.

## Stopping partway

Leave the ticket `in progress` with its branch, commit what's there, and let
`stepping-away` write the resumable line (ticket, branch, last commit, next
step). Work that turns out blocked: `blocked` with `Waiting on:` who, what,
since when.

## Never

- Work on the default branch, or in the main checkout once the worktree exists.
- Mark a ticket done, or merge, outside `finish` and the merge policy.
- Skip the person's lines because the tests pass.
