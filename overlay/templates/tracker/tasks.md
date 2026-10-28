# Tracker: tasks

Tracker: tasks

Tickets live in `docs/TASKS.md` in this repo. `file-tickets` adds them,
`work-ticket`, `review` and `finish` move them along, `whats-next` and
`stepping-away` read them. Chosen at scaffold; to switch, see "Switching".

## A ticket

```markdown
## T-<n>: <title>
Status: open
Spec: docs/specs/<file>.md
Blocked by: none
You check: none
Sensitive: no
Branch:
Reviews:

<What to build and where, pointing at the spec rather than restating it.>

Acceptance:
- [ ] A1: <observable check>. Verify: <command, or what to look at>.
```

- **Status** is one of `open`, `in progress`, `in review`, `done`, `blocked`.
  `blocked` carries a `Waiting on:` line saying who, what and since when.
- **Blocked by**: `none`, or ticket ids (`T-2, T-3`). A ticket is ready when it
  is `open` and everything it is blocked by is `done`.
- **You check**: the Acceptance lines only the person can confirm (a real
  device, how it looks or feels), with what to look at, or `none`.
- **Sensitive**: `yes` when it touches auth, payments, data or migrations, CI,
  secrets or a public interface. The person reads the diff of a sensitive
  ticket before saying go.
- **Branch** is filled in when work starts. **Reviews** gets one line per
  review: `<date> <short sha> code: pass|fail, function: pass|fail` and a
  pointer to the findings below the ticket.
- Ids are never reused. A dropped ticket keeps its section with
  `Status: done` and `Dropped: <reason>`.

## Writing to it

Only the main checkout edits `docs/TASKS.md`, on the default branch, and
commits it on its own (`tasks: T-4 in review`), never mixed with code. Worktree
sessions and subagents don't edit it; they report, and the main session
writes. Push that commit when the repo has a remote, so the other computer
sees it.

One writer at a time: TASKS.md suits one person's repo. A repo several people
work in should use GitHub Issues.

## Switching

To move to GitHub Issues: file each open ticket as an issue with the same
header lines, note `Moved to: #<n>` under each moved section, change the
`Tracker:` line at the top of this file to `Tracker: github`, and commit. Never run the two side
by side.

## Maps

`docs/maps/` holds only maps (`map` skill): one effort per directory, the map
at `docs/maps/<effort>/map.md`, decisions at
`docs/maps/<effort>/issues/<NN>-<slug>.md` with `Status:` (`open`, `claimed`,
`resolved`), `Blocked by:` and, when a decision needs the person, a
`Waiting on:` line. Map commits touch only `docs/maps/<effort>/`.

Loose ideas never go in the tracker; they go to `docs/inbox.md`.
