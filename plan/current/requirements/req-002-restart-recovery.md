---
title: "Requirement: REQ-002 - Restart recovery"
summary: "Jobs survive a restart, and a job that a restart interrupted runs again."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Restart recovery

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Source:** US-002
**Priority:** must-have

## User Story

As a caller, I restart the service, so that queued jobs still run and a half-run job runs again.

## Functional Requirements
- Every state change commits before the call returns, so a new `JobStore` on the same file reads each job.
- `recover()` sets every `running` job back to `queued`, clears `started_at`, and returns the number of jobs it changed.
- `Worker.start()` calls `recover()` once, before its thread claims a job. `start_workers` calls `recover()` once for all workers, and starts each worker with `recover=False`, so a second worker never requeues the job of the first.

## Acceptance Criteria
- [ ] AC-1: Jobs persist
  - Given a store with one queued and one done job
  - When the caller opens a second `JobStore` on the same file
  - Then it reads both jobs with the same status and outputs
- [ ] AC-2: Interrupted job
  - Given a store with one `running` job
  - When the caller runs `recover()`
  - Then it returns 1 and the job reads `queued` with no `started_at`

## Dependencies
- REQ-001.
