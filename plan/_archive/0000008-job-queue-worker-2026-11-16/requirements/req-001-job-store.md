---
title: "Requirement: REQ-001 - Job store"
summary: "A caller adds a job and reads it as it moves through queued, running, done, or failed."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Job store

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Source:** US-001
**Priority:** must-have

## User Story

As a caller, I add a job and read its status, so that I can follow it from `queued` to `done` or `failed`.

## Functional Requirements
- `JobStore(path)` creates the folder, the SQLite file, and the `jobs` table if they do not exist.
- `add(input_path, full_stems=False, options=None)` inserts a `queued` job and returns its id.
- `get(job_id)` returns the job as a `Job` object, or `None` for an unknown id. `list()` returns every job in creation order.
- `claim_next()` sets the oldest `queued` job to `running` with `started_at`, and returns it. It returns `None` for an empty queue.
- `mark_done(job_id, outputs)` sets `done`, stores the output paths, and sets `finished_at`.
- `mark_failed(job_id, error)` sets `failed`, stores one error line, and sets `finished_at`.
- `resolve_data_dir()` returns `STEMS_DATA_DIR`, or `./data` when the variable is unset or empty.

## Acceptance Criteria
- [ ] AC-1: Add and read
  - Given an empty store
  - When the caller adds a job with `full_stems=True`
  - Then `get()` returns a `queued` job that holds the input path, the flag, and a `created_at` time
- [ ] AC-2: Claim in order
  - Given two queued jobs
  - When the caller claims twice, then claims a third time
  - Then the first claim returns the older job, the second returns the newer job, and the third returns `None`
- [ ] AC-3: Finish
  - Given a running job
  - When the caller marks one job done with two paths and another failed with an error
  - Then the first reads `done` with the paths and the second reads `failed` with the error, and both hold `finished_at`

## Dependencies
- None.
