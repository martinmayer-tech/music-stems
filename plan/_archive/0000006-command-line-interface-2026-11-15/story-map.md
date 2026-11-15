---
title: "Story Map - 0000006-command-line-interface"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000006-command-line-interface

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Split a mix | Run `stems split mix.wav --output-dir out` and read the paths | US-001 | REQ-001 |
| Split a mix | Add `--full-stems` and read five paths | US-002 | REQ-002 |
| Check the setup | Run `stems env` | US-003 | REQ-003 |
| Check the setup | Run `stems models` | US-004 | REQ-004 |

## Gaps

- Pick a model per call: gap: out of scope. Step 7 adds model choice.
