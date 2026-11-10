---
name: poc
description: "Build a clickable proof of concept of the main journey on JSON mock data, before any spec or ticket: the person plays with it, their feedback changes it, and it loops until they type approved. The approved POC is kept in the repo as the reference the spec, the tickets and the reviewers use. Use when new work has screens or data someone has to look at, when intake picks the POC path, or when the person says 'build a POC', 'mock it up so I can play with it', 'let me see it first'. For one narrow question use prototype instead."
---

# POC first

Nobody knows what they want from a page of prose. A POC puts the main journey
in front of the person while changing it still costs minutes: real-looking
data, pages they can click through, nothing behind them. What they approve
becomes the picture everything later is measured against.

A `prototype` answers one question and is thrown away. A POC shows the whole
main journey, is kept, and its approval is recorded.

## Where it lives

`docs/poc/<topic>/` in the repo, committed, never inside the app's source:

- `poc.md`: the record (format below).
- `index.html` and any further pages: plain HTML, CSS and JS with no build
  step and nothing to install. HTML even when the product will be a native app
  or another stack: this is the fastest thing to look at and change.
- `data/*.json`: the mock data, one file per entity.

Create the folder only when the first file is written.

## 1. Enough questions to build it, no more

Run `grill` in its **to a POC** mode: five to eight questions at most, only
the ones whose answer changes what the POC shows (who uses it, the main
journey step by step, which screens, which things appear on them). Everything
else you assume, and write each assumption down in `poc.md`. A wrong
assumption the person can see is corrected faster than a question answered
cold.

When `intake` already wrote a brief the person agreed to, start from it and
ask only what it leaves open.

## 2. The data sample

Write `data/*.json` before any page: the pages take their shape from it.

- **Start from what exists.** A schema, a migration, an API response, an
  export, a spreadsheet the person points at. Keep the real field names and
  shapes. Invent a shape only when nothing exists, and say that you did.
- **Never real records.** Shapes from the real system, values made up: no real
  names, emails, account numbers or anything copied out of production. The
  POC is committed and may be shared.
- **Put the ugly rows in on purpose:** a very long name, an empty list, a few
  hundred rows where a list could grow, an optional field left out, a status
  nobody planned for. These are what break a layout.
- A dozen believable rows per entity is the floor. Three rows of "Test 1"
  hide every real problem.

## 3. Build it, without asking

- The **main journey end to end**, clickable: the screens the person walks
  through in order, each showing the mock data. Side paths get a visible stub
  ("not in the POC") rather than a dead link.
- Pages load the JSON with `fetch`, and what the person does in a page
  (add, edit, filter) changes it in memory only. Nothing is saved, nobody
  signs in, nothing calls a server.
- Give every screen a **short stable name** in its title and in `poc.md`
  (`S1 list`, `S2 detail`, `S3 new entry`). The spec, the tickets and the
  reviewers point at screens by these names.
- Show the states that matter on each screen: empty, loading where it would
  be slow, an error, the very long value.
- Follow the look of the existing product when there is one. With no product
  yet, keep it plain and legible; the POC settles what is on each screen and
  how the journey flows, not the final polish.
- No tests, no error handling beyond what is shown, no tidying of the code.
  It is a reference to look at, never source to paste into the product.

Don't stop to ask while building. A choice you had to make goes on the
assumptions list.

## 4. Put it in front of the person

A browser will not `fetch` JSON from a page opened as a file, so serve the
folder and give the address:

```bash
python3 -m http.server 8765 --directory docs/poc/<topic>
```

(run it in the background; pick another port if that one is taken). Commit the
POC, set `Status: with you`, and tell the person in a few lines:

- the address to open and the order to walk the screens in;
- the assumptions you baked in, as a short list they can scan;
- what is faked (saving, sign-in, anything slow);
- then: "Play with it and tell me what's wrong, what's missing and what you'd
  change." And **stop**.

## 5. The feedback loop

The person reacts however they like: a list, a ramble, one word. Sort every
remark into one of four, and show them the sort before acting:

| Goes to | When |
| --- | --- |
| **Change the POC now** | Something on a screen or in the journey should be different |
| **Decision** | A rule or a choice the spec has to carry ("managers see everyone's, staff see their own") |
| **Question** | The remark opens something the POC can't settle; it goes to the second round of `grill` |
| **Not this job** | A good idea outside the brief; one line in `docs/inbox.md` |

Then make the changes, commit, and say what changed, screen by screen. Run the
second round of `grill` (its **after the POC** mode) for the questions, and
for what no screen shows: edges, errors, permissions, data rules, volumes,
what is out of scope. Answers that change a screen go back into the POC.

Write each round into `poc.md`. Repeat until the person types **approved**
(or a plain equivalent: "that's it, go"). Silence, or "looks good so far", is
not approval: ask.

## 6. Approved

Commit, then set `Status: approved <date> <short sha>`, naming that commit, and
commit the status line. Stop the server. Go on to `spec` without being asked:
that is the next stage, and its approval is the next place the person steers.

A change to the POC after approval puts the status back to `with you`, and it
needs approving again. The approval is for one commit, like a review.

## poc.md

```markdown
# POC: <topic>

Status: draft | with you | approved <date> <short sha>

## Brief
What it is, who uses it, the main journey in numbered steps, what is out.

## Screens
- S1 <name>: `index.html`. <one line: what it is for>
- S2 <name>: `detail.html`. …

## Data
- `data/<entity>.json`: where its shape came from (schema, export, invented).

## Assumptions
- <a choice made without asking>. Confirmed | changed in round N | open.

## Faked
- <what the POC pretends: saving, sign-in, …>

## Round 1, <date>
What the person said, sorted (changed, decisions, questions, not this job),
and what changed in the POC.

## Decisions
One line each, with its reason. The spec copies these.
```

## What the approved POC is used for

- `spec` links the screens instead of describing them, and names the JSON as
  the shape of the data.
- `file-tickets` makes the first ticket the main journey made real, and
  points builders at `data/*.json` for their test fixtures.
- The function reviewer compares built screens with POC screens for every
  Acceptance line that says "matches POC screen S…".
- A builder whose choice would make the product differ from the approved POC
  stops and asks. That is not a ruling to make alone.

## Never

- Start the spec or file a ticket on a POC that is not approved.
- Put real records in the mock data, or the POC inside the product's source.
- Grow the POC into the product. When it starts needing real saving, sign-in
  or tests, it has done its job: get it approved and spec the real thing.
- Ask the person questions a look at the POC would answer.
