---
name: ship-acceptance
description: Verify a delivered spec against its Acceptance lines and record the delivery evidence in docs/shipped/. Use when a spec's tickets have all merged, when preparing a release, after a person deploys, or when deciding whether a spec is done. Covers deployed systems and delivered documents or tools. Never deploys production.
---

# Ship acceptance

The last handoff: approved spec → its Acceptance lines checked by someone who
did not build it → delivery record. Every ticket can merge green; this decides
whether the spec's outcome was delivered. Merged is not delivered.

## 1. Pin what will be checked

Read the approved spec (`docs/specs/<name>.md`) and the candidate's exact
revision (a commit, or a SHA-256 for a file). Copy the `## Acceptance` lines
word for word with their IDs (A1, A2, …; number them in the record if the spec
did not). If a line needs to change, that goes back to the person who approved
the spec. A line is never weakened to fit what was built.

Create `docs/shipped/` on first write. Use
[record-template.md](./record-template.md) for `docs/shipped/<spec-name>.md`.
A retry or a new candidate adds a dated section. A failed result is never
overwritten with a pass.

## 2. Check the candidate before release

The checker is not the session that built it.

- **Lines a model can check from the repo:** dispatch the
  `tc-workflow:function-reviewer` agent (on `opus`) in a throwaway checkout of
  the candidate (`git worktree add --detach "${TMPDIR:-/tmp}/ship-<short-sha>"
  <sha>`), with the check command and the spec's Acceptance lines. Its
  per-line evidence goes into the record. Remove the checkout after.
- **Lines that need the running thing or the person** (a screen, a real
  device, a saved record, a file that arrives): the person performs the check
  as written, or a session other than the builder performs it and captures
  what it saw. A screenshot shows what was on screen; it does not show the
  data was saved. Read the saved state through another route.

Record for each line: ID, pass / fail / not-run, the exact revision, where it
ran, who checked, when, and the real output or observation. A missing tool or
missing access is **not-run** with the reason, never an assumed pass. An
opinion that the code looks right is not a check.

Any required line failed or not run → **blocked**. All pass →
**ready-for-release**.

## 3. A person releases

A person applies production. This skill never does. Do not send files or
messages to recipients without explicit authorization.

After the person confirms the release and the target is known, confirm the
revision that is live and repeat the same lines against it. A different
revision from the one checked in step 2 needs step 2 again.

For a delivered document or tool, identify the exact file that was handed
over and where it went, and check that file.

## 4. Write the record

Status is one of:

- **blocked**: a required line failed or was not run.
- **ready-for-release**: every line passed before release; not yet released.
- **shipped**: every line passed against what was released.
- **released-with-exceptions**: a person chose to release with a line unmet.
  The record names the line, who decided, when and why, and the follow-up
  work. An exception never becomes an unqualified shipped.

For `shipped`, add a line under the spec's `Status:` line:
`Completion: shipped · <link to the record>`. For
`released-with-exceptions`, `Completion: released-with-exceptions · <link>`;
`whats-next` keeps showing it until the person accepts the open tail.
`blocked` and `ready-for-release` leave the spec as it is.

Done means the record says what was asked for, what was delivered, what was
checked by someone other than the builder, and what remains unproven.
