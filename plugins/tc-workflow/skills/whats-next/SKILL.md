---
name: whats-next
description: Session open. Read where the work stands (tickets in this repo's tracker, specs, plans and their ledgers, recent sessions), propose one or two things to pick up, and write this session's Intent. Use when the user says "what's next?", "what should I work on?", "where did we leave off?", "catch me up", or starts a session cold without a named task.
---

# What's next

The session open. Read first, then propose. Don't ask "what do you want to
work on?": that's what the user is asking you.

**If the user already named the work, there's no pick to make.** Read just
enough to write the Intent for it, write it, and start.

## 1. Read

The shared record first, the personal log second (`WORKFLOW.md`: `docs/` is
truth, `_pm/` is log).

First bring the record up to date: if the branch has an upstream and the
working tree is clean, `git pull --ff-only`, so a map, spec or plan moved
forward on another computer shows here. If the pull can't fast-forward, say so
and read what's local.

- **Plans in flight.** `docs/plans/*.md`, newest first. For each, find how far
  it got: its ledger at `.workflow/sdd/<plan-name>/progress.md` when this
  checkout has one (it's gitignored, so another machine or worktree won't), and
  `git log` for the commits its tasks name. A plan with tasks left is a stream
  of work; the first unfinished task is its pick-up.
- **Tickets.** The tracker `docs/agents/issue-tracker.md` names
  (`Tracker: tasks` is `docs/TASKS.md`; `Tracker: github` is
  `gh issue list --state open --json number,title,labels,body`). Sort them:
  `in progress` (with their branch and worktree: these are resumes),
  `in review` (waiting on a fix pass or the person's go to merge), ready (open,
  everything they're blocked by done), waiting (blocked by open tickets), and
  `blocked` (with their `Waiting on:` line).
- **Specs not yet filed.** `docs/specs/*.md` with no tickets or plan from
  them: approved specs waiting for a go to file, or drafts waiting for
  approval.
- **Shipped records.** `docs/shipped/` tells you which designs were delivered
  (`ship-acceptance`); a `released-with-exceptions` record stays visible until
  the user accepts its open tail.
- **Waiting on the user.** Open questions in a spec, rulings in a ledger
  marked as needing the user, a branch reviewed and waiting for their go to
  merge, `You check` lines nobody has checked yet, a `blocked` ticket's
  `Waiting on:`.
- **The inbox,** `docs/inbox.md` if the repo keeps one: loose ideas, one line
  each. A line is a candidate for shaping, not a task. Never a gate on
  starting work.
- `docs/adr/` newest entries and `GLOSSARY.md` if present.
- `_pm/skeleton.md`, the project's macro why.
- The last one to three files in `_pm/sessions/`, most recent first, especially
  their open threads and Intent vs. outcome.
- A map in `docs/maps/`, if the repo has one (`tc-workflow:map`): its open
  decisions are decision work, not build work. Decisions carrying a
  `Waiting on:` line go under *Waiting on you*. A cleared map's chunks are
  spec candidates, in the order it set.
- Worktrees: `git worktree list`. A ticket worktree with uncommitted work, or
  one whose ticket is done, is a watch-out.

## 2. Propose

Keep work the session can take and decisions only the user can make apart.

```
Where we are: <one sentence: which designs and plans exist, how far each got>.
Ready to pick up: <a ticket in progress to resume, a ready ticket, the first unfinished task of a plan, an approved spec to file, or "nothing in flight">.
Waiting on you: <a branch to merge, lines to check, a spec to approve, a go to file, open questions, or "nothing">.
Recommended: <one pick-up> because <reason from what you read>.
Also worth: <maybe one more>.
Watch-outs: <a plan with no commits in a while, a ledger and git that disagree, an unseated review>.
```

New work with nothing shaped yet goes to `tc-workflow:grill` (and
`tc-workflow:prototype` when seeing beats talking, `design-handoff` for
screens), ending in `tc-workflow:spec`. Work that is genuinely foggy, with
several unknowns that depend on each other, gets `tc-workflow:map`: suggest
it, don't start it; its destination is a set of chunks, a spec each.

## 3. Write the Intent, when there is one

Two or three sentences of plain prose: what this session pushes on, why it
matters, what done-for-this-session looks like, what's out of scope. Scope it
to one session. Once the pick is settled (a named task counts), open the
session record:

```bash
ROOT="$(git rev-parse --show-toplevel)"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/session.py" --root "$ROOT" open --name <handle> --intent '<session intent>'
```

When the session starts fuzzy (thinking out loud, exploring, not sure yet
what to pick), open it without `--intent` and don't make one up to fill the
slot. The file says the Intent isn't set. Once the work firms up, set it
with a re-aim (the `checkpoint` command), which becomes the session's aim.
Some sessions never firm up, and that's fine.

Keep the absolute `ROOT` with the returned `path` and `id`: the plan
may move this session into a worktree, and close and re-aim must still find
the same file. Keep all three in this conversation and in any handoff
summary; they bind this conversation to this session. Never pick a session file
by its ordinal. On resume, reread that file's Intent and latest re-aim.

## 4. Work

Shaped work is done here, with the user in the loop. A ticket goes to
`work-ticket`; a small spec with no tickets too (its "No tickets" section). A
spec with several pieces goes to `file-tickets` on the user's go, then
`work-ticket` one at a time, or `implement-spec` when the user
says "implement spec", or nested sessions when the user asks for them by name. Every branch
ends in `finish`: two fresh reviews, then the user's go to merge. A quick,
fully specified task is just done, test-first.

## No history yet

A brand-new project: offer to draft the skeleton if it is still a placeholder,
or to shape the first piece of work. The Intent is then "draft the
skeleton" or "shape the first piece".
