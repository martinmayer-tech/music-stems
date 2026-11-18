---
title: "Backlog Entry: 0000030 - Reply check notes reach the human, not the agent"
summary: "The two Stop hooks print their notes to the human, and the agent never reads them, so the same miss repeats."
status: "open"
priority: "medium"
theme: "pipeline"
---
# Backlog Entry: 0000030 - Reply check notes reach the human, not the agent

**Source feature:** 0000029-add-audioread

**Source phase:** P0

**Deferral source:** human request

**Date filed:** 2026-11-18

---

## Problem

The human sees internal check notes after a reply. The agent that wrote the reply does not see them. Two examples from 2026-11-18:

- `Stop says: [RAVINTIO] Question check: the last reply in this session starts "04:34 P0 Discovery: Question: the baseli" and its Question: line holds no question mark.`
- `Stop says: [RAVINTIO] Reply writing check: "Confirm the design: reply "Yes, I agree"" (actor-pronoun: "I", name the actor by role) This note is advisory.`

Three gaps cause this:

- `check-reply-prefix.mjs` and `check-reply-writing.mjs` write `{ systemMessage }` on stdout. The host shows that field to the human and does not pass it to the agent.
- The agent gets no signal, so it repeats the miss. `plan/.prefix-misses.log` holds the same `question:` miss at 04:15 and at 04:35.
- The writing check flags a quoted phrase. Rule `agree-ambiguous` in `orchestrator-p0-coaching.md` tells the agent to ask for the reply "Yes, I agree", and the check then reports its "I".

## Suggested Action

Send each note to the agent and keep it away from the human. Decide between two forms:

- **Enforce:** the Stop hook blocks with the note as its reason, so the agent corrects the reply in the same turn. Allow one retry for each reply, so a miss the agent cannot fix never loops.
- **Inform:** the hook writes the note to the log only, and the next prompt hook passes the open misses to the agent as context.

Also skip text inside quotation marks and code spans in the `actor-pronoun` rule.

**Observable condition:** a reply whose `Question:` line holds no question mark shows the human no `[RAVINTIO]` note, and the agent's next reply holds the correction.

## Why Deferred

The active run adds `audioread` and changes no hook. The hooks belong to the pack, and a blocking Stop hook widens a guard, so it needs its own design decision.
