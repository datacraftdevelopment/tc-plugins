---
name: grill
description: "Interview the person about a plan, one question at a time. Three modes: to a POC (a handful of questions, just enough to build something to look at), after the POC (what no screen can show), and full (until every open branch is settled, for work with nothing to look at). Use when the person says 'grill me', 'stress-test this', 'poke holes in it', when poc or intake calls it, or when work is about to be specced and decisions are still open. Asks, never builds."
---

# Grill the plan

Work that runs unattended can't stop to ask what the person meant. Every question left open now becomes a guess
later, made by a worker with none of this conversation. This skill settles those questions while the person is here.

## Which mode

- **To a POC** (called from `poc` or `intake`: work with screens or data to look at). **Five to eight questions at
  most.** Ask only what changes what the POC shows: who uses it, the main journey step by step, which screens, which
  things appear on them. Every other open branch becomes an assumption, written down for `poc.md`, not a question.
  Stop at the cap even if branches are open: the person settles them faster by looking.
- **After the POC** (the person has played with it). Start from their feedback and the assumptions list. Ask what no
  screen can show: edges (empty, too many, offline, failing), errors, who may see or change what, data rules,
  volumes, what is out of scope, how anyone will know it works. No cap; stop when nothing open would change what
  gets built.
- **Full** (no POC: a command-line tool, a service, a refactor, a rule change). Everything below, until nothing is
  open.

The steps are the same in every mode; only where you stop differs.

## How to run it

1. **Read first.** Look at what already exists before asking anything you could find out yourself: the repo, its
   docs, recent commits, any spec or map in progress. Never ask what a file can answer.
2. **List the open branches, privately.** For the plan in front of you, note each decision that isn't made yet:
   what it does, who uses it, what is out of scope, what happens at the edges (empty, too many, offline, failing),
   how anyone will know it works.
3. **Ask one question at a time.** Start with the one the most other answers hang on. Put your recommended answer
   with it, and why, so the person can just say yes. Offer two or three choices when the space is small.
4. **Follow the answer down.** Each answer opens or closes branches. Go deep on the branch you're in before you
   move on. If an answer contradicts an earlier one, say so and ask which stands.
5. **Keep a running list** of what has been decided, in a line each. Show it when it grows past five or six
   lines, and at the end.
6. **Stop when nothing is open** that would change what gets built, or when the person says enough. Anything still
   open is written down as open, never quietly assumed.

## Rules

- One question per message. A list of ten questions gets ten half answers.
- Ask about behaviour and outcomes, not implementation the person doesn't care about.
- You may push back. If an answer will cause trouble, say what trouble, once, then accept their call.
- Don't write code or files while grilling, except the decisions list if the person asks for it saved.

## After

Go on to the next stage without waiting to be asked: after **to a POC**, build it (`poc`); after the other two, write
it up (`spec`). Use `prototype` on the way when one narrow question is best answered by seeing it.
