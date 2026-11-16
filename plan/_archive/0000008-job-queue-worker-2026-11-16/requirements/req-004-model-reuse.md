---
title: "Requirement: REQ-004 - Model reuse"
summary: "A worker loads each model once and reuses it for later jobs."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-004 - Model reuse

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Source:** US-004
**Priority:** must-have

## User Story

As a caller, I queue two jobs, so that the second loads no model that the first already loaded.

## Functional Requirements
- The worker passes `split_func` a separator factory that returns a `PooledSeparator`.
- `PooledSeparator.load_model(model_filename=...)` builds a separator through the base factory and loads the model on the first request for that model. Later requests reuse the loaded separator.
- Before each use, the pool points the separator at the job's output folder.
- `PooledSeparator.separate(...)` calls the pooled separator that holds the last requested model.
- Importing `stem_service` loads no model library.

## Acceptance Criteria
- [ ] AC-1: Second job loads nothing
  - Given two jobs without `full_stems` and a counting fake separator factory
  - When one worker runs both
  - Then the fake reports one `load_model` call for the vocals model in total
- [ ] AC-2: Two passes keep both models
  - Given two jobs with `full_stems`
  - When one worker runs both
  - Then the fake reports one `load_model` call for each of the two models in total
- [ ] AC-3: No model library on import
  - Given a fresh interpreter
  - When it imports `stem_service`
  - Then `audio_separator` is absent from `sys.modules`

## Dependencies
- REQ-003.
