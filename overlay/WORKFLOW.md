# The workflow, on one page

How work moves from an idea to production with this plugin. Every step is a
skill; you can name it, or let the session pick it up from what you say.

```
whats-next ──► shape ──► spec ──► tickets ──► build ──► review ──► you merge ──► ship-acceptance ──► stepping-away
               map                file-        work-ticket        code +        finish             against the
               grill              tickets      implement-spec     function                         real thing
               prototype                       nested sessions    reviewers
```

## 1. Open and close every session

- `whats-next` reads where the work stands (tickets, plans, specs, recent
  sessions) and proposes what to pick up, then writes this session's Intent:
  two or three sentences on what this session pushes and what done looks like.
- `stepping-away` closes it: what shipped against the Intent, a line per plan
  or ticket still open, loose ideas to `docs/inbox.md`.
- `checkpoint` re-aims mid-session when the direction changes.

`docs/` is the shared truth. `_pm/` is your personal log and never wins an
argument with `docs/`.

## 2. Shape before you build

- `grill`: the session interviews you one question at a time until every open
  branch is settled. Asks, never builds.
- `prototype`: a throwaway build to settle one question by seeing it.
- `map`: for work too foggy for one session, a map of the decisions it needs,
  settled one at a time across sessions.
- `design-handoff`: for screens, a brief for Claude Design before the spec.
- `spec`: writes it up in `docs/specs/`, with **Acceptance** lines: three to
  six observable checks, each saying how to verify it. Everything after this
  is measured against those lines.

A quick, fully specified task skips shaping: it is just done, test-first.

## 3. Tickets

`file-tickets` cuts a spec into small tickets in the tracker this repo chose
at scaffold (`docs/agents/issue-tracker.md`): `docs/TASKS.md` in the repo, or
GitHub Issues. Each ticket has its Acceptance lines, what it waits on, and the
lines only you can check (how it looks or feels, a real device). It files
only after you type go.

## 4. Build

Three ways, from the most hands-on to the most hands-off:

- **One ticket at a time:** `work-ticket`. A worktree and branch for the
  ticket, a plan if it is more than a step or two (`writing-plans`), built by
  subagents (`subagent-driven-development`) or inline (`executing-plans`),
  test-first (`test-driven-development`), bugs through
  `systematic-debugging`, and no "done" without output
  (`verification-before-completion`).
- **A whole spec in one go:** `/tc-workflow:implement-spec`. Background
  subagents take every ready ticket at once, each in its own worktree; a
  merger folds each into one integration branch; the next ready tickets
  start. Only when you type it.
- **Nested sessions:** say "set up nested sessions" and the main session
  starts two or three background Claude Code sessions, one per ticket,
  steers them and lands their work. Only when you ask for it by name, on
  your own Mac.

## 5. Review, then you merge

`finish` closes every branch the same way: the checks, then `review`, which
sends the exact commit to two fresh reviewers that never saw it being built:

- the **code reviewer** reads the diff for bugs, risk and anything that
  lowers the bar (skipped tests, loosened checks);
- the **function reviewer** runs the checks and walks every Acceptance line
  at that commit, with the evidence for each.

Both must pass. One fix pass and one re-review, then it comes to you. A
verdict is for one commit: new code needs a new review. Lines only you can
check are yours to confirm. **Nothing merges without your typed go**, and
anything touching security, payments, data migrations, CI or secrets gets your
own read of the diff too.

## 6. Ship

Merged is not delivered. `ship-acceptance` walks the spec's Acceptance lines
against the real candidate, then against production after a person deploys,
and records the result in `docs/shipped/`. The plugin never deploys.

## Guards that run on their own

- The **credential guard** blocks staging or committing files that look like
  credentials, in every repo.
- `gate-hooks` installs repo rules a session can't talk its way past
  (production commands, protected paths, a test lock while fixing a bug).
- `review-policy` writes `REVIEW.md`, which both reviewers read.

## Model rule

Subagents always name their model: `sonnet` to build, `opus` for judgment and
every review, whatever the main session runs on.
