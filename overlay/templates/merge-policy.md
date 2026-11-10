# Merge policy

Merge: ask

How a reviewed branch reaches the default branch in this repo. `finish` reads
the `Merge:` line above every time; nothing else decides it.

- **`ask`**: the person types go for every merge. For anything hosted, shared
  with a client or other people, or carrying real data.
- **`on-pass`**: a branch merges without asking when **all** of these hold,
  and is reported in one line afterwards:
  - both fresh reviewers passed the exact head commit;
  - the repo's check is green on it;
  - no `You check` line is still open;
  - the ticket is not `Sensitive: yes`, and no reviewer raised it.

  If any one fails, that branch falls back to `ask`. For a local prototype or
  a project nobody else depends on yet.

No file, or no `Merge:` line, means `ask`.

## Changing it

Only on the person's own typed word ("merge on pass from now on", "ask me
before every merge"). A session never changes this line by itself and never
reads a passing review as permission to. Record each change below.

Move to `ask` when the project goes live: the first deploy, the first outside
user, the first real data. `ship-acceptance` asks about it at the first
production run.

## History

- <date>: `<ask | on-pass>`, chosen at scaffold. <the person's reason, in a few words>

## What no policy allows

Merging a commit other than the one reviewed, merging on a red check, pushing
over the default branch's history, or deploying. Sensitive work (auth,
payments, data or migrations, CI, secrets, a public interface) always waits
for the person's read of the diff and their go.
