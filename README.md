# tc-plugins

Joe DaSilva's Claude Code workflow, packaged for the teams he trains: one
plugin, `tc-workflow`, in a marketplace called `tc-plugins`. **Public repo.**
It replaces the older edition (the `pm` plugin handed out as a local
tc-plugins folder).

What the plugin does, for the people using it:
[`plugins/tc-workflow/README.md`](plugins/tc-workflow/README.md) and the
one-page [`WORKFLOW.md`](plugins/tc-workflow/WORKFLOW.md).

## Install (each trainee, once)

```
/plugin marketplace add datacraftdevelopment/tc-plugins
/plugin install tc-workflow@tc-plugins
```

Then restart Claude Code. Anyone who has the old TC `pm` plugin removes it
first: `/plugin uninstall pm@tc-plugins`, then remove the old marketplace if it
had the same name (`/plugin marketplace remove tc-plugins`) before adding this
one. Updates: `/plugin marketplace update tc-plugins`.

Problems or ideas: `/tc-workflow:feedback` in any session drafts an issue
here, scrubbed of anything from your project, and files it on your go. Or open
one at <https://github.com/datacraftdevelopment/tc-plugins/issues/new/choose>.

## How the plugin is made

`plugins/tc-workflow/` is **generated**. Never edit it by hand.

```
build/sources.json   the two public upstreams and the exact commits used
build/files.json     the allowlist: the only upstream files that ship
build/phrases.json   word-for-word edits to upstream files, then token swaps
build/banned.json    the clean check: words that must never ship
overlay/             files this edition owns outright (laid on top)
build/build.py       does all of the above, fails loudly on any miss
tests/               build is reproducible, clean check works, guard suite passes
```

Rebuild after changing anything above, with public checkouts of
`datacraftdevelopment/dc-dev-plugins` and `datacraftdevelopment/agent-runway`
next to this repo (or pass `--pm-sp-src` / `--agent-runway-src`):

```bash
python3 build/build.py
python3 -m unittest discover tests
```

Then bump `overlay/.claude-plugin/plugin.json`'s version, rebuild, read the
diff of `plugins/`, and commit.

**Taking a newer upstream:** set the new commit in `build/sources.json` and
rebuild. A phrase that no longer matches, a file that moved, or a banned word
that appeared stops the build with the file and line. Fix the map, or move the
file into `overlay/` and own it. Read the diff of `plugins/` before
committing.

## Rules

- **This repo is public.** No company or client names, internal hosts,
  credentials or anything under NDA, in the plugin, the build files or issues.
  The plugin is a way of working, not project knowledge.
- A generic improvement found here goes upstream as its own clean change,
  written there; nothing is copied back wholesale.
- The build only exports tracked files at pinned commits (`git archive`), never
  a working tree, and refuses links.
