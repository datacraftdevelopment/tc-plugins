# The workflow, on one page

How work moves from an idea to production with this plugin. You say what you
want built once; `intake` picks the path and runs the stages in order. You
steer at four points and are otherwise left alone.

```
"I want X" ─► brief ─► questions ─► design concepts ─► POC on mock data ─► spec + tickets ─► build ─► review ─► merge ─► ship-acceptance
              ▲ 1      (5 to 8)     ▲ 2a pick a        ▲ 2b you play,      ▲ 3 one go,       first              ▲ 4 by the
              is this               direction          change, approve     and how to        slice              merge policy
              the thing?            (new products)                         build it          shown
```

| Steer point | You look at | Your answer starts |
| --- | --- | --- |
| 1. Brief | Half a page: what, who, the main journey, what is out | The questions, the data sample, the POC |
| 2. POC | Two or three design concepts of the key screen, to pick a direction (skipped when the product already has a look). Then a working page in that direction, until you type approved | The spec and the ticket table |
| 3. Spec and tickets | One spec, one table, and all at once or one at a time | The whole build, through review |
| 4. Merge | Verdicts, screenshots beside the POC, the diff when sensitive | The merge. Under `on-pass` this point is skipped when everything passed. |

Between those points the session asks only when an answer would change what
you'd see, or a step can't be undone. Small, fully specified jobs skip all of
it and are just done, test-first. Work with nothing to look at (a command, a
service, a refactor) skips the POC: full `grill`, then `spec`.

## 1. Open and close every session

- `whats-next` reads where the work stands (tickets, plans, specs, recent
  sessions) and proposes what to pick up, then writes this session's Intent:
  two or three sentences on what this session pushes and what done looks like.
- `stepping-away` closes it: what shipped against the Intent, a line per plan
  or ticket still open, loose ideas to `docs/inbox.md`.
- `checkpoint` re-aims mid-session when the direction changes.

`docs/` is the shared truth. `_pm/` is your personal log and never wins an
argument with `docs/`.

## 2. Shape before you build: see it first

- `intake`: the front door. Sizes the request, writes the brief, runs what
  follows.
- `grill`: one question at a time, each with a recommended answer. **To a
  POC** it asks five to eight questions and assumes the rest; **after the
  POC** it covers what no screen shows (edges, errors, permissions, rules);
  **full** is for work with nothing to look at. Asks, never builds.
- `poc`: design first, then function, kept apart. With no existing look, you
  get two or three concepts of the one key screen that really differ, on the
  same mock data, and pick a direction (or mix them). Then the main journey,
  clickable, on JSON mock data shaped like the real data, in
  `docs/poc/<topic>/`, built in that direction. You play with it, your remarks are sorted
  (change now, decision, question, not this job), it changes, and that loops
  until you type approved. It is kept: the spec links its screens, its JSON
  becomes the test fixtures, and reviewers compare built screens against it.
- `prototype`: a throwaway build to settle one narrow question.
- `map`: for work too foggy for one spec, a map of the decisions it needs,
  settled one at a time across sessions. Each chunk it ends with goes through
  intake.
- `/design` (built into Claude Code) makes those concepts: a canvas of
  editable artboards you pick from and tweak. The pick is saved into the
  repo before the POC is built on it. Without `/design`, the concepts are
  plain HTML pages side by side.
- `design-handoff`: writes the brief for `/design` when the data model is
  big, and again after approval if you want the look polished.
- `spec`: writes it up in `docs/specs/`, pointing at the POC, with
  **Acceptance** lines: three to six observable checks, each saying how to
  verify it. Everything after this is measured against those lines.

## 3. Tickets

`file-tickets` cuts a spec into small tickets in the tracker this repo chose
at scaffold (`docs/agents/issue-tracker.md`): `docs/TASKS.md` in the repo, or
GitHub Issues. Each ticket has its Acceptance lines, what it waits on, and the
lines only you can check (a real device, your own judgement). With a POC, the
first ticket is the **first slice**: the main journey made real, as thin as it
can be, shown to you running before the rest start. The table comes with the
spec, and one typed go covers both and how they are built.

## 4. Build

Three ways:

- **One ticket at a time:** `work-ticket`. A worktree and branch for the
  ticket, a plan if it is more than a step or two (`writing-plans`), built by
  subagents (`subagent-driven-development`) or inline (`executing-plans`),
  test-first (`test-driven-development`), bugs through
  `systematic-debugging`, and no "done" without output
  (`verification-before-completion`).
- **A whole spec in one go:** pick "all at once" when you approve the
  tickets (`implement-spec`). The first slice is built and shown to you; on
  your yes, background subagents take every ready ticket at once, each in its
  own worktree; a merger folds each into one integration branch and checks it;
  the next ready tickets start. One review and one merge for the whole spec.
- **Nested sessions:** say "set up nested sessions" and the main session
  starts two or three background Claude Code sessions, one per ticket,
  steers them and lands their work. Only when you ask for it by name, on
  your own Mac.

A builder may settle technical questions alone and write them down. A choice
that would show, anything that makes a screen or a behaviour differ from the
approved POC or the spec, is yours: it stops and asks.

## 5. Review, then the merge

`finish` closes every branch the same way: the checks, then `review`, which
sends the exact commit to two fresh reviewers that never saw it being built:

- the **code reviewer** reads the diff for bugs, risk and anything that
  lowers the bar (skipped tests, loosened checks);
- the **function reviewer** runs the checks and walks every Acceptance line
  at that commit, with the evidence for each. For a line that says a screen
  matches the POC, it screenshots both and compares them.

Both must pass. One fix pass and one re-review. A verdict is for one commit:
new code needs a new review. Lines only you can check are yours to confirm.

**Who merges is this project's merge policy**
(`docs/agents/merge-policy.md`), which you chose at scaffold and can change
with a sentence:

- `ask`: nothing merges without your typed go. Several finished branches are
  brought to you together, and one go can merge them all. For anything
  hosted, client-facing or carrying real data.
- `on-pass`: a branch merges on its own when both reviewers passed that exact
  commit, the check is green, no line is waiting on you, and nothing is
  sensitive. You get a line saying what merged. For a local prototype or a
  build nobody depends on yet.

Under either, anything touching security, payments, data migrations, CI or
secrets waits for your own read of the diff and your go. When a project first
goes live, `ship-acceptance` asks whether to switch to `ask`.

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

Every subagent and every nested session names its model; none inherits the
main session's. Pick the lowest model that fits the work:

- `sonnet` for building to a clear spec or plan, mechanical edits,
  exploration, research, merges and small fix passes;
- `opus` for judgment: design choices, hard debugging, reading a spec as its
  builder, and every review.

**Opus is the ceiling.** When the main session runs on Fable, everything it
starts runs on Opus at most, and on Sonnet when the work allows. Never Haiku.

## When the plugin itself gets in the way

`feedback` drafts an issue for the plugin's maintainer, scrubbed of anything
from your project, and files it on the public repo only after you say go.
