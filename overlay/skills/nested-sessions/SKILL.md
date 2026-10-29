---
name: nested-sessions
description: Run two or three independent ready tickets at once, each in its own nested session that this main session starts, steers, follows up and lands, so the user talks to one session instead of going into each one. Only when the user asks for it by name, on their own Mac, with Claude Code running locally. Use when the user says "nested sessions", "set up nested sessions", "do a nested session for this", "subsessions", "spin up a subsession", "background sessions", "run these in parallel sessions". Never on its own initiative: the default build is work-ticket or subagent-driven-development.
---

# Nested sessions

Two or three nested sessions running side by side, each an ordinary session on
its own ticket, worktree and branch. This session is their **main session**: it
starts them, answers or relays their questions, follows up when one goes quiet,
lands their work by the merge rule and archives them when they are done. The
user talks to the main session. They can open a nested session, but they never
have to.

**Names.** The desktop app shows these as *nested sessions* under the session
that started them. Anthropic's docs call them **background sessions**
(<https://code.claude.com/docs/en/agent-view>), and the messaging between them
**cross-session messaging**
(<https://code.claude.com/docs/en/cross-session-messaging>). In the docs,
"nested" means something else: a subagent that starts its own subagents.

**What wakes the main session.** A message from a nested session starts a turn
in the main session when it is idle, so managing them costs a turn per event,
not a session kept alive polling. A nested session that simply *finishes* does
**not** wake the main session on its own. It wakes it only by messaging, or
through an idle notice the main session asked for (§2). Never poll: where the
host has no cross-session messaging, see §6.

## 1. Decide whether it is appropriate

"If appropriate" is a real question. Answer it out loud, yes or no, with the reason.

Say **yes** only when all of these hold:

- There are at least two ready tickets, each a meaningful outcome. Small fixes
  stay in this session, done serially.
- **Disjoint files.** List what each ticket will touch. Any overlap, including
  lockfiles, generated code, migrations, schema or config registries, means
  those two run one after the other.
- **At most one database writer**, and no shared port, dev server, browser
  profile or other single resource.
- No ticket depends on another's output. A dependency is a second wave, started
  when the first merges.
- The machine has room. Check memory and CPU (`memory_pressure`, `uptime` on
  macOS). Three sessions building at once ran a 16 GB Mac out of memory. Each
  nested session also uses quota like an interactive one.
- The host can manage them: Claude Code 2.1.236 or later (`claude --version`)
  for idle notices, and `crossSessionInbound` not set to `refuse`. Nested
  sessions run **on this machine**. A cloud session can't message back to
  another machine, so cloud sessions are §6, never managed nested sessions.

Otherwise say **no** and name the alternative: do them one at a time with
`work-ticket`, or a whole spec with `implement-spec`. A side task
that needs no session of its own (a search, a read-only check) is a subagent,
which reports back on its own.

**Three nested sessions at once is the ceiling.** The main session counts as
one when it is building too; when it only manages, three nested sessions plus it.

## 2. Start each nested session

One nested session per ticket, through the host's session control. On the
command line that is

```bash
claude --bg --model <sonnet|opus> --name <ticket-id> "<brief>"
```

which prints the session's short id. **Always pass `--model`**: a nested
session started without it inherits the main session's model. Pick by the
ticket: `sonnet` for a ticket that is building to a clear spec (most of them),
`opus` for one that needs judgment (a design call the spec left open, a hard
bug, a risky migration). Opus is the ceiling: even when the main session runs
on Fable, no nested session runs above Opus. See the model rule in
`WORKFLOW.md`. Name each one after its ticket so messages
can address it by name. If the host has its own control for starting a nested
session, use that instead. Give it a short self-contained brief that points at
things rather than copying them:

```
Repo: <checkout path>. You are a nested session of <main session name>; the
other nested sessions are working <ticket ids>, leave those alone.
Run whats-next bound to ticket <id>: <title>. Do not pick other work.
Work on branch <name>, in a worktree of your own. Set it up from
docs/agents/worker-env.md if the repo has one.
Report to the main session by message, not to the user: a short message when
you are blocked, when you have a question, and when the ticket is green and
ready to merge (branch, head commit, what the checks proved). The main session
will send you review findings to fix. Do not wait on or message the other
nested sessions. Merge only when the main session says so. Close with
stepping-away.
Handoff: <this session's file>.
```

Name the ticket so two nested sessions never pick the same one; the nested
session's own `whats-next` claims it. A background session moves into a
worktree of its own before it edits files, and a fresh worktree lacks
uncommitted work and everything git ignores (env files, dependencies, local
databases, `_pm/` where it is ignored). Commit what it needs first and say in
the brief what it has to set up. Where `_pm/` is ignored, tell it to write its
session file in the main checkout.

Right after starting each one, ask for an **idle notice**: `SendMessage` to it
with `notify_when_idle`. That costs the nested session nothing and gives the
main session one notice when the nested session next finishes a turn or exits.
It is one notice per request and lapses after 12 hours, so ask again after each
notice while the nested session still has work. The nested session's own
messages are the main signal; the notice catches one that stopped without
reporting.

Report each one as **created and pending** until it has actually started, then
give the user one line per nested session: ticket, branch, where it runs.

## 3. Manage them

Act on events, not on a timer. Each turn a nested session's message or idle
notice wakes you:

- **A question.** Answer it yourself when the repo, the ticket, the spec or an
  earlier decision answers it, and say where the answer came from. Bring the
  user only a real decision (taste, scope, anything hard to undo), one line
  with your recommendation, naming the nested session. Relay their answer back.
- **Blocked.** Unblock it (commit a missing file, settle an interface, reorder
  the waves) or park its ticket with `Waiting on:` and tell the user once.
  A nested session stuck on a **permission prompt** is the user's to answer:
  a message from another session never counts as the user's consent, so don't
  try to approve it by message. Tell the user which session and what it asks.
- **Green.** Before anything merges, run `review` on the nested session's
  branch at the head commit it reported: the code and function reviewers, fresh,
  in their own checkouts. Send their findings to the same nested session to
  fix; it keeps its context, so the fix is not a cold start. After the fix,
  review once more. A second failed review marks the ticket `blocked` with
  `Waiting on:` and its findings. Don't review inside the nested session: the
  point is eyes that didn't build it.
- **Ready to merge** (review passed). Read its report and diff by path. A
  background session that worked in its own worktree may already have pushed
  its branch and opened a draft PR; that is fine, the merge is still yours to
  call. The first ready merges first; later ones rebase onto it, and a
  conflict is that nested session's to resolve (and its new head is reviewed
  again). Merge as `finish` says, steps 4 to 6: only on the user's typed go
  for that branch at that commit. Push, deploy and client messages keep their
  own authorization.
- **Idle notice without a report.** Check its state once with
  `claude agents --json --all`: `state` is `working`, `blocked`, `done`,
  `failed` or `stopped`, and `waitingFor` names what a blocked one waits on.
  Then message it once asking for status. Read its transcript
  (`claude logs <id>`) only if it doesn't answer.

Steer by message, short and pointed: a changed decision, a new constraint, a
file to read. Messages are plain text only, never files or history. Don't
restate the brief. Don't read nested session transcripts on every turn; their
reports are what you keep in context.

The main session owns the shared things: the tracker (ticket status,
`docs/TASKS.md`), the changelog, the client face, the integration branch.
Nested sessions don't edit them; they report, and the main session writes.

## 4. Archive

When a nested session's ticket is merged and its `stepping-away` has run, check
its branch is merged (`git merge-base --is-ancestor`), then stop it and remove
it: `claude stop <id>`, then `claude rm <id>` (or the host's own archive
control). `claude rm` removes the worktree Claude made for it when that is
safe, and refuses when the worktree has uncommitted changes or unpushed
commits; read the refusal, don't force it. The transcript stays available
through `claude --resume`. Archive or stop the nested session whose ticket was
dropped or parked too, once its state is written on the ticket. Never leave
one running with nothing to do.

When the last one is archived, tell the user in one message: what merged (with
commits), what each check proved, what is parked and on what.

## 5. What each nested session does

The normal loop, reporting to the main session:

1. `whats-next` bound to the named ticket.
2. The work, in its worktree, committing at green checkpoints so a crash costs
   reasoning, not work.
3. Rebase on the base branch, run the project's checks on the rebased tree,
   and report to the main session.
4. Fix what the two reviewers find, re-run the checks, report again.
5. Merge when the main session says so.
6. `stepping-away`. The main session archives it.

## 6. Hosts without cross-session messaging

If this host can open sessions but they can't message back (a cloud session, a
click-to-start chip, a plain new window, an older Claude Code), fall back to
unmanaged siblings: each one is told to report to the **user**, own its ticket
through its own merge on the user's word, and close itself. The main session
then lets go: no polling, no transcript reads, no integration. If the user asks
how one is doing, look once and answer. No session-creation control at all:
print the briefs for the user to paste.

## Next to implement-spec

A whole spec already cut into tickets, built hands-off with subagents, is
`implement-spec`. This skill is for two or three tickets the user
wants moving at once, each needing a session of its own that the user can open
and talk to.

## What this skill does not do

- Start on its own. The user asks for nested sessions by name.
- No lane board and no polling loop.
- No unattended merges: the user says go for each branch.
- No more than three at once.
