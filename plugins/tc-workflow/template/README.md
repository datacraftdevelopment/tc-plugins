# Project

Light by design: only the day-one folders exist; everything else is created
on first use (the taxonomy lives in `CLAUDE.md`).

## Working the project

1. `_pm/skeleton.md` holds the outcome, journey and non-negotiables, written at
   scaffold time; keep it current as scope moves.
2. Open each session with `whats-next`; close it with `stepping-away`.
3. New work: say what you want built. `intake` shows a brief, then for
   anything with screens a POC on mock data in `docs/poc/` to play with and
   approve; then `spec` (with its Acceptance checks) and its tickets in one
   go, built one at a time (`work-ticket`) or all at once (`implement-spec`).
   Every branch closes with `finish`: two fresh reviews, then the merge by
   `docs/agents/merge-policy.md`. `ship-acceptance` proves the
   whole spec against production.
4. Tickets live where `docs/agents/issue-tracker.md` says. Decisions that need
   their own record go to `docs/adr/`. Loose ideas go to `docs/inbox.md`.

Stamped by the tc-workflow plugin's `/tc-workflow:scaffold`. The workflow of
record is that plugin's `WORKFLOW.md`.
