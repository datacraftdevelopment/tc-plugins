---
name: file-tickets
description: "Cut a spec into small tickets in this repo's tracker (docs/TASKS.md or GitHub Issues), shown with the spec for one go, with the first ticket the main journey made real, and file them only when the person types go. Use from spec when it has several pieces, or when the person says 'file tickets', 'break this into tickets', 'cut it up', 'make tickets for this'."
---

# File tickets

Turn a spec into a small batch of tickets a fresh builder can pick up one at a
time. **The person's typed go is the approval. Never file without it.**

Read `docs/agents/issue-tracker.md` first: `Tracker: tasks` means
`docs/TASKS.md`, `Tracker: github` means GitHub Issues through `gh`. It also
holds the ticket format. No such file: the repo was never scaffolded; ask the
person which they want and write it from this plugin's
`templates/tracker/tasks.md` or `templates/tracker/github.md`
(`${CLAUDE_PLUGIN_ROOT}/templates/tracker/`).

## 1. Propose the batch

Each ticket small, with an observable result, and not waiting on a decision
only the person can make. Two to six tickets is a good batch; more, and the
spec is probably two specs. Show it as one table:

| key | title | waits on | you check | sensitive |
| --- | --- | --- | --- | --- |
| a | Store each session's frame size | nothing | none | no: new column, no change to old rows |
| b | Camera preview fills the frame on a phone | a | A2: preview on a real phone | no |
| c | Show the frame size in the history list | a | none | no |

- **The first slice.** When the spec has a POC, ticket `a` is the main
  journey made real, as thin as it can be while still running end to end on
  real storage: the screens of the journey, one happy path, no edges. Mark it
  `first slice` in the title column, and when filed, start its description
  with the line `First slice: shown to the person before the rest start.` Everything else waits on it. It is built
  and shown to the person before the rest start, so a wrong turn costs one
  ticket, not the spec.
- **Fixtures.** With a POC, each ticket that touches data says which
  `docs/poc/<topic>/data/*.json` files its tests use. Builders copy them into
  the repo's test fixtures; they never invent a second shape.
- **waits on** names another key in this batch, an existing ticket (`T-12`,
  `#12`), or nothing. Only a real dependency: the other ticket's work must be
  in place, or both change the same files. Fewer waits mean more can be built
  at once.
- **you check** lists the Acceptance lines only the person can confirm: a real
  device or camera, or how it looks or feels. Everything else is checked by
  the function reviewer from the repo alone.
- **sensitive** is `yes` when the ticket touches auth, payments, data or
  migrations, CI, secrets or a public interface. The person reads the diff of
  a sensitive ticket before merging. When unsure, `yes`.

Under the table, each ticket's Acceptance lines: one to three observable
checks, each with how to verify it (a command where there is one). Write lines
a fresh reviewer can verify in a clean checkout with the repo's own commands,
or an experiment it can do and undo (change a value, see a named test fail).
Copy the spec's lines where they fit; never weaken one to make it easier.

Then ask, in your own words, one question that covers both the batch and the
build: "File these N tickets and build them? All at once, or one at a time?"
and **stop**. Do not file in the same turn. Coming straight from `spec`, this
is the same message as the spec, and the one go covers the spec too.

- **All at once** is `implement-spec`: every ready ticket built in the
  background on one integration branch, the first slice shown to the person
  first, one review and one merge for the whole spec. Recommend it when the
  tickets are mostly independent and the spec has a POC.
- **One at a time** is `work-ticket`, ticket by ticket with the person
  alongside. Recommend it for sensitive work, or when the tickets are few and
  each needs their eye.
- Nested sessions only when the person asks for them by name.

## 2. File on go

Only when the person's next message says go (go, yes, file them) for this
batch. If they change something, show the table again and ask again. A go for
an earlier batch is not a go for a changed one.

**Tracker: tasks.** In the main checkout, on the default branch, append one
section per ticket to `docs/TASKS.md` in the format the tracker file gives,
numbering on from the highest id in the file. `Blocked by:` uses the new ids.
Commit it on its own (`tasks: file T-4..T-6 from <spec>`), and push if the
repo has a remote.

**Tracker: github.** One `gh issue create` per ticket, in dependency order so
`Blocked by:` can name real issue numbers, with the body in the tracker file's
format (write each body to a temp file and pass `--body-file`). Create the
three status labels first if they're missing (the tracker file has the
commands).

Then tell the person the ids and which are ready now, and start the build
they chose: `implement-spec` for all at once, `work-ticket` on the first
ready ticket for one at a time. If their go didn't say which, ask that one
question; don't pick for them.

## Never

- File without the person's typed go for this exact batch, or file more than
  they agreed to.
- Mark a ticket not sensitive to make it look easier.
- Put loose ideas in the tracker: those go to `docs/inbox.md`.
