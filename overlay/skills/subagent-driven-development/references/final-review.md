# Final Review and Finish

Part of tc-workflow:subagent-driven-development. Every task in the plan is
complete.

The final whole-branch review is `tc-workflow:finish`: it brings the branch up
to date, runs the check, and sends the head commit to `tc-workflow:review`,
the two fresh reviewers (code and function). Don't dispatch a separate
whole-branch reviewer here first: that review would be repeated.

Before you hand over to `finish`, point it at the ledger: the deferred-minor
and parked lines, so the person sees them with the verdicts. If the reviews
fail, `finish` runs ONE fix pass with the complete findings list, not one
fixer per finding, and one re-review. There is no second fix wave: residual
findings go to your human partner.

### Finish

Before you delete anything, collect every ledger line containing `Ruling:` —
preflight rulings, parked findings, breaker adjudications, all of them — into
your final message under "Rulings I made", in the order you made them, each
with what it costs if wrong. The list is exhaustive: if the ledger holds a
ruling, the list holds it. That list is the only place the decisions you
took on your human partner's behalf reach them — they read it and rework
whatever you got wrong. A ruling that dies with the workspace was a decision
made in secret.

When `finish` has merged the branch on your human partner's go, delete this
plan's workspace (`rm -rf <workspace>`) — the git history is the record now.
Sibling directories belong to other plans; leave them alone.
