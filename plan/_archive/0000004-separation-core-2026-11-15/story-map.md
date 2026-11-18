---
title: "Story Map - 0000004-separation-core"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000004-separation-core

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Split a mix | Call `split(mix, out)` and read two paths | US-001 | REQ-001 |
| Split a mix | Call `split(mix, out, full_stems=True)` and read five paths | US-002 | REQ-002 |
| Set up the service | Install the pinned `audio-separator` extra | US-003 | REQ-003 |
| Set up the service | Point `STEMS_MODEL_DIR` at a persistent folder | US-003 | REQ-001 |

## Gaps

- Pick a model per call: gap: out of scope. Step 7 adds model choice.
