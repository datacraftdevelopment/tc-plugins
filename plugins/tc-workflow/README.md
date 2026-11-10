# tc-workflow

A way of building software with Claude Code: say what you want, play with a
POC on mock data until it is right, then have it specced, cut into tickets and
built test-first with agents. Two fresh reviewers check the exact commit, the
merge follows a policy you set per project (ask every time, or merge when the
reviews pass), and the result is proved against production. **Read [`WORKFLOW.md`](./WORKFLOW.md) first**: it is the whole
loop on one page.

Claude Code only. Nothing here needs another AI tool or a separate app.

## Install

```
/plugin marketplace add datacraftdevelopment/tc-plugins
/plugin install tc-workflow@tc-plugins
```

Update later with `/plugin marketplace update tc-plugins`, then restart
Claude Code. If you have the older TC `pm` plugin, remove it first
(`/plugin uninstall pm@tc-plugins`): the two share skill names and the
credential guard would run twice.

Needs `git` and `python3` (3.9 or newer). GitHub Issues as the tracker also
needs the `gh` CLI, signed in. Nested sessions need Claude Code 2.1.236 or
later, running on your own computer. `implement-spec` runs builders in the
background, where nothing can ask you for permission: allow `git` and the
repo's check command in the repo's `.claude/settings.json` first (the skill
offers to).

## Start a project

```
/tc-workflow:scaffold MyProject      # a new folder
/tc-workflow:scaffold here           # this repo
```

It asks where tickets should live (`docs/TASKS.md` or GitHub Issues), how
merges should work (ask you every time, or merge once both reviews pass), the
repo's check command, and five short questions for `_pm/skeleton.md`. Then
say what you want built, in a sentence: you get a short brief, and for
anything with screens a POC on mock data to play with before any spec or
ticket. `whats-next` opens later sessions.

## What's in it

| Step | Skills |
|---|---|
| Session | `whats-next`, `stepping-away`, `checkpoint` |
| Shape | `intake` (the front door), `grill`, `poc`, `prototype`, `map`, `design-handoff`, `spec` |
| Tickets | `file-tickets` (into `docs/TASKS.md` or GitHub Issues) |
| Build | `work-ticket`, `writing-plans`, `subagent-driven-development`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion` |
| Build a whole spec | `implement-spec` (when you pick "all at once"), `nested-sessions` (only when asked for) |
| Review and merge | `review` (agents `code-reviewer`, `function-reviewer`), `finish`, by the project's merge policy (`ask` or `on-pass`) |
| Ship | `ship-acceptance` |
| Guards | `credential-guard` (always on), `gate-hooks`, `review-policy` (agent `policy-reviewer`) — see [`GATES.md`](./GATES.md) |
| Reference | `domain-modeling`, `codebase-design`, `okf`, `research`, `pr` |
| Optional, needs Ringer | `cross-review`: another AI vendor's read of a spec or branch, through Ringer, only when asked for by name; does nothing without Ringer |
| Problems with the plugin | `feedback`: drafts a scrubbed issue on this plugin's repo, files it on your go |

Where each part comes from and its licence: [`VENDOR.md`](./VENDOR.md).

Built by **Joe DaSilva**.
