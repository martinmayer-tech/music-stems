---
title: "Story Map - 0000010-http-api"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000010-http-api

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Queue a job | Upload an audio file | US-001 | REQ-001 |
| Follow a job | Read one job or the list of jobs | US-002 | REQ-002 |
| Collect stems | Download each stem of a finished job | US-003 | REQ-003 |
| Run the service | Start it on a safe address and reject bad uploads | US-004 | REQ-004 |

## Gaps

- Cancel or delete a job: gap: out of scope. The brief asks for neither.
- Log in: gap: out of scope. The chart sets no login.
- Pick a model: gap: out of scope. Step 7 adds it.
