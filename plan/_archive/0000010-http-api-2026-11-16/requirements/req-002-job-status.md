---
title: "Requirement: REQ-002 - Job status"
summary: "A caller reads one job or the list of jobs and follows a job to done or failed."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Job status

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Source:** US-002
**Priority:** must-have

## User Story

As a caller, I read one job or the list of jobs, so that I can follow a job to `done` or `failed`.

## Functional Requirements
- `GET /jobs/{id}` returns the job as JSON with `id`, `status`, `full_stems`, `stems`, `error`, `created_at`, `started_at`, and `finished_at`.
- `stems` holds the file names of the job's outputs, or `null` until the job is `done`.
- The JSON holds no server path.
- `GET /jobs` returns every job in creation order as a JSON list.
- An unknown id gets status 404.

## Acceptance Criteria
- [ ] AC-1: Read one job
  - Given a queued job in the store
  - When the caller reads `GET /jobs/{id}`
  - Then the answer is 200 with the status `queued`, `stems` set to `null`, and no server path in the body
- [ ] AC-2: Read the list
  - Given two jobs in the store
  - When the caller reads `GET /jobs`
  - Then the answer lists both jobs, the older one first
- [ ] AC-3: Read an unknown job
  - Given an empty store
  - When the caller reads `GET /jobs/unknown`
  - Then the answer is 404

## Dependencies
- REQ-001 adds the jobs that this route reads. The tests add jobs through the store.
