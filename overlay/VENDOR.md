# What this plugin is made of

`tc-workflow` is built, not hand-edited: `build/build.py` in this repo cuts it
from two upstream plugins at pinned commits (`BUILD-INFO.json` names them),
keeps only an allowlisted set of files, rewrites a few phrases, and lays the
files this edition owns on top. Every file below keeps its licence.

| Part | From | Licence |
|---|---|---|
| `writing-plans`, `subagent-driven-development`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion` | Jesse Vincent's **Superpowers** v7.0.1 (<https://github.com/obra/superpowers>), via Agent Runway | MIT, [`LICENSE.superpowers`](LICENSE.superpowers) |
| `domain-modeling`, `codebase-design`, `research`, `pr` | Matt Pocock's skills (<https://github.com/mattpocock/skills>), via pm-sp | MIT, [`LICENSE.mattpocock`](LICENSE.mattpocock) |
| `implement-spec` | Adapted from Matt Pocock's `implement-spec` (mattpocock/skills 1.3.1, commit 59db609) | MIT, [`LICENSE.mattpocock`](LICENSE.mattpocock) |
| `map`, `grill`, `prototype`, and the owned `spec`, `file-tickets`, `work-ticket`, `review`, `finish`, the two reviewer agents | Agent Runway (<https://github.com/datacraftdevelopment/agent-runway>) | PolyForm Shield 1.0.0 (<https://polyformproject.org/licenses/shield/1.0.0>). Required Notice: Copyright 2026 DataCraft Development |
| Session skills, scaffold, `design-handoff`, `okf`, `ship-acceptance`, `nested-sessions`, the credential guard, `gate-hooks`, `review-policy` and its agent | Joe DaSilva's pm-sp and pm (<https://github.com/datacraftdevelopment/dc-dev-plugins>) | © 2026 Joe DaSilva, for use at TC |

The two upstream repositories are public; nothing from this edition goes back
to them. A generic improvement found here goes upstream only as a separate,
cleaned patch, never by copying this repo.

## What the build changes in upstream files

1. Skill references `superpowers:`, `agent-runway:` and `pm-sp:` become
   `tc-workflow:`.
2. The plan workspace `.runway/sdd/` becomes `.workflow/sdd/`.
3. Where a skill closed work through the Runway app, it now closes through
   this edition's `finish` (two fresh reviews, then the person merges).
4. Lines about tools this edition doesn't carry (a second-vendor reviewer, the
   Runway app, private paths) are removed. `build/phrases.json` lists every
   edit word for word.
