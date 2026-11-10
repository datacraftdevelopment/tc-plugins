# What this plugin is made of

`tc-workflow` is built, not hand-edited: `build/build.py` in this repo lays
the files this edition owns (`overlay/`: every workflow skill, the agents,
the templates) over a small allowlisted set of guards and reference skills
taken from one upstream plugin at a pinned commit (`BUILD-INFO.json` names
it). Every file below keeps its licence.

The skills in the first and fourth rows were first copied from Agent Runway
at commit ec05598 and have been kept and changed here since 0.3.0; nothing is
read from that repository at build time.

| Part | From | Licence |
|---|---|---|
| `writing-plans`, `subagent-driven-development`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion` | Jesse Vincent's **Superpowers** v7.0.1 (<https://github.com/obra/superpowers>), via Agent Runway | MIT, [`LICENSE.superpowers`](LICENSE.superpowers) |
| `domain-modeling`, `codebase-design`, `research`, `pr` | Matt Pocock's skills (<https://github.com/mattpocock/skills>), via pm-sp | MIT, [`LICENSE.mattpocock`](LICENSE.mattpocock) |
| `implement-spec` | Adapted from Matt Pocock's `implement-spec` (mattpocock/skills 1.3.1, commit 59db609) | MIT, [`LICENSE.mattpocock`](LICENSE.mattpocock) |
| `intake`, `poc` | Written for this edition | © 2026 Joe DaSilva |
| `map`, `grill`, `prototype`, and the owned `spec`, `file-tickets`, `work-ticket`, `review`, `finish`, the two reviewer agents | Agent Runway (<https://github.com/datacraftdevelopment/agent-runway>) | PolyForm Shield 1.0.0 (<https://polyformproject.org/licenses/shield/1.0.0>). Required Notice: Copyright 2026 DataCraft Development |
| Session skills, scaffold, `design-handoff`, `okf`, `ship-acceptance`, `nested-sessions`, the credential guard, `gate-hooks`, `review-policy` and its agent | Joe DaSilva's pm-sp and pm (<https://github.com/datacraftdevelopment/dc-dev-plugins>) | © 2026 Joe DaSilva |

A generic improvement found here goes upstream only as a separate change,
written there, never by copying this repo.

## What the build changes in upstream files

1. Skill references to the upstream plugin's own name become
   `tc-workflow:`.
2. Lines about tools this edition doesn't carry (a second-vendor reviewer, the
   Runway app, private paths) are removed. `build/phrases.json` lists every
   edit word for word.
