---
name: cross-review
description: "Optional: a reader from another AI vendor, run through Ringer, reads a spec as its builder or reviews a finished branch, next to a fresh Claude reader. Only for people who have Ringer installed. Use ONLY when the person asks for it by name: 'Ringer cross-review', 'cross-review this', 'get another model on this'. Never run it on your own, never as part of review or finish, and never suggest installing Ringer."
---

# Cross-review (optional, needs Ringer)

An extra read from a different AI vendor, at the two points where it pays:
before a big spec becomes tickets, and before a branch merges. It sits on top
of the normal flow; it never replaces `review`, and `finish` never waits for
it unless the person says so.

[Ringer](https://github.com/datacraftdevelopment/ringer) is a separate tool
that routes work to other models. Most people using this plugin don't have
it, and don't need it.

## First: is Ringer here?

Run `zsh -lc 'command -v ringer'` (on a machine without zsh,
`bash -lc 'command -v ringer'`). The login shell matters: Ringer is often only
on the PATH there.

- **Not found:** say "Cross-review needs Ringer, which isn't installed on this
  computer. The two normal reviewers (`review`) still cover this branch."
  Then stop. Don't install anything, don't look for it elsewhere, and don't
  bring it up again this session.
- **Found:** load Ringer's own `ringer` skill if it is installed. It owns the
  mechanics: the task manifest, the check, the engine, watching the run. Every
  call to the other model goes through Ringer, never a direct call to another
  vendor's CLI.

A cloud session counts as not found: give the same message, and only add that
it can run from their own computer if the person has said they have Ringer
there.

## The readers

Both get the same packet and run at the same time; neither sees the other's
answer.

- **The other vendor:** one Ringer task on the `codex` engine. Use the model
  and effort the person's Ringer config sets for reviews, unless they name
  one.
- **A fresh Claude:** an `opus` subagent with none of this session's context.
  It hasn't watched the spec or code get written, which is the point.

The packet is read-only context and the question: no transcript, no unrelated
history. Merge the answers before acting. A point both raise counts once; a
point only one raises is still a point.

## Spec mode

For a big spec, after `spec` writes it and before `file-tickets` files it.

- **Packet:** the spec's path, the repo path, and the instruction to read it
  as the person who will build it and list what they'd still have to ask.
  Also ask which Acceptance lines a reviewer couldn't prove (those become
  `You check` lines).
- **Each answer:** every question with a reason on the same line; any
  decision that is hard to undo flagged `door:`.
- **After:** sort the questions into answered already, minor, and the
  person's. Doors always go to the person. Fix the spec once, one round, then
  offer `file-tickets`.

## Branch mode

On a finished branch, when the person asks, usually right after `review`
passes and before they say go.

- **Packet:** base and head commits, the diff, the spec and ticket the branch
  answers to, `REVIEW.md` if the repo has one, and the check's output at the
  head commit.
- **Each verdict:** findings with severity and file:line, each tied to the
  spec, the ticket or `REVIEW.md`; a finding with no reference is noted, not
  acted on. Both also look for a lowered bar: new suppressions, skipped or
  deleted tests, stubs, loosened checks.
- **After:** fix what it finds test-first, rerun the check, and send the new
  head once more. Any new commit also needs `review` again on that commit, as
  `finish` says. A second failed cross-review stops: tell the person what is
  still open. Never merge past an open finding.

## When a reader can't run

If the Ringer task fails on quota, sign-in or model availability, retry once,
then carry on with the Claude reader alone and label the result
`(Claude only)`. If both fail, or the person says to skip it, label it
`(not run)`. Never present a one-reader result as a full cross-review.
