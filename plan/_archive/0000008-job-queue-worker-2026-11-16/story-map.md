---
title: "Story Map - 0000008-job-queue-worker"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000008-job-queue-worker

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Queue a job | Add a job and read its status | US-001 | REQ-001 |
| Keep jobs across a restart | Reopen the store and read the jobs | US-002 | REQ-002 |
| Run jobs | Queue two jobs and watch them run in turn | US-003 | REQ-003 |
| Run jobs | Queue two jobs and check that models load once | US-004 | REQ-004 |

## Gaps

- Cancel a job: gap: out of scope. The brief asks for no cancel.
- Call the queue over HTTP: gap: out of scope. Step 5 adds the API.
