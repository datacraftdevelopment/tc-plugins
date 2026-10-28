# Project

Light by design: only the day-one folders exist; everything else is created
on first use (the taxonomy lives in `CLAUDE.md`).

## Working the project

1. `_pm/skeleton.md` holds the outcome, journey and non-negotiables, written at
   scaffold time; keep it current as scope moves.
2. Open each session with `whats-next`; close it with `stepping-away`.
3. New work: shape it (`grill`, `prototype`, then `spec`, which writes
   `docs/specs/` with its Acceptance checks), cut it into tickets with
   `file-tickets`, build each with `work-ticket`, and close each branch with
   `finish`: two fresh reviews, then you merge. `ship-acceptance` proves the
   whole spec against production.
4. Tickets live where `docs/agents/issue-tracker.md` says. Decisions that need
   their own record go to `docs/adr/`. Loose ideas go to `docs/inbox.md`.

Stamped by the tc-workflow plugin's `/tc-workflow:scaffold`. The workflow of
record is that plugin's `WORKFLOW.md`.
