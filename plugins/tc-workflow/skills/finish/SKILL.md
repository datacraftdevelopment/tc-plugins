---
name: finish
description: "Close a finished branch: bring it up to date, run the checks, push it and open the pull request, run the two fresh reviews, one fix pass if they fail, then merge only on the person's typed go and close the ticket. Use when a ticket's or plan's work is built and green, when the person says 'finish this', 'wrap up the branch', 'get it merged', or when work-ticket, subagent-driven-development or executing-plans reach their end."
---

# Finish a branch

Every branch ends here, whether one ticket, a whole plan or an integration
branch from `implement-spec`. **The person merges.** Nothing here merges on
its own, and a passing review is not a go.

Read `docs/agents/issue-tracker.md` first: it says whether tickets live in
`docs/TASKS.md` (`Tracker: tasks`) or GitHub Issues (`Tracker: github`).

## 1. Up to date and green

In the branch's worktree:

1. Commit or stash nothing silently: `git status` must be clean. Uncommitted
   work is either committed (it belongs) or the person is told.
2. Bring in the base branch (`git fetch`, then `git merge origin/<base>` or
   rebase, following the repo's habit; with no remote, the local base). A
   conflict is this branch's to resolve, test-first like any change.
3. Run the repo's check fresh and show the output
   (`verification-before-completion`). Red stops here: fix it first.

## 2. Push and open the pull request

When the repo has a remote: push the branch and open a pull request (draft
until the reviews pass) against the base. Its body points at the spec and
says `Closes #<n>` in GitHub mode, or names `T-<n>` in tasks mode. Use the
`pr` skill for the body. No remote: skip this; the merge in step 5 is local.

Move the ticket to `in review` (tasks: the `Status:` line, committed on the
default branch in the main checkout; github: the `in review` label).

## 3. Review

Run `review` on the head commit. Both reviewers must pass.

- **Both pass:** go to step 4.
- **Either fails:** ONE fix pass. Give every finding and failing line to one
  builder (a `sonnet` subagent with the findings and the worktree path, or
  yourself when working inline), each fix test-first: a test that reproduces
  the finding, red, then green, then the whole check. Commit, push, and run
  `review` once more on the new head. A second failure stops: the ticket goes
  `blocked` with `Waiting on: the person, review findings on <short sha>`,
  and the person gets the findings and your recommendation.

When the branch came from `subagent-driven-development`, this review **is**
the final whole-branch review: don't run another on top.

## 4. Bring it to the person

Mark the pull request ready. Then tell the person, in a few lines:

- the branch, the head sha, and the pull request link;
- both verdicts, and the evidence for each Acceptance line (one line each);
- the `You check` lines and what they confirmed, or what still needs them;
- any rulings the plan made on their behalf, and deferred minor findings;
- if the ticket is `Sensitive: yes`, or a reviewer raised it: "please read
  the diff before you say go," with the files that matter.

Then ask: "Merge it?" and **stop**. The go must be the person's own typed
word for this branch, at this sha.

## 5. Merge on go

Only after the go, and only if the head is still the reviewed sha (a new
commit means step 3 again):

- **github, or any remote:** `gh pr merge <n> --merge --match-head-commit
  <sha>` (or the repo's merge style), or the person presses merge themselves.
- **No remote:** in the main checkout, on the base branch,
  `git merge --no-ff <branch>`.

Never force-push the base, never merge with a failing check, never merge a
different commit from the one reviewed.

## 6. Close the ticket and clean up

- Ticket to `done` (tasks: `Status: done` and the merge commit; github: the
  pull request closes it, or close it with a comment naming the merge commit).
- Tickets that were blocked by this one may now be ready: name them.
- Remove the worktree (`git worktree remove <path>`; it refuses when there is
  uncommitted work: read why, don't force it) and delete the merged branch.
- When this was the last ticket of a spec, say so and offer
  `ship-acceptance`: merged is not delivered.

## Never

- Merge, or mark a ticket done, without the person's typed go for this branch.
- Count a review of an earlier commit.
- Lower the bar to get green: skip or delete a test, loosen a check, or
  weaken an Acceptance line. A line that can't be met goes back to the person.
- Deploy. Production is a person's step, after which `ship-acceptance` checks it.
