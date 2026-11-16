---
title: "Requirement: REQ-003 - Worker"
summary: "A worker runs queued jobs one at a time and never lets two jobs overlap."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Worker

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Source:** US-003
**Priority:** must-have

## User Story

As a caller, I queue two jobs, so that they run one after the other and never overlap.

## Functional Requirements
- `Worker(store, data_dir=None, separator_factory=None, split_func=split)` owns one thread. `start(recover=True)` starts it and `stop()` ends it after the current job.
- The thread claims one job and calls `split_func` with the job's input path, a per-job folder under `{data_dir}/jobs/{id}`, and the `full_stems` flag. It then claims the next.
- The thread marks a job `done` with the returned paths. If `split_func` raises, it marks the job `failed` with one error line and goes on.
- The thread waits when the queue is empty. It wakes after a poll interval or when `wake()` runs.
- `start_workers(store, devices)` starts one `Worker` for each device name and returns them.

## Acceptance Criteria
- [ ] AC-1: Jobs run in turn
  - Given two queued jobs and a fake `split_func` that records its start and end times
  - When one worker runs
  - Then the second job starts after the first ends and both end as `done`
- [ ] AC-2: A failure does not stop the worker
  - Given a first job that raises and a second job that succeeds
  - When one worker runs
  - Then the first reads `failed` with one error line and the second reads `done`
- [ ] AC-3: One worker for each device
  - Given two device names
  - When the caller runs `start_workers`
  - Then it returns two running workers, and `stop()` ends both

## Dependencies
- REQ-001 and REQ-002.
