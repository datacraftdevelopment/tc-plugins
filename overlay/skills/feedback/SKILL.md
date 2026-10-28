---
name: feedback
description: "File a bug report or an idea about this plugin (tc-workflow) on its public GitHub repo, datacraftdevelopment/tc-plugins. Use when the person says a skill is broken, confusing or missing and wants to tell whoever maintains it, or says 'send feedback', 'report this', 'file a bug about the plugin', or runs /tc-workflow:feedback."
---

# Feedback on the plugin

The person wants to report a problem or an idea about **this plugin itself**
(a skill that misbehaved, a step that confused them, something missing). Draft
one GitHub issue on `datacraftdevelopment/tc-plugins`, show it, and file it
only on their go. This is not for bugs in their own project: those go in their
project's tracker.

1. **Understand it.** Read what they said. If it's unclear whether it's a bug
   or an idea, or what they expected, ask one question.

2. **Gather facts without asking.** Skip any that fail; never guess:
   - the plugin version: `version` in
     `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`;
   - Claude Code: `claude --version`;
   - the system: `sw_vers -productVersion` on a Mac, otherwise `uname -sr`;
   - which skill was involved, from this conversation;
   - for a failure: the exact error text, and the step the skill was on.

3. **Search first.**
   `gh issue list -R datacraftdevelopment/tc-plugins --state all --search "<2-3 key words>"`.
   If one looks like the same problem, show it and offer to add a comment there
   instead of opening a new issue.

4. **Draft.** A title under 70 characters. Body sections: **What happened**
   (or **What I want**), **Steps**, **Expected**, **Facts** (plugin version,
   Claude Code version, system, skill). Label `bug` or `enhancement`.

5. **Scrub it. The repo is PUBLIC.** Remove tokens, keys, passwords, URLs
   with credentials, hostnames, machine names, company, client and people's
   names, private repo names, ticket contents, and any code or file contents
   from the person's own project. Replace home paths with `~` and project
   paths with `<project>`. Describe the project only in general words
   ("a Python web app"). When in doubt, leave it out.

6. **Show the whole draft** and say: "This will be public on GitHub. File
   it?" Wait for a go typed in this session. Anything else is not a go.

7. **File on go.** Write the body to a temp file, then:
   `gh issue create -R datacraftdevelopment/tc-plugins --title "<title>" --body-file <file> --label <bug|enhancement>`.
   If `gh` is missing or not signed in, build
   `https://github.com/datacraftdevelopment/tc-plugins/issues/new?title=<enc>&body=<enc>&labels=<label>`
   (URL-encoded; if the body is very long, keep the essentials and say what to
   paste), open it (`open <url>` on a Mac) and tell them to press Submit.
   Reply with the issue link, or that the page is open.

## Never

- File without the person's typed go, or file more than one issue per report.
- Put anything from their project or their company into the issue.
