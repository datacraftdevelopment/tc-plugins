---
name: intake
description: "The front door for new work. Size what the person asked for, pick the path (just do it, grill then spec, POC first, or a map), and run the stages in order without being told each one, stopping only at the steer points. Use whenever the person says what they want built or changed without naming a skill: 'I want to build X', 'let's add Y', 'we need a screen for Z', 'new feature', 'can we make it do…', or when whats-next ends in new work that isn't shaped yet."
---

# Intake

The person says what they want once. You decide how much process it needs,
say which path you picked in one line, and run it. They should never have to
ask for the next stage by name, and they should never find out at the end that
something else was built.

## 1. Read, then size it

Read before asking: `_pm/skeleton.md`, the repo, `docs/specs/`, `docs/poc/`,
`docs/agents/merge-policy.md`, recent commits. Then pick one path:

| The work is… | Path |
| --- | --- |
| **Small**: fully specified, a step or two, nothing to decide | Just do it, test-first, then `finish`. No brief, no spec. |
| **One piece, nothing to look at**: a command, a service, a rule, a refactor | `grill` (full) → `spec` → build |
| **Has screens, or data someone has to look at**: a new page, a new app, a report, a changed flow | Brief → `poc` → `spec` and tickets → build |
| **Foggy**: several unknowns that depend on each other, too big for one spec | Suggest `map`. Each chunk it ends with comes back here. |

When it is between two, take the heavier one for anything a person will look
at, and the lighter one for anything they won't. Say the path and why in one
line ("This has two new screens, so POC first.") and carry on. The person can
overrule it in a word.

## 2. The brief (every path except small)

Half a page, written from what they said and what the repo shows, in the chat:

```
What: <one or two sentences>
Who uses it: <role>
Main journey: 1. … 2. … 3. …
Out: <what someone might expect that this leaves out>
Path: <which one, and the stages ahead>
Open: <the one or two things you can't guess, if any>
```

Ask: "Is this the thing?" and **stop**. This is steer point 1, the cheapest
place to catch a wrong idea. Fix what they correct; their go starts the path.

## 3. Run the path

From here each stage hands to the next on its own. The person is asked only at
the steer points:

| Steer point | What the person looks at | What their answer starts |
| --- | --- | --- |
| 1. Brief | The half page above | Questions, the data sample, the POC |
| 2. POC | A working page in the browser, until they type approved | The spec and the ticket table |
| 3. Spec and tickets | One spec, one table, one go, and how to build them | The whole build, through review |
| 4. Merge | Verdicts, screenshots beside the POC, the diff when sensitive | The merge (or nothing to ask, when the merge policy is `on-pass` and everything passed) |

The path without a POC has no steer point 2. The small path has only the last.

**Between steer points, keep going.** Ask only when an answer would change
what gets built in a way the person would notice, or a step can't be undone.
Everything else: decide, write it down (an assumption in `poc.md`, a decision
in the spec, a ruling in the plan's ledger), and show it at the next steer
point.

**At each steer point, show the thing, not a description of it:** the address
of the POC, the spec file and the table, the pull request and the screenshots.
A few lines, then the question, then stop.

## 4. Keep the place

The stages leave their own trail, so a later session picks up where this one
stopped: `docs/poc/<topic>/poc.md` carries a `Status:` line, the spec carries
its own, tickets carry theirs. `whats-next` reads them. If the session ends
between steer points, `stepping-away` writes the resumable line (which stage,
what is next).

## Never

- Skip the brief because the request sounded clear. Clear requests are the
  ones that get built wrong with confidence.
- Run a stage the path doesn't need to look thorough: a small job gets no
  spec, a job with nothing to look at gets no POC.
- Start a `map` unasked; suggest it.
- Pass a steer point without the person's answer.
