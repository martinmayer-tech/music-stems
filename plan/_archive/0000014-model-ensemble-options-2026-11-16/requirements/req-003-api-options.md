---
title: "Requirement: REQ-003 - Options in the API"
summary: "POST /jobs takes the three options, rejects a bad value with 422, stores them in jobs.options, and the worker passes them to split()."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Options in the API

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Source:** US-003
**Priority:** must-have

## User Story

As a user, I send the options with `POST /jobs`, so that the queued job uses them.

## Functional Requirements
- `POST /jobs` takes the optional form fields `model`, `ensemble_preset`, and `single_stem`. An empty string counts as unset.
- The route calls `validate_options()` before it writes the upload. A bad value gets status 422 and a `detail` text that names the value. No job and no upload file remain.
- The route stores the set options as a JSON object in `jobs.options`. The table gains no column.
- The worker passes `job.options` to `split()` as keyword arguments. The model pool keys each separator by model file and preset, so a preset never reuses a plain separator.

## Acceptance Criteria
- [ ] AC-1: Store the options
  - Given the test client and a fake separator
  - When a client posts a file with `model` set to `htdemucs_6s.yaml`
  - Then the answer is 201 and the stored job holds `{"model": "htdemucs_6s.yaml"}` in its options
- [ ] AC-2: Reject a bad value
  - Given the test client
  - When a client posts a file with a model outside the allowlist
  - Then the answer is 422, the `detail` names the model, and the store holds no job
- [ ] AC-3: Run with the options
  - Given a worker with a fake `split` function
  - When the worker claims a job that holds options
  - Then `split` receives each stored option as a keyword argument

## Dependencies
- REQ-001 holds the allowlists.
