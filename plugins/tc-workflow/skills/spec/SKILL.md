---
name: spec
description: "Write what this session has worked out into a spec a fresh agent can build from and check against: what it does, what it doesn't, and acceptance checks. Use when the person says 'write the spec', 'spec this', 'write it up', or when a discussion has settled what to build."
---

# Write the spec

The spec is what every builder and reviewer reads instead of this conversation (a later session, a subagent, or the
two fresh reviewers). Write it from what has already been said in this session and what the repo shows. Don't start a fresh interview: if something that
changes what gets built is still open, ask about that one thing (as in `grill`), and leave the rest.

## Where

`docs/specs/YYYY-MM-DD-<topic>.md` in the repo, unless the repo already keeps specs somewhere else. Create the
folder only when the first spec is written.

## What goes in it

```markdown
# <What is being built>

Status: spec, <date>. Sensitive: <no: one-line reason | yes>.

## Why
Two or three sentences: the problem and who has it.

## What it does
The behaviour, from the user's side. Short paragraphs or a list. Name screens, commands or endpoints by what
the person sees.

## Not in scope
What someone might expect that this deliberately leaves out.

## Decisions
Choices made along the way, one line each with its reason. Link a map or prototype if one settled it.

## Testing
Where the tests go in: the one or two places (a command, an API, a screen) the behaviour is checked from. Use the
repo's existing test style. Builders test at these points, not inside the code they write.

## Acceptance
- [ ] A1: <an observable check>. Verify: <a command, a URL, or what to look at>.
- [ ] A2: …
```

## Sensitive

Settle it with the person in one line before you write. `no` needs a reason it can't hurt anything that matters
(copy, a new isolated screen, tests only). Anything touching auth, payments, data, migrations, CI, secrets or a
public interface is `yes`, and so is anything you can't explain away in a line. `file-tickets` starts each ticket
from this; the person reads the diff of sensitive work before saying go, and a reviewer can raise it, never lower it.

## Acceptance lines

These are the part that matters most. The function reviewer walks each one, pass or fail, on the exact commit,
`file-tickets` copies them into the tickets, and `ship-acceptance` checks them again against production.

- Each line is observable: something a fresh agent can run or look at, not "works well".
- Each says how to verify it, with a command where there is one.
- A reviewer verifies them alone, in a fresh copy of the repo, with the repo's own commands: write lines it can run,
  or an experiment it can do and undo (change a value, see a named test fail). Something only a real device or camera,
  or the person's eye on how it looks and feels, can show isn't a line it can pass: mark it `(you check)` and say what
  the person looks at. `file-tickets` puts those on the ticket's `You check` line.
- Three to six for a spec. If you need more, the spec is probably two specs.

## After: how it gets built

Show the spec, fix what the person changes, and commit it. An approved spec is not a go to build: ask, the person may
want to sit on it. Then, by size:

- **One piece:** no tickets. Build it with `work-ticket` (its "No tickets" section): a worktree, a plan if it needs
  one, test-first, then `finish`.
- **Several independent pieces:** offer `file-tickets`. Once they're filed, the person picks how to build them:
  `work-ticket` one at a time, `implement-spec` for the whole spec in one go, or nested sessions when
  they ask for them.
- **A project-sized spec:** before filing, offer a builder's read: dispatch a fresh `opus` subagent with only the
  spec and the repo, asking what a builder would get stuck on, guess at, or build differently from what's meant.
  Fix the spec from what it finds, then file.
