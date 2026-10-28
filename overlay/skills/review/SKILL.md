---
name: review
description: "Two fresh reviews of one exact commit: the code reviewer reads the diff, the function reviewer runs the check and walks every Acceptance line. Both must pass. Records the verdicts on the ticket. Use from finish, implement-spec and nested-sessions, or when the person says 'review this branch', 'get it reviewed', 'run the two reviews'."
---

# Review one commit, twice

Two reviewers that never saw the work being built look at the **exact head
commit**, each from its own side. Both must pass. A verdict belongs to that one
commit: any new commit needs a new review.

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

Two subagents, in parallel, both on `opus`:

- `tc-workflow:code-reviewer` with: the code checkout path, the base, the
  ticket text and its Acceptance lines, whether it is sensitive.
- `tc-workflow:function-reviewer` with: the function checkout path, the check
  command, the ticket text and its Acceptance lines, the person-checked lines.

Give them pointers, not a summary of the work: never the builder's reasoning,
the plan's rulings or what you think of the change, and never one reviewer's
verdict to the other. They read the ticket and the code themselves.

## 4. Read the verdicts

Each ends with a JSON block. Check it names the sha you pinned; a verdict for
another commit doesn't count. A reviewer that crashed, returned no JSON or
skipped lines is **not a pass**: dispatch it once more, and if it fails again,
report it as blocked.

- **Both pass:** the commit is reviewed. If either raised `sensitive`, say so:
  the person reads the diff before saying go.
- **Either fails:** the findings (code) and failing lines (function) go back
  to the builder: in `finish`, one fix pass, then one re-review of the new
  head (both reviewers again, fresh). A second failure stops and goes to the
  person with the findings, and the ticket is marked `blocked` with
  `Waiting on: the person, review findings on <short sha>`.

## 5. Record

Write the verdicts where the tracker keeps them
(`docs/agents/issue-tracker.md`):

- **tasks**: on the ticket's `Reviews:` line add
  `<date> <short sha> code: pass|fail, function: pass|fail`, and under the
  ticket a `### Review <short sha>` block with each finding and each line's
  evidence. Commit it on the default branch in the main checkout, on its own.
- **github**: a comment on the pull request starting `Review of <short sha>`,
  with both verdicts, the findings and each line's evidence.

Then remove both review worktrees (`git worktree remove --force <path>`).
Report in a few lines: the sha, both verdicts, what failed and why.

## Never

- Review in the session that built the change, or hand a reviewer the
  builder's story.
- Count a line as passed because the code looks right, or because the
  person "would probably" confirm it.
- Reuse a verdict after a new commit, a rebase or a conflict fix.
- Edit, commit or push from a review checkout.
