---
title: "Story Map - 0000029-add-audioread"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000029-add-audioread

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Install the engine | Install the `separation` extra and get `audioread` with it | US-002 | REQ-001 |
| Build the image | Build the image and get `audioread` at the same version | US-001 | REQ-001 |
| Separate a track | Upload a track to a fresh image and see the job end `done` | US-001 | REQ-002 |

## Gaps

- Run a separation in CI: gap: out of scope. The design keeps real models out of CI.
- Run a job in the GPU image: gap: out of scope. The design lists the GPU image run as out.
