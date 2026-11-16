---
title: "Story Map - 0000014-model-ensemble-options"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000014-model-ensemble-options

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Call the library | Pass a model, a preset, and a stem to `split()` | US-001 | REQ-001 |
| Use the shell | Pass the same options to `stems split` | US-002 | REQ-002 |
| Queue a job | Send the options with `POST /jobs` | US-003 | REQ-003 |
| Use the page | Choose the options on the upload form | US-004 | REQ-004 |

## Gaps

- Pick the pass 1 model: gap: out of scope. The brief names only the preset for pass 1.
- Type a free model name: gap: out of scope. The brief wants an allowlist.
- List the options through a route: gap: out of scope. The page holds the same list as text.
