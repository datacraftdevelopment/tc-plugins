# Tracker: GitHub Issues

Tracker: github

Tickets are GitHub issues in this repo, read and written with the `gh` CLI
(signed in to an account that can write to the repo). `file-tickets` opens
them, `work-ticket`, `review` and `finish` move them along, `whats-next` and
`stepping-away` read them.

## A ticket

Title: `<title>`. The issue number is the ticket id (`#12`). Body:

```markdown
Spec: docs/specs/<file>.md
Blocked by: none
You check: none
Sensitive: no

<What to build and where, pointing at the spec rather than restating it.>

## Acceptance
- [ ] A1: <observable check>. Verify: <command, or what to look at>.
```

- **Status** is the issue's state plus one label: open with no label is
  `open`; `in progress`, `in review` and `blocked` are labels; closed is
  `done`. A `blocked` issue gets a comment starting `Waiting on:`.
- **Blocked by**: `none`, or issue numbers (`#10, #11`). Ready means open, no
  status label, and everything it is blocked by is closed.
- **You check** and **Sensitive**: as in the tasks tracker. Sensitive covers
  auth, payments, data or migrations, CI, secrets or a public interface.
- The branch is named `t-<n>-<slug>`, and its pull request says `Closes #<n>`.
- Each review is a comment on the pull request starting `Review of <short sha>`
  with both verdicts and their findings.

Create the labels once, if missing:

```bash
gh label create "in progress" --color FBCA04
gh label create "in review" --color 0E8A16
gh label create "blocked" --color B60205
```

## Switching

To move to docs/TASKS.md: copy each open issue into `docs/TASKS.md` with the
same header lines, comment `Moved to docs/TASKS.md as T-<n>` on the issue and
close it, change the `Tracker:` line at the top of this file to `Tracker: tasks`, and commit.
Never run the two side by side.

## Maps

`docs/maps/` holds only maps (`map` skill): one effort per directory, the map
at `docs/maps/<effort>/map.md`, decisions at
`docs/maps/<effort>/issues/<NN>-<slug>.md` with `Status:` (`open`, `claimed`,
`resolved`), `Blocked by:` and, when a decision needs the person, a
`Waiting on:` line. Map commits touch only `docs/maps/<effort>/`.

Loose ideas never go in the tracker; they go to `docs/inbox.md`.
