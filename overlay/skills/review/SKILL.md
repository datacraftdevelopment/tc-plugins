---
name: review
description: "Two fresh reviews of one exact commit: the code reviewer reads the diff, the function reviewer runs the check and walks every Acceptance line. Both must pass. Records the verdicts on the ticket. Use from finish, implement-spec and nested-sessions, or when the person says 'review this branch', 'get it reviewed', 'run the two reviews'."
---

# Review one commit, twice

Two reviewers that never saw the work being built look at the **exact head
commit**, each from its own side. Both must pass. A verdict belongs to that one
commit: any new commit needs a new review.

## 0. Is it ready for a code review?

Two cheaper looks come first, because a code review of a design that is
about to change is wasted, and the next one will be too.

- **A design read, when the change makes separate processes or sessions agree
  about shared state** (who owns a thing, a queue, a lock, a heartbeat, files
  several writers touch). Have the builder write the design on one page: the
  states, who writes what, what happens when a process dies or two act at
  once. Dispatch the code reviewer on that page alone and ask for the cases
  that break it. Build after the design holds. If three reviews of the code
  each find a different routing or timing bug, the design is the finding:
  stop and bring the person a simpler one.
- **The person's own look, when the change has a screen.** Put a build they
  can try in front of them before the code review, and record what they saw
  as `You check` lines. Five minutes of their hands finds what no reviewer
  reads for: that a control is confusing, that a step is missing.

## 1. Pin what is reviewed

From the branch's checkout:

```bash
git rev-parse HEAD
git merge-base origin/<base> HEAD
```

(no remote: `git merge-base <base> HEAD`). Note the head `sha`, the base and
the ticket (or, with no ticket, the spec or plan the branch answers to). Read
the ticket's Acceptance lines, its `You check` lines and `Sensitive`
(`docs/agents/issue-tracker.md` says where tickets live). Find the repo's
check command: the one the plan or the ticket names, or the README's, or ask
the person once and note it in `CLAUDE.md` under `## Verifying your work`.

The POC: the spec's `POC:` line. When it names one, note its folder
(`docs/poc/<topic>/`) and whether any Acceptance line says "matches POC
screen S…". Make a folder for screenshots outside the checkouts:
`.workflow/review/<short-sha>/shots/` in the main checkout (gitignored).

The person-checked lines: any `You check` line the person has confirmed in
this session, with what they saw and when. Ask them for any that are still
open before you dispatch, so the function reviewer can count them. A line they
haven't checked stays open and blocks.

## 2. Give each reviewer a throwaway checkout

Each reviewer gets its own detached worktree at the sha, outside the repo's
working folders, so neither sees uncommitted work or the other's experiments:

```bash
git worktree add --detach "${TMPDIR:-/tmp}/review-<short-sha>-code" <sha>
git worktree add --detach "${TMPDIR:-/tmp}/review-<short-sha>-function" <sha>
```

If the check needs set-up a fresh checkout lacks (dependencies, an env file
from `.env.example`), do that set-up in both folders first and say what you
did. Never copy real credentials into them.

## 3. Dispatch both at once

Two subagents, in parallel, both on `fable`, the one place the model rule
goes above `opus` (see `WORKFLOW.md`). Name the model when you dispatch; the
agents also carry it, so a reviewer that reports another model was started
wrong and is not a pass:

- `tc-workflow:code-reviewer` with: the code checkout path, the base, the
  ticket text and its Acceptance lines, whether it is sensitive.
- `tc-workflow:function-reviewer` with: the function checkout path, the check
  command, the ticket text and its Acceptance lines, the person-checked lines,
  and, with a POC, its folder inside the checkout and the screenshots folder.

**A third reader from another vendor, only where the machine has one.** Run
the check at the top of `tc-workflow:cross-review` ("is it here?"). Found:
start that skill's other-vendor reader at the same time, in branch mode, that
reader only, on the same sha and with the same pointers as the code reviewer.
Not found: carry on with the two and say nothing about it; never install
anything for it.

Give them pointers, not a summary of the work: never the builder's reasoning,
the plan's rulings or what you think of the change, and never one reviewer's
verdict to the other. They read the ticket and the code themselves.

What makes a review find things, in every dispatch:

- **The brief as a file.** With no ticket, write what the change must do as
  numbered lines in one file outside the checkouts and give every reader its
  path, so all of them judge the same thing. Put the limits the builder has
  stated as known and accepted at the end, so they aren't reported again.
- **Reproduce, don't only read.** Ask the function reviewer to replay each
  line that matters itself, in a scratch folder, through the same door a
  person or agent would use, and to record what it ran and what came back.
  Ask the code reviewer to reproduce a suspected defect before calling it
  important.
- **Prove the tests can fail.** Name three to five deliberate breakages of
  the rules that matter most (the check always answers yes, the lock isn't
  exclusive) and have the function reviewer apply each, name the test that
  goes red, and restore. A rule whose breakage leaves every test green is a
  failing line, however many tests pass.
- **Rails on a live machine.** Say what the reviewers must not touch (a
  running app someone is using, the person's real data and settings folders),
  have them record a checksum of those folders before and after, and have
  them confirm no process they started is left running.

## 4. Read the verdicts

Each ends with a JSON block. Check it names the sha you pinned; a verdict for
another commit doesn't count. A reviewer that crashed, returned no JSON or
skipped lines is **not a pass**: dispatch it once more, and if it fails again,
report it as blocked.

- **The other-vendor reader, when it ran:** it returns findings, not a
  verdict. Check each one against the code yourself. A finding you confirm,
  tied to the ticket, the spec or `REVIEW.md`, counts as a code-review fail and
  goes back with the rest; one you can't confirm is noted in the record, not
  acted on. If the reader couldn't run (quota, sign-in, model not available),
  retry once, then go on with the two and write `(other vendor: not run)` in
  the record. It never blocks a merge by being absent.
- **Both pass:** the commit is reviewed. If either raised `sensitive`, say so:
  the person reads the diff before saying go.
- **Either fails:** the findings (code) and failing lines (function) go back
  to the builder: in `finish`, one fix pass, then one re-review of the new
  head (both reviewers again, fresh). A second failure stops and goes to the
  person with the findings, and the ticket is marked `blocked` with
  `Waiting on: the person, review findings on <short sha>`. Don't send a
  third round on your own, however close it looks: the person may want a
  smaller design, not another fix.
- **A confirming read instead of the full re-review** is allowed in one case:
  the function reviewer passed the first time, the code reviewer's failures
  were specific findings and not the design, and the fix pass closed each one
  with a test. Then dispatch the code reviewer alone, fresh, on the new head,
  pointed at the fix diff and the list of findings, asked two things: is each
  important finding closed in the code and not only in a test, and did the
  fixes add anything harmful (a way to lose data, a hang, a crash, a write
  outside its folders). It fails only on those. Anything else it finds is
  recorded as a follow-up. Say in the record that it was a confirming read.

## 5. Record

Write the verdicts where the tracker keeps them
(`docs/agents/issue-tracker.md`):

- **tasks**: on the ticket's `Reviews:` line add
  `<date> <short sha> code: pass|fail, function: pass|fail` (plus
  `other vendor: N confirmed|not run` when that reader was started), and under the
  ticket a `### Review <short sha>` block with each finding and each line's
  evidence. Commit it on the default branch in the main checkout, on its own.
- **github**: a comment on the pull request starting `Review of <short sha>`,
  with both verdicts, the findings and each line's evidence.

Then remove both review worktrees (`git worktree remove --force <path>`).
Report in a few lines: the sha, both verdicts, what failed and why, and the
screenshots folder when the function reviewer filled it. `finish` shows those
to the person.

## Never

- Review in the session that built the change, or hand a reviewer the
  builder's story.
- Count a line as passed because the code looks right, or because the
  person "would probably" confirm it.
- Reuse a verdict after a new commit, a rebase or a conflict fix.
- Review a head the builder reported before it read your last message to it.
- Send a third round after two failures without the person.
- Raise a test's threshold or drop a test to get a pass without saying so in
  the record: the person decides whether a loosened bar is acceptable.
- Edit, commit or push from a review checkout.
